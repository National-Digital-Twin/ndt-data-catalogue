# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

"""Azure Data Factory DataHub connector.

This package provides a connector to ingest metadata from Azure Data Factory
into DataHub, including:

- Data Factories as Containers
- Pipelines as DataFlows
- Activities as DataJobs
- Dataset lineage
- Execution history (optional)

Usage:
    source:
      type: azure_data_factory
      config:
        subscription_id: ${AZURE_SUBSCRIPTION_ID}
        credential:
          authentication_method: service_principal
          client_id: ${AZURE_CLIENT_ID}
          client_secret: ${AZURE_CLIENT_SECRET}
          tenant_id: ${AZURE_TENANT_ID}
"""
