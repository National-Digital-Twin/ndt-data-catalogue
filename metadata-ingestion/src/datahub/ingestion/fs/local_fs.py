# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

import os
import pathlib
from typing import Any, Iterable

from datahub.ingestion.fs.fs_base import FileInfo, FileSystem


class LocalFileSystem(FileSystem):
    @classmethod
    def create(cls, **kwargs):
        return LocalFileSystem()

    def open(self, path: str, **kwargs: Any) -> Any:
        # Local does not support any additional kwargs
        assert not kwargs
        return pathlib.Path(path).open(mode="rb")

    def list(self, path: str) -> Iterable[FileInfo]:
        p = pathlib.Path(path)
        if p.is_file():
            return [self.file_status(path)]
        else:
            return iter([self.file_status(str(x)) for x in p.iterdir()])

    def file_status(self, path: str) -> FileInfo:
        if os.path.isfile(path):
            return FileInfo(path, os.path.getsize(path), is_file=True)
        else:
            return FileInfo(path, 0, is_file=False)

    def write(self, path: str, content: str, **kwargs: Any) -> None:
        """Write content to a local file."""
        # Create parent directories if they don't exist
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)

        # Write the content
        with p.open("w", **kwargs) as f:
            f.write(content)

    def exists(self, path: str) -> bool:
        """Check if a file exists locally."""
        return pathlib.Path(path).exists()
