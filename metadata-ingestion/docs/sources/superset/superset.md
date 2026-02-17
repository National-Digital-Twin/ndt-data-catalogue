<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

If you were using `database_alias` in one of your other ingestions to rename your databases to something else based on business needs you can rename them in superset also

```yml
source:
  type: superset
  config:
    # Coordinates
    connect_uri: http://localhost:8088

    # Credentials
    username: user
    password: pass
    provider: ldap
    database_alias:
      example_name_1: business_name_1
      example_name_2: business_name_2

sink:
  # sink configs
```
