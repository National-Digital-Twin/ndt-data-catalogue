**SPDX-License-Identifier:** OGL-UK-3.0

**Copyright Owner:** © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

Licensed under the Open Government Licence v3.0.

# License Header Migration Tool

A Python tool designed to help apply license headers across this National Digital Twin open source project. It handles multiple scenarios to ensure the correct files receive the correct licenses. First, run SkyWalking Eyes to generate a list of files that need to be changed. Save that output to a text file, then run this tool as described below.

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
- ✅ Adds NDT-only header to code files without existing headers
- ✅ Adds Crown Copyright header to markdown files (.md, .mdx, .MD)
- ✅ Batch processing from file lists with summary statistics
- ✅ Config-based file filtering using `.licenserc-markdown.yaml` and `.licenserc.yaml`
- ✅ Supports multiple programming languages (Python, Java, TypeScript, JavaScript, Go, etc.)
- ✅ Uses proper comment styles for each language
- ✅ Automatically excludes files based on repository config (with fallback exclusions)
- ✅ Dry-run mode for testing
- ✅ Comprehensive test suite (42 tests)

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

### Quick Start (From Repository Root)

Most common usage - running from `ndt-data-catalogue/` repository root:

```bash
# Dry run (preview changes)
python licence-header-utils/src/license_header_migration/migrate.py --file-list skywalkingeyes-output.txt --dry-run

# Apply changes
python licence-header-utils/src/license_header_migration/migrate.py --file-list skywalkingeyes-output.txt
```

### Command Line (From Package Directory)

