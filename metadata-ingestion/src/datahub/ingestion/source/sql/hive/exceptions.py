# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

"""Common exceptions for Hive sources"""


class HiveSourceError(Exception):
    """Base exception for Hive source errors"""

    pass


class InvalidDatasetIdentifierError(HiveSourceError, ValueError):
    """Raised when a dataset identifier cannot be parsed into database/schema"""

    pass
