<!--
SPDX-License-Identifier: Apache-2.0

© Crown Copyright 2025. This work has been developed by the National Digital Twin
Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
entity
-->

# 🌊 HydroLineage

Example data pipeline for UK flood monitoring data.

Pipeline: UK Flood API → Airflow → PostgreSQL (`raw`) → dbt (`staging`/`analytics`) → DataHub lineage.

---

## ⚠️ Assumptions

This example assumes the following are already in place before running `k8s/deploy.sh`:

- A working Kubernetes cluster with `kubectl` access from your environment
- A reachable DataHub data catalogue deployment (typically DataHub GMS) in your target environment
- A valid DataHub access token exported as `DATAHUB_GMS_TOKEN`
- Helm installed and able to deploy into your target Kubernetes namespace

Quick verification checklist:

```bash
# Kubernetes access
kubectl cluster-info

# Helm availability
helm version

# DataHub token present
test -n "$DATAHUB_GMS_TOKEN" && echo "DATAHUB_GMS_TOKEN is set"

# Optional: DataHub GMS connectivity (set URL first)
export DATAHUB_GMS_URL='https://your-datahub-gms-url'
curl -sSf "$DATAHUB_GMS_URL/config" >/dev/null && echo "DataHub GMS reachable"
```

---

## 🚀 Quick Start (Kubernetes)

```bash
cd k8s

# Required
export DATAHUB_GMS_TOKEN='your-datahub-token'

# Recommended (avoid defaults)
export HYDRO_POSTGRES_PASSWORD='your-warehouse-password'
export AIRFLOW_DB_PASSWORD='your-airflow-metadata-password'

./deploy.sh
```

Access Airflow UI:

```bash
kubectl port-forward -n hydro-lineage svc/airflow-lineage-airflow-webserver 8080:8080
```

Open http://localhost:8080 (`admin` / `admin` unless changed in Helm values).

---

## ✅ What `k8s/deploy.sh` configures

- Namespace, secrets, and runtime overrides
- Airflow + PostgreSQL + Redis (Helm)
- DAG/dbt/DataHub recipe ConfigMaps
- Airbyte bootstrap and Airflow Variables/Connections
- DataHub integration wiring