**Note:** These commands assume you're in the `licence-header-utils` directory. If you're in the repository root, see [Quick Start](#quick-start-from-repository-root) above.

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

Specify repository root (for finding `.licenserc` config files):

```bash
python -m license_header_migration.migrate --file-list files.txt --repo-root /path/to/repo
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

The tool will process each file and display output like:

```
======================================================================
DOWNLOADING RUNTIME ASSETS
======================================================================
Source: apache/skywalking-eyes
✓ Downloaded: languages.yaml
✓ Downloaded: styles.yaml
Cache directory: /tmp/licence-header-utils-assets
======================================================================

======================================================================
LOADING LICENSE CONFIGURATIONS
======================================================================
Repository root: /home/user/ndt-data-catalogue
✓ Loaded markdown config: .licenserc-markdown.yaml
✓ Loaded general config: .licenserc.yaml
======================================================================

Would migrate: src/main.py
Would migrate: src/utils/helper.py
...

============================================================
SUMMARY
============================================================
Added headers to 5 file(s)
Wrapped headers in 3 file(s)
Skipped 2 file(s)
Total processed: 8 file(s)
============================================================
```

### As a Module

```python
from license_header_migration.migrate import main, process_file

# Process entire directory tree
main(root_dir="./src", dry_run=False)

# Process single file
from license_header_migration.migrate import load_yaml, build_extension_style_map
from license_header_migration.migrate import resolve_asset_paths, load_styles_with_additions

languages_path, styles_path = resolve_asset_paths(assets_dir=None)
languages = load_yaml(languages_path)
styles = load_styles_with_additions(styles_path)
style_map = build_extension_style_map(languages, styles)

process_file("example.py", style_map[".py"], dry_run=False)
```

### Running from Repository Root (Detailed)

If you're in the repository root (`ndt-data-catalogue/`) instead of the `licence-header-utils/` directory:

**Option 1: Run the Python file directly (Recommended)**

This is the simplest approach and doesn't require package installation:

```bash
# Preview changes (dry run)
python licence-header-utils/src/license_header_migration/migrate.py \
  --file-list skywalkingeyes-output.txt \
  --dry-run

# Apply changes
python licence-header-utils/src/license_header_migration/migrate.py \
  --file-list skywalkingeyes-output.txt

# Specify custom repo root for .licenserc files
python licence-header-utils/src/license_header_migration/migrate.py \
  --file-list skywalkingeyes-output.txt \
  --repo-root /path/to/repo \
  --dry-run
```

**Option 2: Change directory first**

```bash
cd licence-header-utils
source venv/bin/activate  # if using virtual environment
python -m license_header_migration.migrate --file-list ../skywalkingeyes-output.txt --dry-run
```

**Option 3: Install the package (for frequent use)**

```bash
cd licence-header-utils
pip install -e .  # Install in editable mode
cd ..  # Back to repo root
python -m license_header_migration.migrate --file-list skywalkingeyes-output.txt --dry-run
```

**Important Notes:**

- The `-m` flag requires the package to be installed via pip
- Don't use slashes (`/`) with `-m`, use dots (`.`) for module paths
- Running the Python file directly (Option 1) works without installation
- The `--repo-root` defaults to the parent of `licence-header-utils/` (i.e., the repository root)

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

This is a guide about the migration tool.
```

#### Output (Crown Copyright Added)

```markdown
<!--
SPDX-License-Identifier: OGL-UK-3.0

Copyright Owner: © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

Licensed under the Open Government Licence v3.0.
-->

# My Documentation

This is a guide about the migration tool.
```

**Note:** Markdown file exclusions are controlled by `.licenserc-markdown.yaml` in the repository root. When the config is not found, the tool falls back to excluding these standard files:

- LICENSE.md, NOTICE.md, ACKNOWLEDGEMENTS.md, CHANGELOG.md
- CODE_OF_CONDUCT.md, CONTRIBUTING.md, MAINTAINERS.md
- OGL_LICENSE.md, README.md, SECURITY.md

## Running Tests

Run all tests:

```bash
pytest
```

If your system Python is externally managed (PEP 668), plain tests still work without `pip install -e`.

Run with coverage:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest --cov=src/license_header_migration --cov-report=html
```

Run specific test:

```bash
pytest tests/test_migrate.py::TestAcrylHeaderMigration::test_python_acryl_header_migration -v
```

## Test Cases

The test suite includes 42 tests covering:

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
├── assets/                     # Local style additions only
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

### License Configuration (Repository Root)

The tool reads exclusion patterns from `.licenserc` configuration files in your repository root:

- **`.licenserc-markdown.yaml`**: Controls markdown file processing

  - `paths`: Glob patterns to identify markdown files (e.g., `**/*.md`, `**/*.mdx`)
  - `paths-ignore`: Markdown files to exclude (e.g., `README.md`, `LICENSE.md`)
  - Example:
    ```yaml
    header:
      paths:
        - "**/*.md"
        - "**/*.mdx"
      paths-ignore:
        - "README.md"
        - "LICENSE.md"
        - "NOTICE.md"
    ```

- **`.licenserc.yaml`**: Controls general file exclusions
  - `paths-ignore`: Files/patterns to exclude from processing (e.g., `**/*.json`, `**/*.txt`)
  - Example:
    ```yaml
    header:
      paths-ignore:
        - "**/*.md"
        - "**/*.json"
        - "**/*.txt"
        - "**/build/**"
    ```

**Exclusion Logic**:

1. Check if file matches markdown patterns → if yes, check markdown exclusions
2. If not excluded by markdown config, check general config exclusions
3. Only process files that pass both filter checks

**Fallback Behavior**: When config files are not found, the tool uses hardcoded exclusions for standard markdown files and processes all other files based on their extension.

### Language & Style Configuration (Runtime Assets)

The tool uses configuration files from [Apache SkyWalking Eyes](https://github.com/apache/skywalking-eyes):

- **languages.yaml**: Defines programming languages and their file extensions

  - Source: https://github.com/apache/skywalking-eyes/blob/main/assets/languages.yaml
  - Originally from GitHub Linguist (MIT license)
  - Downloaded at runtime from GitHub (or provided via `--assets-dir`)

- **styles.yaml**: Defines comment styles for different languages

  - Source: https://github.com/apache/skywalking-eyes/blob/main/assets/styles.yaml
  - Downloaded at runtime from GitHub (or provided via `--assets-dir`)

- **styles-additions.yaml**: NDT-specific style additions
  - Contains local style additions (including `PlainText`)
  - Automatically merged with downloaded/local `styles.yaml` at load time
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
