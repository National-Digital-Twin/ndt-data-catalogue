<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

# General Debugging Guide

## Logo for my platform is not appearing on the Home Page or search results

Please see if either of these guides help you

- [Adding a custom Dataset Data Platform](../how/add-custom-data-platform.md)
- [DataHub CLI put platform command](../cli.md#put-platform)

## How do I add dataset freshness indicator for datasets?

You can emit an [operation aspect](https://github.com/datahub-project/datahub/blob/master/metadata-models/src/main/pegasus/com/linkedin/common/Operation.pdl) for the same.
