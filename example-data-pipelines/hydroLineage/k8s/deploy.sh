#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

#
# HydroLineage Airflow 3.16 Single-Step Deployment Script
# This script is idempotent and can be run multiple times safely
#
# Features:
# - Pre-flight checks (kubectl, helm, cluster connectivity)
# - Automatic database backup before migration
# - Helm dependency updates
# - ConfigMap creation/updates (idempotent)
# - Database migration post-deployment
# - Airbyte bootstrap with connection variable setup
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AIRFLOW_VERSION="3.1.6"
RELEASE_NAME="airflow-lineage"
NAMESPACE="hydro-lineage"
BACKUP_DIR="$SCRIPT_DIR/backups"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}HydroLineage Airflow ${AIRFLOW_VERSION} Deployment${NC}"
echo -e "${BLUE}========================================${NC}"

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================
echo -e "\n${YELLOW}Running pre-flight checks...${NC}"

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"
command -v kubectl >/dev/null 2>&1 || { echo -e "${RED}❌ kubectl not found. Install it first.${NC}"; exit 1; }
command -v helm >/dev/null 2>&1 || { echo -e "${RED}❌ helm not found. Install it first.${NC}"; exit 1; }
echo -e "${GREEN}✅ kubectl and helm found${NC}"

# Check cluster connection
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Cannot connect to Kubernetes cluster. Configure kubectl first.${NC}"
    exit 1
fi
CURRENT_CONTEXT=$(kubectl config current-context)
echo -e "${GREEN}✅ Connected to cluster: ${CURRENT_CONTEXT}${NC}"

echo -e "${GREEN}✅ Pre-flight checks passed${NC}"

# =============================================================================
# HELM DEPENDENCIES
# =============================================================================
echo -e "\n${YELLOW}Updating Helm dependencies...${NC}"
echo "✅ Connected to cluster: $(kubectl config current-context)"

# Update Helm dependencies
echo ""
echo "Updating Helm dependencies..."
cd "$SCRIPT_DIR/helm"
helm dependency update
echo -e "${GREEN}✅ Dependencies updated${NC}"

# =============================================================================
# NAMESPACE AND SECRETS
# =============================================================================
echo -e "\n${YELLOW}Ensuring namespace and secrets exist...${NC}"

# Ensure namespace exists before creating ConfigMaps
if kubectl get ns "$NAMESPACE" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Namespace $NAMESPACE already exists${NC}"
else
    kubectl create ns "$NAMESPACE"
    echo -e "${GREEN}✅ Namespace $NAMESPACE created${NC}"
fi

# If the chart includes a Namespace resource, Helm requires ownership metadata to adopt an existing namespace.
kubectl label ns "$NAMESPACE" app.kubernetes.io/managed-by=Helm --overwrite >/dev/null
kubectl annotate ns "$NAMESPACE" meta.helm.sh/release-name="$RELEASE_NAME" meta.helm.sh/release-namespace="$NAMESPACE" --overwrite >/dev/null

