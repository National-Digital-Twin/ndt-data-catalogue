#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

# Script to remove HydroLineage metadata from DataHub
# This will delete Airflow, dbt, and PostgreSQL metadata

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== DataHub Metadata Cleanup Script ===${NC}"
echo

# Check if DataHub GMS token is set
if [ -z "$DATAHUB_GMS_TOKEN" ]; then
    echo -e "${RED}Error: DATAHUB_GMS_TOKEN environment variable not set${NC}"
    echo "Please set it with: export DATAHUB_GMS_TOKEN='your-token-here'"
    exit 1
fi

# Set DataHub GMS URL (K8s service or localhost if port-forwarded)
DATAHUB_GMS_URL="${DATAHUB_GMS_URL:-http://datahub-datahub-gms.datahub.svc.cluster.local:8080}"
echo -e "${GREEN}Using DataHub GMS URL: $DATAHUB_GMS_URL${NC}"
echo

# Function to delete entities by platform
delete_by_platform() {
    local platform=$1
    local entity_type=$2
    
    echo -e "${YELLOW}Deleting $entity_type entities from platform: $platform${NC}"
    
    datahub delete --platform $platform --entity-type $entity_type --force || {
        echo -e "${YELLOW}Warning: Failed to delete some $entity_type entities from $platform (may not exist)${NC}"
    }
}

# Function to delete entities by URN pattern
delete_by_urn_pattern() {
    local urn_pattern=$1
    
    echo -e "${YELLOW}Deleting entities matching URN pattern: $urn_pattern${NC}"
    
    datahub delete --urn "$urn_pattern" --force || {
        echo -e "${YELLOW}Warning: Failed to delete entities matching $urn_pattern (may not exist)${NC}"
    }
}

echo -e "${GREEN}Step 1: Deleting PostgreSQL metadata${NC}"
delete_by_platform "postgres" "dataset"
echo

echo -e "${GREEN}Step 2: Deleting dbt metadata${NC}"
delete_by_platform "dbt" "dataset"
echo

echo -e "${GREEN}Step 3: Deleting Airbyte metadata${NC}"
delete_by_platform "airbyte" "dataset"
delete_by_platform "airbyte" "dataFlow"
delete_by_platform "airbyte" "dataJob"
echo

echo -e "${GREEN}Step 4: Deleting Airflow DAG metadata${NC}"
delete_by_platform "airflow" "dataFlow"
delete_by_platform "airflow" "dataJob"
delete_by_platform "airflow" "dataProcessInstance"
echo

echo -e "${GREEN}Step 5: Cleaning up specific HydroLineage datasets${NC}"
# Delete specific datasets by URN if needed
# Examples:
# delete_by_urn_pattern "urn:li:dataset:(urn:li:dataPlatform:postgres,hydro.raw.*,PROD)"
# delete_by_urn_pattern "urn:li:dataset:(urn:li:dataPlatform:dbt,hydro.*,PROD)"

echo -e "${GREEN}Step 6: Deleting custom tags${NC}"
datahub delete --urn "urn:li:tag:HydroLineage" --force || echo -e "${YELLOW}Warning: HydroLineage tag not found${NC}"
datahub delete --urn "urn:li:tag:Airbyte" --force || echo -e "${YELLOW}Warning: Airbyte tag not found${NC}"
datahub delete --urn "urn:li:tag:Ingestion" --force || echo -e "${YELLOW}Warning: Ingestion tag not found${NC}"
datahub delete --urn "urn:li:tag:dbt" --force || echo -e "${YELLOW}Warning: dbt tag not found${NC}"
datahub delete --urn "urn:li:tag:Analytics" --force || echo -e "${YELLOW}Warning: Analytics tag not found${NC}"
datahub delete --urn "urn:li:tag:Staging" --force || echo -e "${YELLOW}Warning: Staging tag not found${NC}"
datahub delete --urn "urn:li:tag:Core" --force || echo -e "${YELLOW}Warning: Core tag not found${NC}"
echo

echo -e "${GREEN}=== Cleanup Complete ===${NC}"
echo -e "${YELLOW}Note: It may take a few minutes for changes to reflect in the DataHub UI${NC}"
echo -e "${YELLOW}You may need to refresh your browser to see the changes${NC}"
