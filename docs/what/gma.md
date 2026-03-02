<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

# What is Generalized Metadata Architecture (GMA)?

GMA is the backend infrastructure for DataHub. Unlike existing architectures, GMA leverages multiple storage technologies to efficiently service the four most commonly used query patterns

- Document-oriented CRUD
- Complex queries (including joining distributed tables)
- Graph traversal
- Fulltext search and autocomplete

GMA also embraces a distributed model, where each team owns, develops and operates their own metadata services (known as [GMS](gms.md)), while the metadata are automatically aggregated to populate the central [metadata graph](graph.md) and [search indexes](search-index.md). This is made possible by standardizing the metadata models and the access layer.

We strongly believe that GMA can bring tremendous leverage to any team that has a need to store and access metadata.
Moreover, standardizing metadata modeling promotes a model-first approach to developments, resulting in a more concise, consistent, and highly connected metadata ecosystem that benefits all DataHub users.
