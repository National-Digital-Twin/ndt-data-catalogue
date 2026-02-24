# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

"""Report class for SQL Analytics Endpoint schema extraction."""

from dataclasses import dataclass


@dataclass
class SqlAnalyticsEndpointReport:
    """Report for SQL Analytics Endpoint schema extraction operations."""

    successes: int = 0
    failures: int = 0
    skipped: int = 0
