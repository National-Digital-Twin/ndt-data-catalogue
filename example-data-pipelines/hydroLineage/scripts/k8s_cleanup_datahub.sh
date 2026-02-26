#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

# Helper script to run DataHub cleanup from within Kubernetes cluster
# This script executes the cleanup from the Airflow scheduler pod

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Running DataHub Cleanup from K8s ===${NC}\n"

# Check if DataHub token is available
if ! kubectl get secret datahub-gms-token -n hydro-lineage &>/dev/null; then
    echo -e "${YELLOW}Warning: datahub-gms-token secret not found in hydro-lineage namespace${NC}"
    echo "Please create it first or provide DATAHUB_GMS_TOKEN environment variable"
fi

# Get the token from the secret
DATAHUB_TOKEN=$(kubectl get secret datahub-gms-token -n hydro-lineage -o jsonpath='{.data.DATAHUB_GMS_TOKEN}' | base64 -d)

echo -e "${GREEN}Copying cleanup script to Airflow scheduler pod...${NC}"
kubectl cp scripts/cleanup_datahub_metadata.py \
    hydro-lineage/airflow-lineage-scheduler-0:/tmp/cleanup_datahub_metadata.py

echo -e "${GREEN}Installing requests library if needed...${NC}"
kubectl exec -n hydro-lineage airflow-lineage-scheduler-0 -- \
    pip install --quiet requests 2>/dev/null || true

echo -e "${GREEN}Running cleanup script...${NC}"
kubectl exec -n hydro-lineage airflow-lineage-scheduler-0 -- \
    bash -c "export DATAHUB_GMS_TOKEN='$DATAHUB_TOKEN' && python /tmp/cleanup_datahub_metadata.py"

echo -e "\n${GREEN}Cleanup script execution completed!${NC}"
echo -e "${YELLOW}Note: Check the output above for results${NC}"
