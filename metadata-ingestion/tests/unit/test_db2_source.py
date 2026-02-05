# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

import pytest

from datahub.ingestion.source.sql.db2 import _quote_identifier, _split_zos_pathschemas


@pytest.mark.parametrize(
    "input, expected",
    [
        ('"SINGLE_SCHEMA"', ["SINGLE_SCHEMA"]),
        ('"lowercase_schema"', ["lowercase_schema"]),
        ('"MULTIPLE_SCHEMAS","SCHEMA_TWO"', ["MULTIPLE_SCHEMAS", "SCHEMA_TWO"]),
        ('"SCHEMA WITH ""ESCAPED"" QUOTES"', ['SCHEMA WITH "ESCAPED" QUOTES']),
    ],
)
def test_db2_split_zos_pathschemas(input, expected):
    assert _split_zos_pathschemas(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("UPPERCASE", '"UPPERCASE"'),
        ("lowercase", '"lowercase"'),
        ('with double "quotes"', '"with double ""quotes"""'),
    ],
)
def test_db2_quote_identifier(input, expected):
    assert _quote_identifier(input) == expected