# Early token prerequisite check: fail before backup/deploy if neither a valid
# local DATAHUB_GMS_TOKEN nor an existing secret is available.
LOCAL_DATAHUB_TOKEN_PRECHECK="${DATAHUB_GMS_TOKEN:-}"
if [ -z "$LOCAL_DATAHUB_TOKEN_PRECHECK" ] || [ ${#LOCAL_DATAHUB_TOKEN_PRECHECK} -lt 10 ]; then
  if ! kubectl get secret datahub-gms-token -n "$NAMESPACE" >/dev/null 2>&1; then
    echo -e "${RED}❌ Missing DataHub token requirement: set DATAHUB_GMS_TOKEN (>=10 chars) or create secret datahub-gms-token in namespace $NAMESPACE${NC}"
    exit 1
  fi
fi

# Database password for warehouse/dbt connectivity.
# Preferred: export HYDRO_POSTGRES_PASSWORD='...'
if [ -n "${HYDRO_POSTGRES_PASSWORD:-}" ]; then
  HYDRO_POSTGRES_PASSWORD_VALUE="${HYDRO_POSTGRES_PASSWORD}"
elif [ -n "${POSTGRES_PASSWORD:-}" ]; then
  HYDRO_POSTGRES_PASSWORD_VALUE="${POSTGRES_PASSWORD}"
  echo -e "${YELLOW}⚠️  Using legacy POSTGRES_PASSWORD env var. Prefer HYDRO_POSTGRES_PASSWORD.${NC}"
else
  EXISTING_WAREHOUSE_PASSWORD=$(kubectl get secret "${RELEASE_NAME}-warehouse-postgresql" -n "$NAMESPACE" -o jsonpath='{.data.password}' 2>/dev/null | base64 -d || true)
  if [ -z "$EXISTING_WAREHOUSE_PASSWORD" ]; then
    EXISTING_WAREHOUSE_PASSWORD=$(kubectl get secret "${RELEASE_NAME}-warehouse-postgresql" -n "$NAMESPACE" -o jsonpath='{.data.postgres-password}' 2>/dev/null | base64 -d || true)
  fi

  if [ -n "$EXISTING_WAREHOUSE_PASSWORD" ]; then
    HYDRO_POSTGRES_PASSWORD_VALUE="$EXISTING_WAREHOUSE_PASSWORD"
    echo -e "${GREEN}✅ Using existing warehouse Postgres password from secret ${RELEASE_NAME}-warehouse-postgresql.${NC}"
  else
    HYDRO_POSTGRES_PASSWORD_VALUE="hydro_secure_password_2024"
    echo -e "${YELLOW}⚠️  HYDRO_POSTGRES_PASSWORD not set and no existing warehouse secret found; using demo fallback password.${NC}"
  fi
fi

# Airflow metadata/result backend DB password.
# Preferred: export AIRFLOW_DB_PASSWORD='...'
if [ -n "${AIRFLOW_DB_PASSWORD:-}" ]; then
  AIRFLOW_DB_PASSWORD_VALUE="${AIRFLOW_DB_PASSWORD}"
else
  AIRFLOW_DB_PASSWORD_VALUE="airflow_secure_password_2024"
  echo -e "${YELLOW}⚠️  AIRFLOW_DB_PASSWORD not set; using default Airflow metadata DB password.${NC}"
fi

# Create/update DB credentials secret consumed by Airflow + dbt profile env vars.
kubectl create secret generic hydro-db-credentials -n "$NAMESPACE" \
  --from-literal=POSTGRES_PASSWORD="$HYDRO_POSTGRES_PASSWORD_VALUE" \
  --from-literal=DBT_PASSWORD="$HYDRO_POSTGRES_PASSWORD_VALUE" \
  --from-literal=AIRFLOW_CONN_HYDRO_POSTGRES="postgresql://postgres:${HYDRO_POSTGRES_PASSWORD_VALUE}@${RELEASE_NAME}-warehouse-postgresql:5432/hydro" \
  --dry-run=client -o yaml | kubectl apply -f - >/dev/null
echo "✅ DB credentials secret applied (hydro-db-credentials)"

# =============================================================================
# DATABASE BACKUP (if upgrading existing deployment)
# =============================================================================
if helm list -n "$NAMESPACE" | grep -q "^$RELEASE_NAME\s"; then
    echo -e "\n${YELLOW}Existing deployment detected - backing up Airflow metadata database...${NC}"
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    
    # Check if Airflow PostgreSQL pod exists
    if kubectl get pod -n "$NAMESPACE" -l app.kubernetes.io/name=postgresql,app.kubernetes.io/component=primary --no-headers 2>/dev/null | grep -q "Running"; then
        BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
        BACKUP_FILE="$BACKUP_DIR/airflow_metadata_${BACKUP_DATE}.sql"
        
        echo -e "${YELLOW}Creating backup: $BACKUP_FILE${NC}"
        
        POSTGRES_POD=$(kubectl get pod -n "$NAMESPACE" -l app.kubernetes.io/name=postgresql,app.kubernetes.io/component=primary -o jsonpath='{.items[0].metadata.name}')
        
        if kubectl exec -n "$NAMESPACE" "$POSTGRES_POD" -- pg_dump -U airflow airflow > "$BACKUP_FILE" 2>/dev/null; then
            echo -e "${GREEN}✅ Backup completed: $BACKUP_FILE${NC}"
        else
            echo -e "${YELLOW}⚠️  Backup failed or skipped (may be first deployment)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  PostgreSQL pod not running, skipping backup${NC}"
    fi
else
    echo -e "\n${GREEN}New deployment - no backup needed${NC}"
fi

# =============================================================================
# DATAHUB TOKEN SECRET
# =============================================================================
echo -e "\n${YELLOW}Checking DataHub token secret...${NC}"

# Require either:
# 1) a valid local DATAHUB_GMS_TOKEN env var (>= 10 chars), or
# 2) an existing Kubernetes secret named datahub-gms-token.
LOCAL_DATAHUB_TOKEN="${DATAHUB_GMS_TOKEN:-}"
HAS_VALID_LOCAL_TOKEN=false

if [ -n "$LOCAL_DATAHUB_TOKEN" ] && [ ${#LOCAL_DATAHUB_TOKEN} -ge 10 ]; then
  HAS_VALID_LOCAL_TOKEN=true
fi

if [ "$HAS_VALID_LOCAL_TOKEN" = true ]; then
  kubectl create secret generic datahub-gms-token -n "$NAMESPACE" \
    --from-literal=DATAHUB_GMS_TOKEN="$LOCAL_DATAHUB_TOKEN" \
    --from-literal=AIRFLOW__DATAHUB__TOKEN="$LOCAL_DATAHUB_TOKEN" \
    --dry-run=client -o yaml | kubectl apply -f - >/dev/null
  echo "✅ DataHub token secret applied from local DATAHUB_GMS_TOKEN"
else
  if [ -n "$LOCAL_DATAHUB_TOKEN" ] && [ ${#LOCAL_DATAHUB_TOKEN} -lt 10 ]; then
    echo "⚠️  DATAHUB_GMS_TOKEN is set but too short (<10 chars); ignoring local value"
  fi

  if kubectl get secret datahub-gms-token -n "$NAMESPACE" >/dev/null 2>&1; then
    echo "ℹ️  Using existing DataHub token secret (datahub-gms-token)"
  else
    echo "❌  Missing DataHub token: set DATAHUB_GMS_TOKEN (>=10 chars) or create secret datahub-gms-token in namespace $NAMESPACE"
    exit 1
  fi
fi

# Resolve effective DataHub token used for Helm overrides and Airflow connection setup.
if [ "$HAS_VALID_LOCAL_TOKEN" = true ]; then
  EFFECTIVE_DATAHUB_TOKEN="$LOCAL_DATAHUB_TOKEN"
else
  EFFECTIVE_DATAHUB_TOKEN=$(kubectl get secret datahub-gms-token -n "$NAMESPACE" -o jsonpath='{.data.DATAHUB_GMS_TOKEN}' 2>/dev/null | base64 -d || true)
  if [ -z "$EFFECTIVE_DATAHUB_TOKEN" ]; then
    EFFECTIVE_DATAHUB_TOKEN=$(kubectl get secret datahub-gms-token -n "$NAMESPACE" -o jsonpath='{.data.AIRFLOW__DATAHUB__TOKEN}' 2>/dev/null | base64 -d || true)
  fi
  if [ -z "$EFFECTIVE_DATAHUB_TOKEN" ]; then
    echo "❌ datahub-gms-token exists but contains no DATAHUB_GMS_TOKEN/AIRFLOW__DATAHUB__TOKEN value"
    exit 1
  fi
fi

# Determine a stable Airflow secret key value.
# Airflow 3 prefers [api].secret_key. Keep this aligned with webserver secret key
# to avoid deprecation warnings and token mismatch issues.
CURRENT_WEBSERVER_SECRET_KEY=$(kubectl get secret airflow-webserver-secret -n "$NAMESPACE" -o jsonpath='{.data.webserver-secret-key}' 2>/dev/null | base64 -d || true)
if [ -n "$CURRENT_WEBSERVER_SECRET_KEY" ] && [ "$CURRENT_WEBSERVER_SECRET_KEY" != "CHANGE_ME_RANDOM_STRING_32_CHARS" ]; then
  WEBSERVER_SECRET_KEY="$CURRENT_WEBSERVER_SECRET_KEY"
else
  WEBSERVER_SECRET_KEY=$(openssl rand -hex 32)
fi

# Create DAGs ConfigMap BEFORE Helm deploy so pods can mount it during init
echo ""
echo "Creating DAGs ConfigMap from ../dags/*.py (pre-deploy)..."

# NOTE: Keep this ConfigMap small: include only python DAG files (ConfigMaps have ~1MiB limit).
CM_ARGS=()
for f in "$SCRIPT_DIR"/../dags/*.py; do
    [ -f "$f" ] && CM_ARGS+=("--from-file=$(basename "$f")=$f")
done
for f in "$SCRIPT_DIR"/../dags/utils/*.py; do
    [ -f "$f" ] && CM_ARGS+=("--from-file=utils_$(basename "$f")=$f")
done

if [ ${#CM_ARGS[@]} -gt 0 ]; then
  kubectl create configmap "${RELEASE_NAME}-dags" -n "$NAMESPACE" \
    "${CM_ARGS[@]}" \
    --dry-run=client -o yaml | kubectl apply -f -
else
  # Create an empty ConfigMap so Airflow pods can mount it even if no DAG files are present.
  kubectl create configmap "${RELEASE_NAME}-dags" -n "$NAMESPACE" \
    --dry-run=client -o yaml | kubectl apply -f -
fi

echo "✅ DAGs ConfigMap created/updated"

# Create DBT ConfigMap BEFORE Helm deploy so pods can mount it during init
echo ""
echo "Creating dbt ConfigMap from ../dbt/ (pre-deploy, excluding target and compiled files)..."

if [ -d "$SCRIPT_DIR/../dbt" ]; then
  # Install dbt dependencies locally before creating ConfigMap
  echo "Installing dbt dependencies..."
  if command -v dbt >/dev/null 2>&1; then
    cd "$SCRIPT_DIR/../dbt"
    dbt deps --profiles-dir . 2>/dev/null || echo "⚠️  dbt deps failed, continuing anyway (packages may be pre-installed)"
    cd "$SCRIPT_DIR"
    echo "✅ dbt dependencies installed"
  else
    echo "⚠️  dbt not found locally, skipping dbt deps (ensure dbt_packages exists or init containers will need network access)"
  fi
  
  CM_ARGS_DBT=()
  
  # Add dbt project files (exclude target, logs, dbt_packages to avoid ConfigMap size limits)
  for f in "$SCRIPT_DIR"/../dbt/*.yml "$SCRIPT_DIR"/../dbt/*.yaml; do
      [ -f "$f" ] && CM_ARGS_DBT+=("--from-file=$(basename "$f")=$f")
  done
  
  # Add models directory recursively
  if [ -d "$SCRIPT_DIR/../dbt/models" ]; then
    for f in $(find "$SCRIPT_DIR/../dbt/models" -type f -name "*.sql" -o -name "*.yml" -o -name "*.yaml"); do
      rel_path="${f#$SCRIPT_DIR/../dbt/}"
      CM_ARGS_DBT+=("--from-file=${rel_path//\//__}=$f")
    done
  fi
  
  # Add macros directory
  if [ -d "$SCRIPT_DIR/../dbt/macros" ]; then
    for f in $(find "$SCRIPT_DIR/../dbt/macros" -type f -name "*.sql"); do
      rel_path="${f#$SCRIPT_DIR/../dbt/}"
      CM_ARGS_DBT+=("--from-file=${rel_path//\//__}=$f")
    done
  fi
  
  # Add seeds directory
  if [ -d "$SCRIPT_DIR/../dbt/seeds" ]; then
    for f in $(find "$SCRIPT_DIR/../dbt/seeds" -type f -name "*.csv" -o -name "*.yml" -o -name "*.yaml"); do
      rel_path="${f#$SCRIPT_DIR/../dbt/}"
      CM_ARGS_DBT+=("--from-file=${rel_path//\//__}=$f")
    done
  fi
  
  # Add tests directory
  if [ -d "$SCRIPT_DIR/../dbt/tests" ]; then
    for f in $(find "$SCRIPT_DIR/../dbt/tests" -type f -name "*.sql"); do
      rel_path="${f#$SCRIPT_DIR/../dbt/}"
      CM_ARGS_DBT+=("--from-file=${rel_path//\//__}=$f")
    done
  fi
  
  # Note: dbt_packages NOT included in ConfigMap (too large)
  # Packages will be installed via dbt deps in init container
  
  if [ ${#CM_ARGS_DBT[@]} -gt 0 ]; then
    kubectl create configmap "${RELEASE_NAME}-dbt" -n "$NAMESPACE" \
      "${CM_ARGS_DBT[@]}" \
      --dry-run=client -o yaml | kubectl apply -f -
    echo "✅ dbt ConfigMap created/updated (${#CM_ARGS_DBT[@]} files)"
  else
    echo "❌  No dbt files found to add to ConfigMap"
  fi
else
  echo "❌  dbt directory not found at $SCRIPT_DIR/../dbt"
fi

# Create DataHub recipes ConfigMap BEFORE Helm deploy so pods can mount it during init
echo ""
echo "Creating DataHub recipes ConfigMap from ../datahub/recipes/ (pre-deploy)..."

if [ -d "$SCRIPT_DIR/../datahub/recipes" ]; then
  CM_ARGS_DATAHUB=()
  
  # Add recipe YAML files
  for f in "$SCRIPT_DIR"/../datahub/recipes/*.yml "$SCRIPT_DIR"/../datahub/recipes/*.yaml; do
      [ -f "$f" ] && CM_ARGS_DATAHUB+=("--from-file=$(basename "$f")=$f")
  done
  
  if [ ${#CM_ARGS_DATAHUB[@]} -gt 0 ]; then
    kubectl create configmap "${RELEASE_NAME}-datahub-recipes" -n "$NAMESPACE" \
      "${CM_ARGS_DATAHUB[@]}" \
      --dry-run=client -o yaml | kubectl apply -f -
    echo "✅ DataHub recipes ConfigMap created/updated (${#CM_ARGS_DATAHUB[@]} files)"
  else
    echo "❌  No DataHub recipe files found to add to ConfigMap"
  fi
else
  echo "❌  datahub/recipes directory not found at $SCRIPT_DIR/../datahub/recipes"
fi

# Create DataHub Airbyte source plugin ConfigMap BEFORE Helm deploy so KPO init containers can mount plugin source
echo ""
echo "Creating DataHub Airbyte source ConfigMap from ../datahub_airbyte_source/ (pre-deploy)..."

AIRBYTE_SOURCE_ROOT="$SCRIPT_DIR/../datahub_airbyte_source"
AIRBYTE_SOURCE_PKG="$AIRBYTE_SOURCE_ROOT/datahub_airbyte_source"

if [ -f "$AIRBYTE_SOURCE_ROOT/pyproject.toml" ] && \
   [ -f "$AIRBYTE_SOURCE_PKG/__init__.py" ] && \
   [ -f "$AIRBYTE_SOURCE_PKG/airbyte_source.py" ]; then
  kubectl create configmap "${RELEASE_NAME}-datahub-airbyte-source" -n "$NAMESPACE" \
    --from-file=pyproject.toml="$AIRBYTE_SOURCE_ROOT/pyproject.toml" \
    --from-file=__init__.py="$AIRBYTE_SOURCE_PKG/__init__.py" \
    --from-file=airbyte_source.py="$AIRBYTE_SOURCE_PKG/airbyte_source.py" \
    --dry-run=client -o yaml | kubectl apply -f -
  echo "✅ DataHub Airbyte source ConfigMap created/updated (${RELEASE_NAME}-datahub-airbyte-source)"
else
  echo "❌  Missing one or more required plugin files under $AIRBYTE_SOURCE_ROOT"
  echo "    Required: pyproject.toml, datahub_airbyte_source/__init__.py, datahub_airbyte_source/airbyte_source.py"
fi

# Apply Istio AuthorizationPolicy for cross-namespace traffic
echo ""
echo "Applying Istio AuthorizationPolicy for DataHub access..."

if [ -f "$SCRIPT_DIR/istio-authz-policy.yaml" ]; then
  kubectl apply -f "$SCRIPT_DIR/istio-authz-policy.yaml"
  echo "✅ Istio AuthorizationPolicy applied"
else
  echo "❌  No Istio policy found at $SCRIPT_DIR/istio-authz-policy.yaml, skipping"
fi

# Apply PostgreSQL init scripts ConfigMap (contains schema/extension setup)
# NOTE: ConfigMap is now managed as a Helm template (helm/templates/hydro-postgres-init-configmap.yaml)
# This allows Helm to handle ownership and avoid conflicts
echo ""
echo "❗️ PostgreSQL init ConfigMap will be created by Helm"

# Create temporary values override with rendered service names
cat > /tmp/helm-override.yaml <<EOF
warehouse-postgresql:
  auth:
    password: "${HYDRO_POSTGRES_PASSWORD_VALUE}"
    postgresPassword: "${HYDRO_POSTGRES_PASSWORD_VALUE}"

airflow:
  connections:
    postgres:
      host: "${RELEASE_NAME}-warehouse-postgresql"
      password: "${HYDRO_POSTGRES_PASSWORD_VALUE}"
  data:
    metadataConnection:
      host: "${RELEASE_NAME}-postgresql"
      pass: "${AIRFLOW_DB_PASSWORD_VALUE}"
  config:
    celery:
      result_backend: "db+postgresql://airflow:${AIRFLOW_DB_PASSWORD_VALUE}@${RELEASE_NAME}-postgresql:5432/airflow"
  extraEnvFrom: |
    - secretRef:
        name: datahub-gms-token
    - secretRef:
        name: hydro-db-credentials
  env:
    - name: AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION
      value: "true"
    - name: AIRFLOW__CORE__LOAD_EXAMPLES
      value: "false"
    - name: AIRFLOW__API__SECRET_KEY
      value: "${WEBSERVER_SECRET_KEY}"
    - name: AIRFLOW_CONN_AIRBYTE_DEFAULT
      value: "http://airbyte-airbyte-server-svc.${NAMESPACE}.svc.cluster.local:8001"
    - name: AIRFLOW__DATAHUB__CONN_ID
      value: "datahub_rest"
    - name: AIRFLOW__DATAHUB__TOKEN
      value: "${EFFECTIVE_DATAHUB_TOKEN}"
    - name: DATAHUB_TELEMETRY_ENABLED
      value: "false"
    - name: POSTGRES_HOST
      value: "${RELEASE_NAME}-warehouse-postgresql"
    - name: POSTGRES_PORT
      value: "5432"
    - name: POSTGRES_DB
      value: "hydro"
    - name: DBT_USER
      value: "postgres"
    - name: PATH
      value: "/home/airflow/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/airflow/dbt_venv/bin"
    - name: PYTHONPATH
      value: "/opt/airflow/extra_python_packages"
EOF

# Install with override file
# NOTE: workers.persistence.enabled=true is REQUIRED for LocalExecutor to convert
# scheduler from Deployment to StatefulSet, which enables DNS resolution for log server
if helm list -n "$NAMESPACE" | grep -q "^$RELEASE_NAME\s"; then
    echo "Upgrading existing release..."
    helm upgrade "$RELEASE_NAME" "$SCRIPT_DIR/helm" -n "$NAMESPACE" \
      -f "$SCRIPT_DIR/helm/values.yaml" \
      -f /tmp/helm-override.yaml \
      --set airflow.workers.persistence.enabled=true
else
    echo "Installing new release..."
    helm install "$RELEASE_NAME" "$SCRIPT_DIR/helm" -n "$NAMESPACE" --create-namespace \
      -f "$SCRIPT_DIR/helm/values.yaml" \
      -f /tmp/helm-override.yaml \
      --set airflow.workers.persistence.enabled=true
fi

echo -e "${GREEN}✅ Helm release '$RELEASE_NAME' installed/upgraded${NC}"

# =============================================================================
# DATABASE MIGRATION
# =============================================================================
echo -e "\n${YELLOW}Running database migration to Airflow ${AIRFLOW_VERSION}...${NC}"

# Wait for scheduler rollout to be ready before running migration
echo -e "${YELLOW}Waiting for scheduler deployment rollout...${NC}"
kubectl rollout status deployment/${RELEASE_NAME}-scheduler -n "$NAMESPACE" --timeout=300s || \
  echo -e "${YELLOW}⚠️  Scheduler rollout not complete yet, migration may be handled by Helm job${NC}"

# Check if migration job already ran successfully (Helm handles this)
if kubectl get job -n "$NAMESPACE" "${RELEASE_NAME}-run-airflow-migrations" &>/dev/null; then
    JOB_STATUS=$(kubectl get job -n "$NAMESPACE" "${RELEASE_NAME}-run-airflow-migrations" -o jsonpath='{.status.succeeded}')
    if [ "$JOB_STATUS" = "1" ]; then
        echo -e "${GREEN}✅ Database migration already completed by Helm job${NC}"
    else
        echo -e "${YELLOW}⚠️  Migration job exists but may still be running${NC}"
        kubectl wait --for=condition=complete job/${RELEASE_NAME}-run-airflow-migrations \
          -n "$NAMESPACE" --timeout=300s || true
    fi
else
    echo -e "${YELLOW}ℹ️  Migration handled by Helm chart migrateDatabaseJob${NC}"
fi

# Verify database is healthy
SCHEDULER_POD=$(kubectl get pod -n "$NAMESPACE" -l component=scheduler,release=$RELEASE_NAME -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
if [ -n "$SCHEDULER_POD" ]; then
    echo -e "${YELLOW}Verifying database health...${NC}"
    if kubectl exec -n "$NAMESPACE" "$SCHEDULER_POD" -- airflow db check &>/dev/null; then
        echo -e "${GREEN}✅ Database migration successful and healthy${NC}"
    else
        echo -e "${RED}⚠️  Database health check failed - please investigate${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Scheduler pod not found, skipping health check${NC}"
fi

# =============================================================================
# WEBSERVER SECRET KEY (Airflow 3 requirement for task execution tokens)
# MUST be done AFTER Helm deployment since Helm recreates the secret from values.yaml
# =============================================================================
echo -e "\n${YELLOW}Checking webserver secret key...${NC}"

# Check if secret has the default placeholder value that Helm creates
EXISTING_KEY=$(kubectl get secret airflow-webserver-secret -n "$NAMESPACE" -o jsonpath='{.data.webserver-secret-key}' 2>/dev/null | base64 -d)
if [ "$EXISTING_KEY" = "CHANGE_ME_RANDOM_STRING_32_CHARS" ]; then
    echo -e "${YELLOW}⚠️  Found default placeholder - updating with random key...${NC}"
    kubectl patch secret airflow-webserver-secret -n "$NAMESPACE" \
        --type='json' -p="[{'op': 'replace', 'path': '/data/webserver-secret-key', 'value':'$(echo -n "$WEBSERVER_SECRET_KEY" | base64 -w0)'}]" >/dev/null 2>&1
    echo -e "${GREEN}✅ Webserver secret key updated to random value${NC}"
    
    # Restart scheduler and triggerer to pick up new secret
    echo -e "${YELLOW}Restarting Airflow components to load new secret...${NC}"
    kubectl rollout restart deployment/${RELEASE_NAME}-scheduler -n "$NAMESPACE" >/dev/null 2>&1 || true
    kubectl rollout restart statefulset/${RELEASE_NAME}-triggerer -n "$NAMESPACE" >/dev/null 2>&1 || true
    kubectl rollout restart deployment/${RELEASE_NAME}-api-server -n "$NAMESPACE" >/dev/null 2>&1 || true
    echo -e "${GREEN}✅ Restart initiated - pods will reload with new secret${NC}"
    SECRET_UPDATED=true
elif [ -z "$EXISTING_KEY" ]; then
    echo -e "${RED}❌ Webserver secret not found - deployment may have failed${NC}"
    SECRET_UPDATED=false
else
    echo -e "${GREEN}✅ Webserver secret already has a custom key (${#EXISTING_KEY} chars)${NC}"
    SECRET_UPDATED=false
fi

# =============================================================================
# AIRBYTE INSTALLATION
# =============================================================================
echo ""
echo "Checking if Airbyte should be deployed..."
AIRBYTE_INSTALLED=false
if helm list -n "$NAMESPACE" | grep -q "^airbyte\s"; then
    echo "ℹ️  Airbyte already installed, skipping installation"
    AIRBYTE_INSTALLED=true
else
    echo "Installing Airbyte as separate Helm release..."
    helm repo add airbyte https://airbytehq.github.io/helm-charts >/dev/null 2>&1 || true
    helm repo update airbyte >/dev/null 2>&1
    
    helm install airbyte airbyte/airbyte \
      --namespace "$NAMESPACE" \
        --set global.edition=community \
        --wait --timeout=5m
    
    echo "✅ Airbyte installed"
    AIRBYTE_INSTALLED=true
fi

# Restart Airflow components so:
# 1) scheduler/webserver pick up updated DAGs configmap
# 2) initContainers re-run to install Python deps (e.g. Airbyte provider) into the shared /opt/airflow/.local volume
echo ""
echo "Restarting Airflow pods to pick up DAGs/deps..."
kubectl rollout restart -n "$NAMESPACE" deployment/${RELEASE_NAME}-scheduler deployment/${RELEASE_NAME}-webserver >/dev/null 2>&1 || true
kubectl delete pod -n "$NAMESPACE" -l component=worker >/dev/null 2>&1 || true
kubectl delete pod -n "$NAMESPACE" -l component=triggerer >/dev/null 2>&1 || true
echo "✅ Restart requested"

# Wait for pods
echo ""
echo "Waiting for pods to be ready (this may take 2-5 minutes)..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgresql -n "$NAMESPACE" --timeout=300s
echo "✅ PostgreSQL ready"

kubectl wait --for=condition=ready pod -l component=webserver -n "$NAMESPACE" --timeout=300s || true
echo "✅ Airflow ready"

# Copy dbt project to scheduler pod
echo ""
echo "Copying dbt project to scheduler..."
SCHEDULER_POD=""
for i in {1..30}; do
  SCHEDULER_POD=$(kubectl get pods -n "$NAMESPACE" -l component=scheduler -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
  if [ -n "$SCHEDULER_POD" ]; then
    if kubectl get pod -n "$NAMESPACE" "$SCHEDULER_POD" -o jsonpath='{.status.containerStatuses[?(@.name=="scheduler")].ready}' 2>/dev/null | grep -q true; then
      break
    fi
  fi
  echo "   Waiting for scheduler container to be ready... (attempt $i/30)"
  sleep 5
done
if [ -n "$SCHEDULER_POD" ] && [ -d "$SCRIPT_DIR/../dbt" ]; then
  kubectl cp "$SCRIPT_DIR/../dbt" "$NAMESPACE/$SCHEDULER_POD:/opt/airflow/" --retries=3
  echo "✅ dbt project copied to /opt/airflow/dbt"
else
  echo "❌  Could not copy dbt project (scheduler pod: $SCHEDULER_POD)"
fi

# -----------------------------------------------------------------------------
# Airbyte bootstrap (no UI steps)
# -----------------------------------------------------------------------------

if [ "$AIRBYTE_INSTALLED" = true ]; then
  if [ "${SKIP_AIRBYTE_BOOTSTRAP:-}" = "1" ]; then
    echo "❗️ SKIP_AIRBYTE_BOOTSTRAP=1 set; skipping Airbyte configuration"
  else
    echo ""
    echo "Waiting for Airbyte server to be ready..."
    kubectl wait --for=condition=ready pod \
      -l app.kubernetes.io/instance=airbyte,app.kubernetes.io/name=server \
      -n "$NAMESPACE" --timeout=300s
    echo "✅ Airbyte server pod ready"

    # Wait for Airbyte API to actually be ready (pod ready != API ready)
    echo "Waiting for Airbyte API to be ready..."
    for i in {1..30}; do
      if kubectl exec -n "$NAMESPACE" deploy/airbyte-server -- \
         curl -s -f http://localhost:8001/api/v1/health >/dev/null 2>&1; then
        echo "✅ Airbyte API ready"
        break
      fi
      if [ $i -eq 30 ]; then
        echo "❌ Airbyte API failed to become ready after 60 seconds"
        exit 1
      fi
      echo "   Attempt $i/30: API not ready yet, waiting 2s..."
      sleep 2
    done

    echo ""
    echo "Bootstrapping Airbyte (sources/destination/connections)..."

    if [ ! -f "$SCRIPT_DIR/airbyte_bootstrap.py" ]; then
      echo "❌ Missing $SCRIPT_DIR/airbyte_bootstrap.py"
      exit 1
    fi

    # Run the bootstrap script from a temporary in-cluster Python pod.
    # We avoid running inside airbyte-server because it may not have python3.
    BOOTSTRAP_JSON=""
    for i in {1..3}; do
      echo "   Running Airbyte bootstrap (attempt $i/3)..."
      set +e
      BOOTSTRAP_JSON=$(kubectl -n "$NAMESPACE" run --rm -i --restart=Never hydro-airbyte-bootstrap \
        --image=python:3.12-slim --command -- sh -lc \
        "env AIRBYTE_API_BASE=http://airbyte-airbyte-server-svc:8001/api/v1 \
          AIRBYTE_HTTP_TIMEOUT=180 \
          HYDRO_POSTGRES_HOST=${RELEASE_NAME}-warehouse-postgresql \
          HYDRO_POSTGRES_PORT=5432 \
          HYDRO_POSTGRES_DB=hydro \
          HYDRO_POSTGRES_SCHEMA=raw \
          HYDRO_POSTGRES_USERNAME=postgres \
          HYDRO_POSTGRES_PASSWORD=${HYDRO_POSTGRES_PASSWORD_VALUE} \
          python -" \
        < "$SCRIPT_DIR/airbyte_bootstrap.py")
      STATUS=$?
      set -e
      if [ $STATUS -eq 0 ] && [ -n "$BOOTSTRAP_JSON" ]; then
        break
      fi
      echo "   Airbyte bootstrap failed; retrying in 10s..."
      sleep 10
    done
    if [ -z "$BOOTSTRAP_JSON" ]; then
      echo "❌ Airbyte bootstrap did not return output."
      exit 1
    fi

    # Extract IDs from the single JSON line without jq/python on the host.
    STATIONS_CONNECTION_ID=$(echo "$BOOTSTRAP_JSON" | sed -n 's/.*"stations_connection_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
    READINGS_CONNECTION_ID=$(echo "$BOOTSTRAP_JSON" | sed -n 's/.*"readings_connection_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

    if [ -z "$STATIONS_CONNECTION_ID" ] || [ -z "$READINGS_CONNECTION_ID" ]; then
      echo "❌ Airbyte bootstrap did not return connection IDs. Output was:"
      echo "$BOOTSTRAP_JSON"
      exit 1
    fi

    echo "✅ Airbyte configured"
    echo "   stations_connection_id=$STATIONS_CONNECTION_ID"
    echo "   readings_connection_id=$READINGS_CONNECTION_ID"

    echo ""
    echo "Setting Airflow Variables for Airbyte connection IDs..."
# Wait for scheduler pod to be ready (supports Deployment or StatefulSet)
    SCHEDULER_POD=""
    for i in {1..30}; do
      SCHEDULER_POD=$(kubectl get pods -n "$NAMESPACE" -l component=scheduler -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
      if [ -n "$SCHEDULER_POD" ]; then
        if kubectl get pod -n "$NAMESPACE" "$SCHEDULER_POD" -o jsonpath='{.status.containerStatuses[?(@.name=="scheduler")].ready}' 2>/dev/null | grep -q true; then
          break
        fi
      fi
      echo "   Waiting for scheduler container to be ready... (attempt $i/30)"
      sleep 5
    done
    if [ -z "$SCHEDULER_POD" ]; then
      echo "❌  Scheduler pod not found; cannot set Airflow Variables"
      exit 1
    fi

    airflow_exec_with_retry() {
      local cmd="$1"
      local tries=3
      local status=0
      for attempt in $(seq 1 $tries); do
        set +e
        kubectl exec -n "$NAMESPACE" -c scheduler "$SCHEDULER_POD" -- bash -lc "$cmd"
        status=$?
        set -e
        if [ $status -eq 0 ]; then
          return 0
        fi
        echo "   Airflow CLI command failed (exit=$status), retrying in 10s... (attempt $attempt/$tries)"
        sleep 10
      done
      return $status
    }

    airflow_exec_with_retry "airflow variables set airbyte_stations_connection_id '$STATIONS_CONNECTION_ID'"
    airflow_exec_with_retry "airflow variables set airbyte_readings_connection_id '$READINGS_CONNECTION_ID'"
    echo "✅ Airflow Variables set"

    # Ensure DataHub REST connection uses the current token (avoids 401s)
    if kubectl get secret datahub-gms-token -n "$NAMESPACE" >/dev/null 2>&1; then
      echo "Setting Airflow DataHub connection (datahub_rest)..."
      airflow_exec_with_retry "airflow connections delete datahub_rest >/dev/null 2>&1 || true"
      airflow_exec_with_retry "airflow connections add datahub_rest --conn-type datahub-rest --conn-host datahub-datahub-gms.datahub.svc.cluster.local --conn-port 8080 --conn-password '${EFFECTIVE_DATAHUB_TOKEN}'"
      echo "✅ Airflow DataHub connection updated (type: datahub-rest)"
    else
      echo "⚠️  datahub-gms-token secret not found; skipping DataHub connection update"
    fi
  fi
fi

# Note: dbt project is now deployed via ConfigMap (see dbt-configmap above)
# Init containers automatically copy dbt files from ConfigMap to /opt/airflow/dbt
# This persists across pod restarts, unlike kubectl cp
echo ""
echo "ℹ️  dbt project deployed via ConfigMap and init containers"

# Show status
echo ""
echo "Deployment Status:"
kubectl get pods -n "$NAMESPACE"

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access Airflow UI:"
echo "   kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME-api-server 8080:8080"
echo "   Then open: http://localhost:8080"
echo "   Default login: admin / admin"
echo ""

# Show Airbyte instructions if installed
if helm list -n "$NAMESPACE" | grep -q "^airbyte\s"; then
    echo "🌐 Access Airbyte UI:"
  echo "   kubectl port-forward -n $NAMESPACE svc/airbyte-airbyte-webapp-svc 8000:80"
    echo "   Then open: http://localhost:8000 (user: airbyte / password: password)"
    echo ""
fi

echo " Next steps:"
echo "   # DAGs and dbt project are automatically deployed via ConfigMaps"
echo "   # Airflow connections are configured via environment variables"
echo ""
echo " View logs:"
echo "   kubectl logs -n $NAMESPACE -l component=scheduler -f"
echo ""
echo " Check status:"
echo "   kubectl get all -n $NAMESPACE"
