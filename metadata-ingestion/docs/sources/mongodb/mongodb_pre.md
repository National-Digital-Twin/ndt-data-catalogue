<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

## Prerequisites and Permissions

**Important:**  
The user account used for MongoDB ingestion must have the `readWrite` role on each database to be ingested. Schema inference and sampling logic executes on system collections (such as `system.profile` and `system.views`), which are not permitted with only `read` or `readAnyDatabase` roles. Without `readWrite`, ingestion will fail with an authorization error.
