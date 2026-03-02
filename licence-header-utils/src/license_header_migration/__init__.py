# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity


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
