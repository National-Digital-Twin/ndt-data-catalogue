#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

#
# Cleanup Airbyte Metadata from DataHub
# Removes all Airbyte-related datasets, pipelines (DataFlows), and tasks (DataJobs)
#

set -e

DATAHUB_GMS_URL="http://datahub-datahub-gms.datahub.svc.cluster.local:8080"
DATAHUB_TOKEN="${DATAHUB_GMS_TOKEN:-$(kubectl get secret datahub-gms-token -n hydro-lineage -o jsonpath='{.data.DATAHUB_GMS_TOKEN}' | base64 -d)}"

if [ -z "$DATAHUB_TOKEN" ]; then
  echo "❌ DATAHUB_GMS_TOKEN not set and could not retrieve from secret"
  exit 1
fi

echo "🧹 Cleaning up Airbyte metadata from DataHub..."
echo "Target: $DATAHUB_GMS_URL"
echo ""

# Function to execute GraphQL queries
graphql_query() {
  local query="$1"
  kubectl run --rm -i --restart=Never datahub-cleanup-$(date +%s) \
    --image=curlimages/curl:latest \
    --namespace=hydro-lineage \
    --command -- sh -c "
      curl -s -X POST '$DATAHUB_GMS_URL/api/graphql' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer $DATAHUB_TOKEN' \
        -d '$query'
    "
}

# =============================================================================
# 1. Delete Airbyte Datasets
# =============================================================================
echo "📊 Fetching Airbyte datasets..."

DATASETS_QUERY=$(cat <<'EOF'
{
  "query": "query { search(input: { type: DATASET, query: \"*\", start: 0, count: 1000, filters: [{ field: \"platform\", values: [\"airbyte\"] }] }) { total searchResults { entity { urn } } } }"
}
EOF
)

DATASETS_RESULT=$(graphql_query "$DATASETS_QUERY")
DATASET_URNS=$(echo "$DATASETS_RESULT" | grep -o 'urn:li:dataset:[^"]*' || echo "")
DATASET_COUNT=$(echo "$DATASET_URNS" | grep -c '^urn' || echo 0)

echo "Found $DATASET_COUNT Airbyte datasets"

if [ "$DATASET_COUNT" -gt 0 ]; then
  echo "Deleting Airbyte datasets..."
  while IFS= read -r urn; do
    if [ -n "$urn" ]; then
      echo "  - $urn"
      DELETE_QUERY=$(cat <<EOF
{
  "query": "mutation { updateDataset(urn: \\\"$urn\\\", input: { status: { removed: true } }) }"
}
EOF
)
      graphql_query "$DELETE_QUERY" > /dev/null
    fi
  done <<< "$DATASET_URNS"
  echo "✅ Deleted $DATASET_COUNT datasets"
else
  echo "✅ No Airbyte datasets found"
fi

# =============================================================================
# 2. Delete Airbyte DataFlows (Pipelines)
# =============================================================================
echo ""
echo "🔄 Fetching Airbyte pipelines (DataFlows)..."

DATAFLOWS_QUERY=$(cat <<'EOF'
{
  "query": "query { search(input: { type: DATA_FLOW, query: \"*\", start: 0, count: 1000 }) { total searchResults { entity { urn } } } }"
}
EOF
)

DATAFLOWS_RESULT=$(graphql_query "$DATAFLOWS_QUERY")
DATAFLOW_URNS=$(echo "$DATAFLOWS_RESULT" | grep -o 'urn:li:dataFlow:[^"]*' | grep -i airbyte || echo "")
DATAFLOW_COUNT=$(echo "$DATAFLOW_URNS" | grep -c '^urn' || echo 0)

echo "Found $DATAFLOW_COUNT Airbyte DataFlows"

if [ "$DATAFLOW_COUNT" -gt 0 ]; then
  echo "Deleting Airbyte DataFlows..."
  while IFS= read -r urn; do
    if [ -n "$urn" ]; then
      echo "  - $urn"
      DELETE_QUERY=$(cat <<EOF
{
  "query": "mutation { updateDataFlow(urn: \\\"$urn\\\", input: { status: { removed: true } }) }"
}
EOF
)
      graphql_query "$DELETE_QUERY" > /dev/null
    fi
  done <<< "$DATAFLOW_URNS"
  echo "✅ Deleted $DATAFLOW_COUNT DataFlows"
else
  echo "✅ No Airbyte DataFlows found"
fi

# =============================================================================
# 3. Delete Airbyte DataJobs (Tasks)
# =============================================================================
echo ""
echo "⚙️  Fetching Airbyte tasks (DataJobs)..."

DATAJOBS_QUERY=$(cat <<'EOF'
{
  "query": "query { search(input: { type: DATA_JOB, query: \"*\", start: 0, count: 1000 }) { total searchResults { entity { urn } } } }"
}
EOF
)

DATAJOBS_RESULT=$(graphql_query "$DATAJOBS_QUERY")
DATAJOB_URNS=$(echo "$DATAJOBS_RESULT" | grep -o 'urn:li:dataJob:[^"]*' | grep -i airbyte || echo "")
DATAJOB_COUNT=$(echo "$DATAJOB_URNS" | grep -c '^urn' || echo 0)

echo "Found $DATAJOB_COUNT Airbyte DataJobs"

if [ "$DATAJOB_COUNT" -gt 0 ]; then
  echo "Deleting Airbyte DataJobs..."
  while IFS= read -r urn; do
    if [ -n "$urn" ]; then
      echo "  - $urn"
      DELETE_QUERY=$(cat <<EOF
{
  "query": "mutation { updateDataJob(urn: \\\"$urn\\\", input: { status: { removed: true } }) }"
}
EOF
)
      graphql_query "$DELETE_QUERY" > /dev/null
    fi
  done <<< "$DATAJOB_URNS"
  echo "✅ Deleted $DATAJOB_COUNT DataJobs"
else
  echo "✅ No Airbyte DataJobs found"
fi

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "=============================="
echo "🎉 Cleanup Complete!"
echo "=============================="
echo "Deleted:"
echo "  - $DATASET_COUNT Airbyte datasets"
echo "  - $DATAFLOW_COUNT Airbyte DataFlows (pipelines)"
echo "  - $DATAJOB_COUNT Airbyte DataJobs (tasks)"
echo ""
echo "💡 Next steps:"
echo "  1. Run your hydro_airbyte_pipeline DAG"
echo "  2. Airflow DataHub plugin will capture proper lineage"
echo "  3. View lineage in DataHub UI at http://localhost:8081"
echo ""
