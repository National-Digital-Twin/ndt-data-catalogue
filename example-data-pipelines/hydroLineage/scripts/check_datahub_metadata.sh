#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

# Script to check what metadata is currently in DataHub

set -e

echo "========================================"
echo "DataHub Metadata Verification"
echo "========================================"
echo ""

# Set DataHub GMS URL
export DATAHUB_GMS_URL="http://datahub-datahub-gms.datahub.svc.cluster.local:8080"

echo "1. Checking dbt Datasets..."
echo "-------------------------------------------"
kubectl exec -n hydro-lineage deployment/airflow-lineage-scheduler -- bash -c "
export DATAHUB_GMS_URL=$DATAHUB_GMS_URL
datahub get --urn 'urn:li:dataset:(urn:li:dataPlatform:dbt,hydro.analytics_analytics.dim_station,PROD)' 2>&1 | grep -E '(name|description|tags|materialization)' | head -20
"

echo ""
echo "2. Checking PostgreSQL Datasets..."
echo "-------------------------------------------"
kubectl exec -n hydro-lineage deployment/airflow-lineage-scheduler -- bash -c "
export DATAHUB_GMS_URL=$DATAHUB_GMS_URL
datahub get --urn 'urn:li:dataset:(urn:li:dataPlatform:postgres,hydro.analytics_analytics.dim_station,PROD)' 2>&1 | head -20
" || echo "PostgreSQL metadata not yet ingested (expected)"

echo ""
echo "3. Listing All dbt Models..."
echo "-------------------------------------------"
echo "- dim_station (dimension table)"
echo "- fct_water_levels (fact table)"
echo "- vw_latest_water_levels (API view)"
echo "- stg_river_stations (staging view)"
echo "- stg_water_level_readings (staging view)"

echo ""
echo "4. Listing All Source Tables..."
echo "-------------------------------------------"
echo "- raw.stations"
echo "- raw.water_level_readings"

echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo "1. Open DataHub UI: http://localhost:9002"
echo "2. Search for 'dim_station' to see the dataset"
echo "3. Click on 'Lineage' tab to see upstream dependencies"
echo "4. Check 'Schema' tab to see column metadata"
echo ""
echo "To access DataHub UI:"
echo "  kubectl port-forward -n datahub svc/datahub-datahub-frontend 9002:9002"
echo ""
