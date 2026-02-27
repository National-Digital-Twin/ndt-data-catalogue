#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

"""
DataHub Metadata Cleanup - Reference Implementation

This file documents the SUCCESSFUL method for cleaning DataHub metadata.

METHOD THAT WORKS:
==================
Use DataHub CLI (acryl-datahub) with --hard --force flags in a temporary Kubernetes pod.

Why this method works:
1. Direct K8s service DNS access (no port-forwarding needed)
2. CLI handles pagination and batch deletion automatically
3. Hard delete (--hard) removes entities permanently vs soft delete
4. Force flag (--force) skips confirmation prompts

Command:
--------
DATAHUB_TOKEN=$(kubectl get secret datahub-gms-token -n hydro-lineage -o jsonpath='{.data.DATAHUB_GMS_TOKEN}' | base64 -d)

kubectl run datahub-cli-temp --rm -i --restart=Never \\
    --image=python:3.11-slim -n hydro-lineage \\
    --env="DATAHUB_GMS_TOKEN=$DATAHUB_TOKEN" -- bash -c "
pip install --quiet 'acryl-datahub[datahub-rest]'
export DATAHUB_GMS_URL='http://datahub-datahub-gms.datahub.svc.cluster.local:8080'
datahub delete --platform airflow --hard --force
datahub delete --platform postgres --hard --force
datahub delete --platform dbt --hard --force
datahub delete --platform airbyte --hard --force
"

Results (Jan 29, 2026):
-----------------------
- Airflow: 49 entities deleted (4 dataFlows + 45 dataJobs)
- PostgreSQL: 8 datasets deleted
- dbt: 8 datasets deleted
- Total: 65 entities, 752 versioned rows removed in ~5 seconds

Alternative GraphQL Method (Kept for Reference):
=================================================
The GraphQL API can be used for more granular control, but has issues:
- Requires careful error handling for pagination
- Search API may not return all entities
- Soft delete only (entities can be restored)

For production use, prefer the CLI method above or use hard_delete_datahub.sh script.
"""

import os
import sys

def print_usage():
    print(__doc__)
    print("\nFor actual cleanup, use: ./scripts/hard_delete_datahub.sh")
    print("Or run the command documented above directly.")

if __name__ == "__main__":
    print_usage()
    sys.exit(0)

HEADERS = {
    "Authorization": f"Bearer {DATAHUB_GMS_TOKEN}",
    "Content-Type": "application/json"
}

def execute_graphql(query: str, variables: Dict[str, Any] = None) -> Dict:
    """Execute a GraphQL query against DataHub"""
    response = requests.post(
        f"{DATAHUB_GMS_URL}/api/graphql",
        headers=HEADERS,
        json={"query": query, "variables": variables or {}}
    )
    
    if response.status_code != 200:
        print(f"Error: GraphQL request failed with status {response.status_code}")
        print(f"Response: {response.text}")
        return None
    
    return response.json()

def search_entities(entity_type: str, platform: str = None) -> List[str]:
    """Search for entities by type and optionally platform"""
    query = """
    query searchEntities($input: SearchInput!) {
        search(input: $input) {
            total
            searchResults {
                entity {
                    urn
                    type
                }
            }
        }
    }
    """
    
    search_query = f"platform:{platform}" if platform else "*"
    
    variables = {
        "input": {
            "type": entity_type.upper(),
            "query": search_query,
            "start": 0,
            "count": 1000
        }
    }
    
    result = execute_graphql(query, variables)
    if not result:
        print(f"Warning: Failed to search for {entity_type} entities")
        return []
    
    if "data" not in result or not result.get("data"):
        print(f"Warning: No data in response for {entity_type}")
        return []
    
    search_data = result["data"].get("search")
    if not search_data:
        print(f"Warning: No search results for {entity_type}")
        return []
    
    search_results = search_data.get("searchResults", [])
    urns = [r["entity"]["urn"] for r in search_results]
    print(f"Found {len(urns)} {entity_type} entities for platform {platform or 'all'}")
    return urns

def delete_entity(urn: str) -> bool:
    """Delete a single entity by URN"""
    query = """
    mutation batchUpdateSoftDeleted($input: BatchUpdateSoftDeletedInput!) {
        batchUpdateSoftDeleted(input: $input)
    }
    """
    
    variables = {
        "input": {
            "urns": [urn],
            "deleted": True
        }
    }
    
    result = execute_graphql(query, variables)
    return result is not None and "data" in result

def delete_entities_bulk(urns: List[str], batch_size: int = 50) -> int:
    """Delete multiple entities in batches"""
    deleted_count = 0
    
    for i in range(0, len(urns), batch_size):
        batch = urns[i:i + batch_size]
        
        query = """
        mutation batchUpdateSoftDeleted($input: BatchUpdateSoftDeletedInput!) {
            batchUpdateSoftDeleted(input: $input)
        }
        """
        
        variables = {
            "input": {
                "urns": batch,
                "deleted": True
            }
        }
        
        result = execute_graphql(query, variables)
        if result and "data" in result:
            deleted_count += len(batch)
            print(f"Deleted batch of {len(batch)} entities ({deleted_count}/{len(urns)})")
        else:
            print(f"Failed to delete batch starting at index {i}")
    
    return deleted_count

def main():
    print("=== DataHub Metadata Cleanup (Python) ===\n")
    
    # 1. Delete PostgreSQL datasets
    print("Step 1: Deleting PostgreSQL metadata...")
    postgres_urns = search_entities("dataset", "postgres")
    if postgres_urns:
        deleted = delete_entities_bulk(postgres_urns)
        print(f"Deleted {deleted} PostgreSQL datasets\n")
    else:
        print("No PostgreSQL datasets found\n")
    
    # 2. Delete dbt datasets
    print("Step 2: Deleting dbt metadata...")
    dbt_urns = search_entities("dataset", "dbt")
    if dbt_urns:
        deleted = delete_entities_bulk(dbt_urns)
        print(f"Deleted {deleted} dbt datasets\n")
    else:
        print("No dbt datasets found\n")
    
    # 3. Delete Airbyte datasets
    print("Step 3: Deleting Airbyte metadata...")
    airbyte_datasets = search_entities("dataset", "airbyte")
    airbyte_flows = search_entities("dataflow", "airbyte")
    airbyte_jobs = search_entities("datajob", "airbyte")
    
    all_airbyte = airbyte_datasets + airbyte_flows + airbyte_jobs
    if all_airbyte:
        deleted = delete_entities_bulk(all_airbyte)
        print(f"Deleted {deleted} Airbyte entities\n")
    else:
        print("No Airbyte entities found\n")
    
    # 4. Delete Airflow metadata
    print("Step 4: Deleting Airflow metadata...")
    airflow_flows = search_entities("dataflow", "airflow")
    airflow_jobs = search_entities("datajob", "airflow")
    
    all_airflow = airflow_flows + airflow_jobs
    if all_airflow:
        deleted = delete_entities_bulk(all_airflow)
        print(f"Deleted {deleted} Airflow entities\n")
    else:
        print("No Airflow entities found\n")
    
    print("=== Cleanup Complete ===")
    print("Note: Soft-deleted entities can be restored from the UI if needed")
    print("It may take a few minutes for changes to reflect in the DataHub UI")

if __name__ == "__main__":
    main()
