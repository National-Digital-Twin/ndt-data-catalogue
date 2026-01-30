# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

"""
Shims for legacy openlineage-airflow package.
This module is used when openlineage-airflow is installed (Airflow 2.x with legacy OpenLineage).
"""

from openlineage.airflow.listener import TaskHolder
from openlineage.airflow.plugin import OpenLineagePlugin
from openlineage.airflow.utils import (
    get_operator_class,
    redact_with_exclusions,
    try_import_from_string,
)

__all__ = [
    "TaskHolder",
    "OpenLineagePlugin",
    "get_operator_class",
    "redact_with_exclusions",
    "try_import_from_string",
]
