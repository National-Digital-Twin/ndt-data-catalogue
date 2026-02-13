**SPDX-License-Identifier:** OGL-UK-3.0

**Copyright Owner:** © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

Licensed under the Open Government Licence v3.0.

# License Header Migration Tool

A Python tool for managing license headers in National Digital Twin Programme (NDT) projects.

## Overview

This tool handles license headers for code inherited from Acryl Data and new NDT-developed code:

- **Wraps existing Acryl headers** with NDT preamble and footer text while preserving original copyright notices
- **Adds NDT-only headers** to code files without existing license headers
- **Adds Crown Copyright headers** to markdown documentation files
- **Batch processes** files from lists with summary statistics

It uses the same language and comment style definitions as [Apache SkyWalking Eyes](https://github.com/apache/skywalking-eyes) to support multiple programming languages.

## Features

- ✅ Detects existing license headers in source files
- ✅ Wraps Acryl headers with NDT preamble and footer
- ✅ **NEW: Adds NDT-only header to code files without existing headers**
- ✅ **NEW: Adds Crown Copyright header to markdown files (.md, .mdx)**
- ✅ **NEW: Batch processing from file lists with summary statistics**
- ✅ Supports multiple programming languages (Python, Java, TypeScript, JavaScript, Go, etc.)
- ✅ Uses proper comment styles for each language
- ✅ Automatically excludes standard markdown files (README.md, LICENSE.md, etc.)
- ✅ Dry-run mode for testing
- ✅ Comprehensive test suite (37 tests)

## Installation

### Development Installation

```bash
cd licence-header-utils
pip install -e ".[dev]"
```

This installs the package in editable mode with development dependencies (pytest, pytest-cov).

### Regular Installation

```bash
cd licence-header-utils
pip install .
```

## Usage

### Command Line

Process all files in current directory:

```bash
migrate-headers
```

Process a specific directory:

```bash
python -m license_header_migration.migrate /path/to/directory
```

Process files from a list (batch processing):

```bash
python -m license_header_migration.migrate --file-list files.txt
```

Dry run (preview changes without modifying files):

```bash
python -m license_header_migration.migrate --file-list files.txt --dry-run
```

#### File List Format

Create a text file with one file path per line. Lines starting with `#` are treated as comments and empty lines are ignored:

```text
# Python files
src/main.py
src/utils/helper.py

# TypeScript files
frontend/app.ts
frontend/components/Button.tsx

# Markdown documentation
docs/guide.md
```

The tool will process each file and display a summary:

```
Migrated: src/main.py
Migrated: src/utils/helper.py
...
===== Summary =====
Added headers to 5 file(s)
Wrapped headers in 3 file(s)
Skipped 2 file(s) (already processed)
Encountered errors in 0 file(s)
```

### As a Module

```python
from license_header_migration.migrate import main, process_file

# Process entire directory tree
main(root_dir="./src", dry_run=False)

# Process single file
from license_header_migration.migrate import load_yaml, build_extension_style_map

assets_dir = "./assets"
languages = load_yaml(f"{assets_dir}/languages.yaml")
styles = load_yaml(f"{assets_dir}/styles.yaml")
style_map = build_extension_style_map(languages, styles)

process_file("example.py", style_map[".py"], dry_run=False)
```

## What It Does

The tool handles two scenarios:

### 1. Files with Existing Acryl Headers (Wrapping)

#### Input (Acryl Header)

```python
# Copyright 2024 Acryl Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ...

def my_function():
    pass
```

#### Output (NDT Wrapped Header)

```python
# SPDX-License-Identifier: Apache-2.0
# Originally developed by Acryl Data, Inc.; subsequently adapted, enhanced,
# and maintained by the National Digital Twin Programme.
#
# Copyright 2024 Acryl Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ...
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

def my_function():
    pass
```

### 2. Files with No Existing Headers (Adding)

#### Input (No Header)

```python
def calculate_sum(a, b):
    return a + b
```

#### Output (NDT Header Added)

```python
# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

def calculate_sum(a, b):
    return a + b
```

### 3. Markdown Files (Crown Copyright)

#### Input (Markdown without header)

```markdown
# My Documentation

This is a guide about something.
```

#### Output (Crown Copyright Added)

```markdown
**SPDX-License-Identifier:** OGL-UK-3.0

**Copyright Owner:** © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

Licensed under the Open Government Licence v3.0.

---

# My Documentation

This is a guide about something.
```

**Note:** The following markdown files are automatically excluded from processing:

- LICENSE.md, NOTICE.md, ACKNOWLEDGEMENTS.md, CHANGELOG.md
- CODE_OF_CONDUCT.md, CONTRIBUTING.md, MAINTAINERS.md
- OGL_LICENSE.md, README.md, SECURITY.md

## Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src/license_header_migration --cov-report=html
```

Run specific test:

```bash
pytest tests/test_migrate.py::TestAcrylHeaderMigration::test_python_acryl_header_migration -v
```

## Test Cases

The test suite includes 34 tests covering:

1. **No Header Test**: Files without headers get NDT-only header added
2. **Acryl Header Test**: Files with Acryl headers are properly wrapped with NDT preamble and footer
3. **Multiple Language Tests**: Python (.py), Java (.java), TypeScript (.ts) files
4. **Markdown Tests**: Crown Copyright headers added to .md/.mdx files
5. **Exclusion Tests**: Excluded markdown files (README.md, LICENSE.md, etc.) are skipped
6. **Dry Run Test**: Dry run mode doesn't modify files
7. **Already Migrated Test**: Already migrated files are skipped
8. **Comment Formatting Tests**: Proper comment styles for different languages
9. **Add NDT Header Tests**: Direct testing of adding headers to files without existing headers

## Project Structure

```
licence-header-utils/
├── pyproject.toml              # Project configuration
├── README.md                   # This file
├── assets/                     # Language and style definitions
│   ├── languages.yaml          # From skywalking-eyes (modified)
│   ├── styles.yaml             # From skywalking-eyes (upstream-safe)
│   └── styles-additions.yaml   # NDT-specific styles
├── src/
│   └── license_header_migration/
│       ├── __init__.py
│       └── migrate.py          # Main migration logic
└── tests/
    ├── __init__.py
    ├── test_migrate.py         # Test suite
    └── fixtures/               # Test files
        ├── no_header.py
        ├── no_header.md
        ├── acryl_header.py
        ├── acryl_header.java
        ├── acryl_header.ts
        ├── with_crown_copyright.md
        └── README.md
```

## Configuration Files

The tool uses configuration files from [Apache SkyWalking Eyes](https://github.com/apache/skywalking-eyes):

- **languages.yaml**: Defines programming languages and their file extensions

  - Source: https://github.com/apache/skywalking-eyes/blob/main/assets/languages.yaml
  - Originally from GitHub Linguist (MIT license)
  - **Note:** Modified to set Markdown's `comment_style_id` to `PlainText` (line 3269)

- **styles.yaml**: Defines comment styles for different languages

  - Source: https://github.com/apache/skywalking-eyes/blob/main/assets/styles.yaml
  - **Can be safely re-downloaded** from upstream without losing functionality

- **styles-additions.yaml**: NDT-specific style additions
  - Contains the `PlainText` style for markdown files
  - Automatically merged with `styles.yaml` at load time
  - Ensures upstream `styles.yaml` can be updated without conflicts

## Supported File Types

The tool supports any language defined in `languages.yaml` that has a `comment_style_id`, including:

- Python (.py)
- Java (.java)
- JavaScript (.js)
- TypeScript (.ts)
- Go (.go)
- C/C++ (.c, .cpp, .h)
- Shell scripts (.sh)
- YAML (.yml, .yaml)
- And many more...

## License

This tool is part of the NDT data catalogue project.

## Credits

- Comment style detection based on [Apache SkyWalking Eyes](https://github.com/apache/skywalking-eyes)
- Language definitions from [GitHub Linguist](https://github.com/github/linguist)
