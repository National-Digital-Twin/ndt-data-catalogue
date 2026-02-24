<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

---

## title: "Docker Container Architecture"

# Docker Container Architecture

When running DataHub via docker-compose. or helm, the following is a diagram of the containers involved
with running DataHub and their relationships with each other. The helm chart uses helm hooks to determine
the proper ordering of the components whereas docker-compose relies on a series of health checks.

```text
                datahub-frontend-react  datahub-actions
                                     \   /
                                       |   datahub-upgrade (NoCodeDataMigration, helm only)
                                       |   /
                                datahub-gms (healthy)
                                       |
                                datahub-upgrade (SystemUpdate completed)
            /--------------------/   |      \------------------------------------------------\
           /                         |                                                         \
mysql-setup (completed)  elasticsearch-setup (completed)                           (if apply) neo4j (healthy)
    |                           |
    |                           |
mysql (healthy)         elasticsearch (healthy)
```
