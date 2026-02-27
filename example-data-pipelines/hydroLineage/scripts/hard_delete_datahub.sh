#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

# Hard delete all HydroLineage metadata from DataHub using CLI
# Method: Uses DataHub CLI in a temporary Kubernetes pod with direct cluster access
# This performs permanent deletion (not soft delete)

set -e

echo "=== Hard Delete DataHub Metadata ==="
echo
echo "Method: Running DataHub CLI in temporary pod with K8s service DNS access"
echo "DataHub GMS: datahub-datahub-gms.datahub.svc.cluster.local:8080"
echo

# Get DataHub token from K8s secret
echo "Getting DataHub token from K8s secret..."
DATAHUB_TOKEN=$(kubectl get secret datahub-gms-token -n hydro-lineage -o jsonpath='{.data.DATAHUB_GMS_TOKEN}' | base64 -d)

if [ -z "$DATAHUB_TOKEN" ]; then
    echo "Error: Could not retrieve DataHub token from secret"
    exit 1
fi

echo "Creating temporary pod and running cleanup..."
echo

# Run cleanup in temporary pod
# Uses python:3.11-slim image, installs DataHub CLI, and deletes all platforms
kubectl run datahub-cli-temp --rm -i --restart=Never \
    --image=python:3.11-slim \
    -n hydro-lineage \
    --env="DATAHUB_GMS_TOKEN=$DATAHUB_TOKEN" \
    -- bash -c "
set -e
pip install --quiet 'acryl-datahub[datahub-rest]'
export DATAHUB_GMS_URL='http://datahub-datahub-gms.datahub.svc.cluster.local:8080'

echo 'Hard deleting Airflow platform entities...'
datahub delete --platform airflow --hard --force

# echo 'Hard deleting PostgreSQL platform entities...'
datahub delete --platform postgres --hard --force

# echo 'Hard deleting dbt platform entities...'
datahub delete --platform dbt --hard --force

# echo 'Hard deleting Airbyte platform entities...'
datahub delete --platform airbyte --hard --force || echo 'No Airbyte entities found'

echo ''
echo 'Cleanup complete!'
"

echo
echo "=== Done ==="
echo "Refresh your DataHub UI (Ctrl+Shift+R) to see the changes."
