<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

# Using Cron

Assume you have a recipe file `/home/ubuntu/datahub_ingest/mysql_to_datahub.yml` on your machine

```
source:
  type: mysql
  config:
    # Coordinates
    host_port: localhost:3306
    database: dbname

    # Credentials
    username: root
    password: example

sink:
 type: datahub-rest
 config:
  server: http://localhost:8080
```

We can use crontab to schedule ingestion to run five minutes after midnight, every day using [DataHub CLI](../../docs/cli.md).

```
5 0 * * * datahub ingest -c /home/ubuntu/datahub_ingest/mysql_to_datahub.yml
```

Read through [crontab docs](https://man7.org/linux/man-pages/man5/crontab.5.html) for more options related to scheduling.
