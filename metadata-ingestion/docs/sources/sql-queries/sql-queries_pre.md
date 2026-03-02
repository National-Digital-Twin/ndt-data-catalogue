<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

#### Example Queries File

```json
{"query": "SELECT x FROM my_table", "timestamp": 1689232738.051, "user": "user_a", "downstream_tables": [], "upstream_tables": ["my_database.my_schema.my_table"]}
{"query": "INSERT INTO my_table VALUES (1, 'a')", "timestamp": 1689232737.669, "user": "user_b", "downstream_tables": ["my_database.my_schema.my_table"], "upstream_tables": []}
```

Note that this file does not represent a single JSON object, but instead newline-delimited JSON, in which
each line is a separate JSON object.
