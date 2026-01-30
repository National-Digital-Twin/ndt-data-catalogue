# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

# Inlined from metadata-ingestion/examples/library/search_documents.py
"""Example: Searching documents using the DataHub SDK.

This example demonstrates how to search for documents using the DataHub SDK.
"""

from datahub.sdk import DataHubClient, FilterDsl

# Initialize the client
client = DataHubClient.from_env()

# ============================================================================
# Example 1: Search for all documents
# ============================================================================
# Use get_urns with entity type filter to find documents
document_urns = client.search.get_urns(
    filter=FilterDsl.entity_type("document"),
)

print("All documents:")
for urn in document_urns:
    print(f"  - {urn}")

# ============================================================================
# Example 2: Search with a text query
# ============================================================================
# Search for documents matching "data quality"
document_urns = client.search.get_urns(
    query="data quality",
    filter=FilterDsl.entity_type("document"),
)

print("\nDocuments matching 'data quality':")
for urn in document_urns:
    print(f"  - {urn}")

# ============================================================================
# Example 3: Search within a specific domain
# ============================================================================
document_urns = client.search.get_urns(
    filter=FilterDsl.and_(
        FilterDsl.entity_type("document"),
        FilterDsl.domain("urn:li:domain:engineering"),
    ),
)

print("\nDocuments in engineering domain:")
for urn in document_urns:
    print(f"  - {urn}")

# ============================================================================
# Example 4: Search with tags
# ============================================================================
document_urns = client.search.get_urns(
    filter=FilterDsl.and_(
        FilterDsl.entity_type("document"),
        FilterDsl.tag("urn:li:tag:important"),
    ),
)

print("\nDocuments with 'important' tag:")
for urn in document_urns:
    print(f"  - {urn}")
