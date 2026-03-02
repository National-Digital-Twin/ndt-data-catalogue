# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

"""DataHub Documents Source - Process Document entities and generate embeddings."""

from datahub.ingestion.source.datahub_documents.datahub_documents_config import (
    DataHubDocumentsSourceConfig,
)
from datahub.ingestion.source.datahub_documents.datahub_documents_source import (
    DataHubDocumentsSource,
)

__all__ = ["DataHubDocumentsSource", "DataHubDocumentsSourceConfig"]
