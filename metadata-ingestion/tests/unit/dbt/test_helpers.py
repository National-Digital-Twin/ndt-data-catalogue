# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

from unittest import mock


def create_mock_dbt_node(table_name: str) -> mock.Mock:
    """Helper to create a mock DBTNode with a name attribute."""
    node = mock.Mock()
    node.name = table_name
    return node
