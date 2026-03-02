<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

Note! The integration can use an SQL parser to try to parse the tables the chart depends on. This parsing is disabled by default,
but can be enabled by setting `parse_table_names_from_sql: true`. The parser is based on the [`sqlglot`](https://pypi.org/project/sqlglot/) package.
