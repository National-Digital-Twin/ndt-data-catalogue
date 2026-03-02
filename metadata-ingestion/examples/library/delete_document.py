# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

# Inlined from metadata-ingestion/examples/library/delete_document.py
"""Example: Deleting documents using the DataHub SDK.

This example demonstrates how to delete documents from DataHub.
"""

from datahub.metadata.urns import DocumentUrn
from datahub.sdk import DataHubClient

# Initialize the client
client = DataHubClient.from_env()

# ============================================================================
# Example 1: Delete a document by URN
# ============================================================================
doc_urn = DocumentUrn("my-tutorial-doc")

# First check if it exists
doc = client.entities.get(doc_urn)

if doc:
    # Delete the document
    client.entities.delete(str(doc_urn))
    print(f"Document deleted: {doc_urn}")
else:
    print(f"Document not found: {doc_urn}")

# ============================================================================
# Example 2: Delete multiple documents
# ============================================================================
doc_ids_to_delete = [
    "doc-1",
    "doc-2",
    "doc-3",
]

for doc_id in doc_ids_to_delete:
    doc_urn = DocumentUrn(doc_id)
    doc = client.entities.get(doc_urn)
    if doc:
        client.entities.delete(str(doc_urn))
        print(f"Deleted: {doc_urn}")
    else:
        print(f"Not found (skipping): {doc_urn}")

print("Cleanup complete!")
