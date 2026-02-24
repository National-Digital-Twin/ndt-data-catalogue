# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

"""
Disable setproctitle on macOS to prevent SIGSEGV when called after fork().

On macOS, the setproctitle C extension uses APIs that are unsafe in a
multi-threaded process after fork(), causing crashes (e.g. in gunicorn workers,
OpenLineage, or any forked child). This module replaces the C implementation
with no-ops so any later caller gets a safe no-op. It runs at interpreter
startup (via .pth) or when datahub is first imported (via datahub/__init__.py).

See: https://github.com/apache/airflow/issues/55838
"""

from __future__ import annotations

import platform
import sys

if sys.platform == "darwin" and platform.system() == "Darwin":
    try:
        import setproctitle

        def _noop_setproctitle(title: str) -> None:
            pass

        def _noop_getproctitle() -> str:
            return ""

        setproctitle.setproctitle = _noop_setproctitle  # type: ignore[assignment]
        setproctitle.getproctitle = _noop_getproctitle  # type: ignore[assignment]
    except ImportError:
        pass
