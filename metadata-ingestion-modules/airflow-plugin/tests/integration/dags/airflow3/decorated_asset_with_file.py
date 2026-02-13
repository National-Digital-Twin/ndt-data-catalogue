# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

"""Test DAG for @asset decorator with explicit file:// URI.

This demonstrates @asset with an explicit URI using the file:// scheme.
The path must be valid (parent directory must exist).

DataHub should capture this as:
urn:li:dataset:(urn:li:dataPlatform:file,tmp/decorated_asset_output.txt,PROD)
"""

from airflow.sdk import asset


@asset(uri="file:///tmp/decorated_asset_output.txt", schedule=None)
def decorated_asset_with_file():
    """Produce an asset with an explicit file:// URI."""
    return "data written to file"
