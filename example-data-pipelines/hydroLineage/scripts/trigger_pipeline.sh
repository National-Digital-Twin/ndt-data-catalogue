#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

# Quick script to trigger the end-to-end pipeline

set -e

echo "=========================================="
echo "HydroLineage End-to-End Pipeline Trigger"
echo "=========================================="
echo ""

# Check if Airflow is accessible
echo "1. Checking Airflow scheduler..."
if kubectl get pods -n hydro-lineage | grep -q "airflow-lineage-scheduler.*Running"; then
    echo "   ✅ Airflow scheduler is running"
else
    echo "   ❌ Airflow scheduler is not running"
    echo "   Run: cd k8s && ./deploy.sh"
    exit 1
fi

# Trigger the DAG
echo ""
echo "2. Triggering pipeline DAG..."
kubectl exec -n hydro-lineage deployment/airflow-lineage-scheduler -- \
    airflow dags trigger hydro_end_to_end_pipeline

echo ""
echo "   ✅ Pipeline triggered!"
echo ""

# Wait a moment for the run to register
sleep 3

# Get latest run ID
echo "3. Checking DAG run status..."
RUN_ID=$(kubectl exec -n hydro-lineage deployment/airflow-lineage-scheduler -- \
    airflow dags list-runs -d hydro_end_to_end_pipeline --state running --output json 2>/dev/null | \
    jq -r '.[0].run_id' 2>/dev/null || echo "unknown")

if [ "$RUN_ID" != "unknown" ] && [ "$RUN_ID" != "null" ]; then
    echo "   ✅ Run ID: $RUN_ID"
else
    echo "   ⏳ Run starting (check Airflow UI)"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Monitor in Airflow UI:"
echo "   kubectl port-forward -n hydro-lineage svc/airflow-lineage-webserver 8080:8080"
echo "   Open: http://localhost:8080"
echo ""
echo "2. View logs for specific task:"
echo "   kubectl exec -n hydro-lineage deployment/airflow-lineage-scheduler -- \\"
echo "     airflow tasks logs hydro_end_to_end_pipeline <task_id> <run_id>"
echo ""
echo "3. Check pipeline progress:"
echo "   watch kubectl exec -n hydro-lineage deployment/airflow-lineage-scheduler -- \\"
echo "     airflow dags list-runs -d hydro_end_to_end_pipeline"
echo ""
echo "Pipeline will complete in ~5 minutes."
echo "=========================================="
