# SPDX-License-Identifier: Apache-2.0
# Originally developed by Acryl Data, Inc.; subsequently adapted, enhanced, and maintained by the National Digital Twin Programme.
#
# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.
"""License header migration tool for NDT."""

__version__ = "0.1.0"

from .migrate import (
    add_crown_copyright_to_markdown,
    add_ndt_header_to_file,
    build_extension_style_map,
    format_comment,
    is_valid_license_header,
    load_styles_with_additions,
    load_yaml,
    migrate_file_content,
    process_file,
    process_file_list,
)
