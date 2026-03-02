# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

# Patch setproctitle on macOS before any fork can occur (avoids SIGSEGV in child processes).
import datahub._setproctitle_patch
from datahub._version import __package_name__, __version__
