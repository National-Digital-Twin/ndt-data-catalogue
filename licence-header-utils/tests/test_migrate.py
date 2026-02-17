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

"""Tests for license header migration."""
import tempfile
import shutil
from pathlib import Path
import pytest

from license_header_migration.migrate import (
    build_extension_style_map,
    format_comment,
    is_valid_license_header,
    migrate_file_content,
    add_ndt_header_to_file,
    add_crown_copyright_to_markdown,
    process_file,
)


@pytest.fixture
def fixtures_dir():
    """Get the fixtures directory path."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def style_map():
    """Build extension to style map from minimal in-memory test assets."""
    styles_yaml = [
        {"id": "Hashtag", "start": "#", "middle": "#", "end": "#", "after": "(?m)^#!.*$"},
        {"id": "SlashAsterisk", "start": "/*", "middle": " *", "end": " */"},
        {"id": "DoubleSlash", "start": "//", "middle": "//", "end": "//"},
        {"id": "PlainText", "start": "", "middle": "", "end": ""},
    ]

    languages_yaml = {
        "Python": {"extensions": [".py"], "comment_style_id": "Hashtag", "ace_mode": "python"},
        "Java": {"extensions": [".java"], "comment_style_id": "SlashAsterisk", "ace_mode": "java"},
        "TypeScript": {"extensions": [".ts", ".tsx"], "comment_style_id": "SlashAsterisk", "ace_mode": "typescript"},
                "JavaScript": {"extensions": [".js"], "comment_style_id": "SlashAsterisk", "ace_mode": "javascript"},
                "Go": {"extensions": [".go"], "comment_style_id": "SlashAsterisk", "ace_mode": "go"},
                "Shell": {"extensions": [".sh"], "comment_style_id": "Hashtag", "ace_mode": "sh"},
        "Gradle": {"extensions": [".gradle"], "comment_style_id": "SlashAsterisk", "ace_mode": "text"},
        "Markdown": {"extensions": [".md", ".mdx"], "comment_style_id": "PlainText", "ace_mode": "markdown"},
    }

    return build_extension_style_map(languages_yaml, styles_yaml)


@pytest.fixture
def local_assets_dir(tmp_path):
        """Create local assets for tests that call process_file_list/main loaders."""
        assets_dir = tmp_path / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)

        (assets_dir / "languages.yaml").write_text(
                "Python:\n"
                "  extensions:\n"
                "    - '.py'\n"
                "  comment_style_id: Hashtag\n"
                "  ace_mode: python\n"
                "Shell:\n"
                "  extensions:\n"
                "    - '.sh'\n"
                "  comment_style_id: Hashtag\n"
                "  ace_mode: sh\n"
                "Markdown:\n"
                "  extensions:\n"
                "    - '.md'\n"
                "  comment_style_id: PlainText\n"
                "  ace_mode: markdown\n",
                encoding="utf-8",
        )

        (assets_dir / "styles.yaml").write_text(
                "- id: Hashtag\n"
                "  start: '#'\n"
                "  middle: '#'\n"
                "  end: '#'\n"
                "  after: '(?m)^#!.*$'\n"
                "- id: PlainText\n"
                "  start: ''\n"
                "  middle: ''\n"
                "  end: ''\n",
                encoding="utf-8",
        )

        return str(assets_dir)


class TestFormatComment:
    """Tests for comment formatting."""
    
    def test_hash_comment_single_line(self):
        """Test single-line hash comment formatting."""
        style = {"start": "#"}
        result = format_comment("This is a comment", style)
        assert result == "# This is a comment"
    
    def test_hash_comment_multiline(self):
        """Test multi-line hash comment formatting."""
        style = {"start": "#"}
        text = "Line one\nLine two"
        result = format_comment(text, style)
        assert result == "# Line one\n# Line two"
    
    def test_slash_asterisk_single_line(self):
        """Test single-line /* */ comment formatting."""
        style = {"start": "/*", "end": "*/", "middle": " *"}
        result = format_comment("Single line", style, multiline=False)
        assert result == "/* Single line */"
    
    def test_slash_asterisk_multiline(self):
        """Test multi-line /* */ comment formatting."""
        style = {"start": "/*", "end": "*/", "middle": " *"}
        text = "Line one\nLine two"
        result = format_comment(text, style, multiline=True)
        assert "/*" in result
        assert "*/" in result
        assert " * Line one" in result
        assert " * Line two" in result
    
    def test_empty_comment(self):
        """Test empty comment formatting."""
        style = {"start": "#"}
        result = format_comment("", style)
        assert result == "#"


class TestLicenseHeaderDetection:
    """Tests for license header detection."""
    
    def test_valid_license_header_copyright(self):
        """Test detection of copyright headers."""
        text = "Copyright 2024 Example Corp"
        assert is_valid_license_header(text) is True
    
    def test_valid_license_header_license(self):
        """Test detection of license headers."""
        text = "Licensed under the Apache License"
        assert is_valid_license_header(text) is True
    
    def test_valid_license_header_spdx(self):
        """Test detection of SPDX headers."""
        text = "SPDX-License-Identifier: Apache-2.0"
        assert is_valid_license_header(text) is True
    
    def test_invalid_license_header(self):
        """Test non-license text is not detected."""
        text = "This is just a regular comment"
        assert is_valid_license_header(text) is False


class TestFileNoHeader:
    """Tests for files with no existing license header."""
    
    def test_no_header_file_gets_ndt_header(self, fixtures_dir, style_map):
        """Test that files with no header get NDT-only header added."""
        with open(fixtures_dir / "no_header.py", "r") as f:
            content = f.read()
        
        style = style_map[".py"]
        result = migrate_file_content(content, style)
        
        # Should have added NDT header
        assert result is not None
        
        # Should contain SPDX identifier
        assert "SPDX-License-Identifier: Apache-2.0" in result
        
        # Should contain NDT statement
        assert "National Digital Twin Programme" in result
        
        # Should mention Acryl Data
        assert "Acryl Data, Inc." in result
        
        # Should maintain the original code
        assert "def hello_world():" in result
        
        # Should NOT have the preamble "Originally developed" (that's only for wrapping)
        assert "Originally developed by Acryl Data" not in result
        
    def test_no_header_java_file(self, fixtures_dir, style_map, tmp_path):
        """Test adding NDT header to Java file without header."""
        # Create a Java file without header
        java_content = """
package com.example;

public class Test {
    public static void main(String[] args) {
        System.out.println("Test");
    }
}
"""
        style = style_map[".java"]
        result = migrate_file_content(java_content, style)
        
        # Should have added NDT header
        assert result is not None
        assert "SPDX-License-Identifier: Apache-2.0" in result
        assert "National Digital Twin Programme" in result
        assert "public class Test" in result
        
        # Verify it uses /* */ comment style
        assert "/*" in result
        assert "*/" in result


class TestAddNDTHeader:
    """Tests for adding NDT header to files without existing headers."""
    
    def test_add_ndt_header_python(self, style_map):
        """Test adding NDT header to Python file."""
        content = """def my_function():
    return "test"
"""
        style = style_map[".py"]
        result = add_ndt_header_to_file(content, style)
        
        assert result is not None
        assert "SPDX-License-Identifier: Apache-2.0" in result
        assert "This file is unmodified from its original version developed by Acryl Data, Inc." in result
        assert "National Digital Twin Programme" in result
        assert "def my_function():" in result
    
    def test_add_ndt_header_java(self, style_map):
        """Test adding NDT header to Java file."""
        content = """package com.example;

public class MyClass {
}
"""
        style = style_map[".java"]
        result = add_ndt_header_to_file(content, style)
        
        assert result is not None
        assert "/*" in result
        assert "SPDX-License-Identifier: Apache-2.0" in result
        assert "National Digital Twin Programme" in result
        assert "package com.example;" in result
    
    def test_add_ndt_header_skip_already_processed(self, style_map):
        """Test that already processed files are skipped."""
        content = """# SPDX-License-Identifier: Apache-2.0
# National Digital Twin Programme

def test():
    pass
"""
        style = style_map[".py"]
        result = add_ndt_header_to_file(content, style)
        
        # Should return None (already has NDT header)
        assert result is None
    
    def test_add_ndt_header_typescript(self, style_map):
        """Test adding NDT header to TypeScript file."""
        content = """export function hello() {
    console.log("Hello");
}
"""
        style = style_map[".ts"]
        result = add_ndt_header_to_file(content, style)
        
        assert result is not None
        assert "/*" in result
        assert "SPDX-License-Identifier: Apache-2.0" in result
        assert "National Digital Twin Programme" in result
        assert "export function hello()" in result


class TestAcrylHeaderMigration:
    """Tests for migrating files with Acryl license headers."""
    
    def test_python_acryl_header_migration(self, fixtures_dir, style_map):
        """Test migration of Python file with Acryl header."""
        with open(fixtures_dir / "acryl_header.py", "r") as f:
            content = f.read()
        
        style = style_map[".py"]
        result = migrate_file_content(content, style)
        
        # Should have migrated content
        assert result is not None
        
        # Should contain NDT preamble
        assert "National Digital Twin Programme" in result
        
        # Should contain SPDX identifier at the top
        assert "SPDX-License-Identifier: Apache-2.0" in result
        
        # Should contain original Acryl copyright
        assert "Copyright 2024 Acryl Data, Inc." in result
        
        # Should contain footer text
        assert "This file is unmodified from its original version" in result
        
        # Should maintain the original code
        assert "def process_data(data):" in result
    
    def test_java_acryl_header_migration(self, fixtures_dir, style_map):
        """Test migration of Java file with Acryl header."""
        with open(fixtures_dir / "acryl_header.java", "r") as f:
            content = f.read()
        
        style = style_map[".java"]
        result = migrate_file_content(content, style)
        
        # Should have migrated content
        assert result is not None
        
        # Should contain NDT preamble
        assert "National Digital Twin Programme" in result
        
        # Should contain SPDX identifier
        assert "SPDX-License-Identifier: Apache-2.0" in result
        
        # Should contain original Acryl copyright
        assert "Copyright 2024 Acryl Data, Inc." in result
        
        # Should maintain the original code
        assert "public class HelloWorld" in result
    
    def test_typescript_acryl_header_migration(self, fixtures_dir, style_map):
        """Test migration of TypeScript file with Acryl header."""
        with open(fixtures_dir / "acryl_header.ts", "r") as f:
            content = f.read()
        
        style = style_map[".ts"]
        result = migrate_file_content(content, style)
        
        # Should have migrated content
        assert result is not None
        
        # Should contain NDT preamble
        assert "National Digital Twin Programme" in result
        
        # Should contain SPDX identifier
        assert "SPDX-License-Identifier: Apache-2.0" in result
        
        # Should contain original Acryl copyright
        assert "Copyright 2024 Acryl Data, Inc." in result
        
        # Should maintain the original code
        assert "export function greet" in result


class TestProcessFile:
    """Tests for file processing."""
    
    def test_process_file_with_acryl_header(self, fixtures_dir, style_map, tmp_path):
        """Test processing a file with Acryl header."""
        # Copy fixture to temp location
        source = fixtures_dir / "acryl_header.py"
        dest = tmp_path / "test_file.py"
        shutil.copy(source, dest)
        
        # Process the file
        style = style_map[".py"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should have wrapped the existing header
        assert result == "wrapped"
        
        # File should be modified
        with open(dest, "r") as f:
            content = f.read()
        
        assert "National Digital Twin Programme" in content
        assert "SPDX-License-Identifier: Apache-2.0" in content
    
    def test_process_file_with_no_header(self, fixtures_dir, style_map, tmp_path):
        """Test processing a file without existing header."""
        # Copy fixture to temp location
        source = fixtures_dir / "no_header.py"
        dest = tmp_path / "test_no_header.py"
        shutil.copy(source, dest)
        
        # Process the file
        style = style_map[".py"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should have added header
        assert result == "added"
        
        # File should have NDT header added
        with open(dest, "r") as f:
            content = f.read()
        
        assert "National Digital Twin Programme" in content
        assert "SPDX-License-Identifier: Apache-2.0" in content
        assert "def hello_world():" in content

    def test_process_file_adds_trailing_newline(self, style_map, tmp_path):
        """Test processing ensures output file has a trailing newline."""
        dest = tmp_path / "no_newline.py"
        with open(dest, "w", encoding="utf-8") as f:
            f.write('def hello_world():\n    return "Hello"')

        style = style_map[".py"]
        result = process_file(str(dest), style, dry_run=False)

        assert result == "added"

        with open(dest, "r", encoding="utf-8") as f:
            content = f.read()

        assert content.endswith("\n")

    def test_process_tsx_no_blank_line_after_header(self, style_map, tmp_path):
        """Test TSX migration does not insert an extra blank line before first import."""
        dest = tmp_path / "IdentitiesContent.tsx"
        with open(dest, "w", encoding="utf-8") as f:
            f.write("import React from 'react';\n\nexport const X = () => null;\n")

        style = style_map[".tsx"]
        result = process_file(str(dest), style, dry_run=False)

        assert result == "added"

        with open(dest, "r", encoding="utf-8") as f:
            content = f.read()

        assert "*/\nimport React from 'react';" in content
        assert "*/\n\nimport React from 'react';" not in content

    def test_wrap_tsx_no_blank_line_after_wrapped_header(self, style_map, tmp_path):
        """Test wrapped TSX Acryl header does not leave an extra blank line before first import."""
        dest = tmp_path / "WrappedIdentitiesContent.tsx"
        with open(dest, "w", encoding="utf-8") as f:
            f.write(
                "/**\n"
                " * Copyright 2025 Acryl Data, Inc.\n"
                " *\n"
                " * Licensed under the Apache License, Version 2.0 (the \"License\");\n"
                " * you may not use this file except in compliance with the License.\n"
                " * You may obtain a copy of the License at\n"
                " *\n"
                " *    http://www.apache.org/licenses/LICENSE-2.0\n"
                " */\n"
                "import React from 'react';\n\n"
                "export const X = () => null;\n"
            )

        style = style_map[".tsx"]
        result = process_file(str(dest), style, dry_run=False)

        assert result == "wrapped"

        with open(dest, "r", encoding="utf-8") as f:
            content = f.read()

        # Footer block should be immediately followed by import (no extra blank line)
        assert "National Digital Twin Programme.\n */\nimport React from 'react';" in content
        assert "National Digital Twin Programme.\n */\n\nimport React from 'react';" not in content
    
    def test_process_file_dry_run(self, fixtures_dir, style_map, tmp_path):
        """Test dry run doesn't modify files."""
        # Copy fixture to temp location
        source = fixtures_dir / "acryl_header.py"
        dest = tmp_path / "test_file.py"
        shutil.copy(source, dest)
        
        # Read original content
        with open(dest, "r") as f:
            original_content = f.read()
        
        # Process with dry run
        style = style_map[".py"]
        result = process_file(str(dest), style, dry_run=True)
        
        # Should report it would wrap header
        assert result == "wrapped"
        
        # File should be unchanged
        with open(dest, "r") as f:
            current_content = f.read()
        
        assert current_content == original_content
    
    def test_process_file_already_migrated(self, style_map, tmp_path):
        """Test that already migrated files with wrapped headers are skipped."""
        # Create a file with NDT wrapped header already
        content = """# SPDX-License-Identifier: Apache-2.0
# Originally developed by Acryl Data, Inc.; subsequently adapted, enhanced,
# and maintained by the National Digital Twin Programme.
#
# Copyright 2024 Acryl Data, Inc.

def test():
    pass
"""
        dest = tmp_path / "already_migrated.py"
        with open(dest, "w") as f:
            f.write(content)
        
        style = style_map[".py"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should return already_migrated (already has correct header)
        assert result == "already_migrated"
    
    def test_acryl_header_2026_gets_wrapped(self, style_map, fixtures_dir, tmp_path):
        """Test that Acryl header with 2026 copyright is recognized and wrapped correctly."""
        # Copy the fixture to tmp_path so we don't modify the original
        source = fixtures_dir / "acryl_header_2026.ts"
        dest = tmp_path / "acryl_header_2026.ts"
        shutil.copy(source, dest)
        
        style = style_map[".ts"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should recognize 2026 as valid Acryl year and wrap it
        assert result == "wrapped"
        
        # Verify the wrapped header is correct with both top wrapper and bottom disclaimer
        with open(dest, "r") as f:
            content = f.read()
        assert "SPDX-License-Identifier: Apache-2.0" in content
        assert "Originally developed by Acryl Data, Inc." in content
        assert "Copyright 2026 Acryl Data, Inc." in content
        # Verify bottom disclaimer is present (only for wrapped Acryl licenses)
        assert "This file is unmodified from its original version developed by Acryl Data, Inc." in content
        assert "All support, maintenance and further development of this code is now the responsibility" in content
    
    def test_acryl_header_2021_gets_wrapped(self, style_map, fixtures_dir, tmp_path):
        """Test that Acryl header with 2021 copyright is recognized and wrapped correctly."""
        # Copy the fixture to tmp_path so we don't modify the original
        source = fixtures_dir / "acryl_header_2021.ts"
        dest = tmp_path / "acryl_header_2021.ts"
        shutil.copy(source, dest)
        
        style = style_map[".ts"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should recognize 2021 as valid Acryl year and wrap it
        assert result == "wrapped"
        
        # Verify the wrapped header is correct with both top wrapper and bottom disclaimer
        with open(dest, "r") as f:
            content = f.read()
        assert "SPDX-License-Identifier: Apache-2.0" in content
        assert "Originally developed by Acryl Data, Inc." in content
        assert "Copyright 2021 Acryl Data, Inc." in content
        # Verify bottom disclaimer is present (only for wrapped Acryl licenses)
        assert "This file is unmodified from its original version developed by Acryl Data, Inc." in content
        assert "All support, maintenance and further development of this code is now the responsibility" in content
    
    def test_acryl_header_javadoc_style_gets_wrapped(self, style_map, fixtures_dir, tmp_path):
        """Test that Acryl header with javadoc-style (/**) comment is recognized and wrapped correctly."""
        # Copy the fixture to tmp_path so we don't modify the original
        source = fixtures_dir / "acryl_header_javadoc_style.java"
        dest = tmp_path / "acryl_header_javadoc_style.java"
        shutil.copy(source, dest)
        
        style = style_map[".java"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should recognize /** style Acryl header and wrap it
        assert result == "wrapped"
        
        # Verify the wrapped header is correct with both top wrapper and bottom disclaimer
        with open(dest, "r") as f:
            content = f.read()
        assert "SPDX-License-Identifier: Apache-2.0" in content
        assert "Originally developed by Acryl Data, Inc." in content
        assert "Copyright 2025 Acryl Data, Inc." in content
        # Verify bottom disclaimer is present (only for wrapped Acryl licenses)
        assert "This file is unmodified from its original version developed by Acryl Data, Inc." in content
        assert "All support, maintenance and further development of this code is now the responsibility" in content
    
    def test_acryl_header_gradle_gets_wrapped(self, style_map, fixtures_dir, tmp_path):
        """Test that Acryl header from gradle file (/** with no space after asterisk) is recognized and wrapped correctly."""
        # Copy the fixture to tmp_path so we don't modify the original
        source = fixtures_dir / "acryl_header_gradle.gradle"
        dest = tmp_path / "acryl_header_gradle.gradle"
        shutil.copy(source, dest)
        
        style = style_map[".gradle"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should recognize /** style Acryl header and wrap it
        assert result == "wrapped"
        
        # Verify the wrapped header is correct with both top wrapper and bottom disclaimer
        with open(dest, "r") as f:
            content = f.read()
        assert "SPDX-License-Identifier: Apache-2.0" in content
        assert "Originally developed by Acryl Data, Inc." in content
        assert "Copyright 2025 Acryl Data, Inc." in content
        # Verify bottom disclaimer is present (only for wrapped Acryl licenses)
        assert "This file is unmodified from its original version developed by Acryl Data, Inc." in content
        assert "All support, maintenance and further development of this code is now the responsibility" in content
    
    def test_process_file_with_ndt_only_header_not_wrapped(self, style_map, tmp_path):
        """Test that files with NDT-only header are not wrapped with Acryl wrapper."""
        # Create a file with NDT-only header (no Acryl copyright)
        content = """# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

def my_function():
    return "test"
"""
        dest = tmp_path / "ndt_only_header.py"
        with open(dest, "w") as f:
            f.write(content)
        
        # Read original content
        with open(dest, "r") as f:
            original_content = f.read()
        
        style = style_map[".py"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should return already_migrated (already has NDT header)
        assert result == "already_migrated"
        
        # Verify file is unchanged
        with open(dest, "r") as f:
            current_content = f.read()
        
        assert current_content == original_content
        
        # Verify it does NOT have the wrapped format (no "Originally developed by")
        assert "Originally developed by" not in current_content
    
    def test_migrate_content_with_ndt_only_header(self, style_map):
        """Test migrate_file_content doesn't wrap NDT-only headers."""
        content = """# SPDX-License-Identifier: Apache-2.0
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

def test():
    pass
"""
        style = style_map[".py"]
        result = migrate_file_content(content, style)
        
        # Should return None (no migration needed)
        assert result is None


class TestExtensionStyleMap:
    """Tests for extension to style mapping."""
    
    def test_common_extensions_mapped(self, style_map):
        """Test that common file extensions have styles."""
        assert ".py" in style_map
        assert ".java" in style_map
        assert ".ts" in style_map
        assert ".js" in style_map
        assert ".go" in style_map
    
    def test_python_uses_hash_comments(self, style_map):
        """Test that Python files use hash comments."""
        python_style = style_map[".py"]
        assert python_style["start"] == "#"
    
    def test_java_uses_slash_asterisk(self, style_map):
        """Test that Java files use /* */ comments."""
        java_style = style_map[".java"]
        assert java_style["start"] == "/*"
        assert java_style["end"] == " */"  # Note: space before */

class TestMarkdownFiles:
    """Tests for markdown file processing."""
    
    def test_markdown_uses_plaintext_style(self, style_map):
        """Test that markdown files use PlainText style."""
        md_style = style_map[".md"]
        assert md_style["id"] == "PlainText"
        assert md_style["start"] == ""
        assert md_style["middle"] == ""
        assert md_style["end"] == ""
    
    def test_add_crown_copyright_to_markdown(self):
        """Test adding Crown Copyright header to markdown file."""
        content = """# Example Documentation

This is a test markdown file.
"""
        result = add_crown_copyright_to_markdown(content)
        
        assert result is not None
        assert "<!--" in result
        assert "SPDX-License-Identifier: OGL-UK-3.0" in result
        assert "-->" in result
        assert "Crown Copyright 2025" in result
        assert "National Digital Twin Programme" in result
        assert "Open Government Licence v3.0" in result
        assert "# Example Documentation" in result
        # Check header comes before the original content
        assert result.index("Crown Copyright") < result.index("# Example Documentation")
    
    def test_add_crown_copyright_skip_already_processed(self):
        """Test that files with Crown Copyright are skipped."""
        content = """<!--
    SPDX-License-Identifier: OGL-UK-3.0

© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme.
    -->

# Documentation
"""
        result = add_crown_copyright_to_markdown(content)
        assert result is None
    
    def test_add_crown_copyright_skip_ogl_license(self):
        """Test that files with OGL license are skipped."""
        content = """Licensed under the Open Government Licence v3.0.

# Documentation
"""
        result = add_crown_copyright_to_markdown(content)
        assert result is None
    
    def test_process_markdown_file(self, style_map, tmp_path, fixtures_dir):
        """Test processing a markdown file."""
        # Copy fixture to temp location
        source = fixtures_dir / "no_header.md"
        dest = tmp_path / "test_doc.md"
        shutil.copy(source, dest)
        
        style = style_map[".md"]
        result = process_file(str(dest), style, dry_run=False)
        
        assert result == "added"
        
        with open(dest, "r") as f:
            content = f.read()
        
        assert "<!--" in content
        assert "-->" in content
        assert "Crown Copyright 2025" in content
        assert "OGL-UK-3.0" in content
        assert "# Example Documentation" in content

    def test_process_uppercase_md_file_has_html_header(self, style_map, tmp_path, fixtures_dir):
        """Test processing an .MD file adds HTML comment style markdown header."""
        source = fixtures_dir / "no_header.md"
        dest = tmp_path / "UPPERCASE.MD"
        shutil.copy(source, dest)

        style = style_map[".md"]
        result = process_file(str(dest), style, dry_run=False)

        assert result == "added"

        with open(dest, "r") as f:
            content = f.read()

        assert content.lstrip().startswith("<!--")
        assert "SPDX-License-Identifier: OGL-UK-3.0" in content
        assert "Open Government Licence v3.0" in content
        assert "-->" in content
    
    def test_process_markdown_already_has_header(self, style_map, tmp_path, fixtures_dir):
        """Test that markdown files with Crown Copyright are skipped."""
        source = fixtures_dir / "with_crown_copyright.md"
        dest = tmp_path / "already_processed.md"
        shutil.copy(source, dest)
        
        # Read original content
        with open(dest, "r") as f:
            original = f.read()
        
        style = style_map[".md"]
        result = process_file(str(dest), style, dry_run=False)
        
        assert result == "already_migrated"
        
        # Content should be unchanged
        with open(dest, "r") as f:
            after = f.read()
        
        assert original == after
    
    def test_process_excluded_markdown_file(self, style_map, tmp_path, fixtures_dir):
        """Test that excluded markdown files like README.md are skipped."""
        source = fixtures_dir / "README.md"
        dest = tmp_path / "README.md"
        shutil.copy(source, dest)
        
        # Read original content
        with open(dest, "r") as f:
            original = f.read()
        
        style = style_map[".md"]
        result = process_file(str(dest), style, dry_run=False)
        
        # Should return excluded
        assert result == "excluded"
        
        # Content should be unchanged
        with open(dest, "r") as f:
            after = f.read()
        
        assert original == after
        assert "Crown Copyright" not in after


class TestFileListProcessing:
    """Tests for batch file processing from a file list."""
    
    def test_process_file_list(self, fixtures_dir, tmp_path, capsys, local_assets_dir):
        """Test processing files from a list."""
        from license_header_migration.migrate import process_file_list
        
        # Create a file list with paths relative to fixtures_dir
        file_list = tmp_path / "files.txt"
        with open(file_list, "w") as f:
            f.write("# Test file list\n")
            f.write(f"{fixtures_dir}/acryl_header.py\n")
            f.write(f"{fixtures_dir}/no_header.py\n")
            f.write("\n")  # Empty line
            f.write(f"# Comment line\n")
            f.write(f"{fixtures_dir}/simple.md\n")
        
        # Copy fixtures to temp location to avoid modifying originals
        import shutil
        test_acryl = tmp_path / "acryl_header.py"
        test_no_header = tmp_path / "no_header.py"
        test_md = tmp_path / "no_header.md"
        
        shutil.copy(fixtures_dir / "acryl_header.py", test_acryl)
        shutil.copy(fixtures_dir / "no_header.py", test_no_header)
        shutil.copy(fixtures_dir / "no_header.md", test_md)
        
        # Update file list with temp paths
        with open(file_list, "w") as f:
            f.write("# Test file list\n")
            f.write(f"{test_acryl}\n")
            f.write(f"{test_no_header}\n")
            f.write(f"{test_md}\n")
        
        # Process the list
        process_file_list(str(file_list), assets_dir=local_assets_dir, dry_run=False)
        
        # Check output contains summary
        captured = capsys.readouterr()
        assert "Added headers to" in captured.out
        assert "Wrapped headers in" in captured.out
        
        # Verify files were actually modified
        with open(test_acryl, "r") as f:
            content = f.read()
            assert "National Digital Twin Programme" in content
        
        with open(test_no_header, "r") as f:
            content = f.read()
            assert "National Digital Twin Programme" in content
        
        with open(test_md, "r") as f:
            content = f.read()
            assert "Crown Copyright" in content
    
    def test_process_file_list_dry_run(self, fixtures_dir, tmp_path, capsys, local_assets_dir):
        """Test dry run mode for file list processing."""
        from license_header_migration.migrate import process_file_list
        import shutil
        
        # Create temp copies
        test_file = tmp_path / "no_header.py"
        shutil.copy(fixtures_dir / "no_header.py", test_file)
        
        # Create file list
        file_list = tmp_path / "files.txt"
        with open(file_list, "w") as f:
            f.write(f"{test_file}\n")
        
        # Get original content
        with open(test_file, "r") as f:
            original = f.read()
        
        # Process with dry run
        process_file_list(str(file_list), assets_dir=local_assets_dir, dry_run=True)
        
        # Check output
        captured = capsys.readouterr()
        assert "Would migrate:" in captured.out
        assert "Added headers to" in captured.out
        
        # Verify file was NOT modified
        with open(test_file, "r") as f:
            after = f.read()
        
        assert original == after
    
    def test_process_file_list_with_errors(self, tmp_path, capsys, local_assets_dir):
        """Test file list processing with non-existent files."""
        from license_header_migration.migrate import process_file_list
        
        # Create file list with non-existent file
        file_list = tmp_path / "files.txt"
        with open(file_list, "w") as f:
            f.write(f"{tmp_path}/nonexistent.py\n")
        
        # Should not crash
        process_file_list(str(file_list), assets_dir=local_assets_dir, dry_run=False)
        
        # Check output contains file not found message
        captured = capsys.readouterr()
        assert "file not found" in captured.out.lower()

    def test_process_file_list_ignores_skywalking_log_lines(self, fixtures_dir, tmp_path, capsys, local_assets_dir):
        """Test SkyWalking INFO/ERROR lines (with ANSI escapes) are ignored as file-list entries."""
        from license_header_migration.migrate import process_file_list

        test_file = tmp_path / "no_header.py"
        shutil.copy(fixtures_dir / "no_header.py", test_file)

        file_list = tmp_path / "skywalking-output.txt"
        file_list.write_text(
            "\x1b[36mINFO\x1b[0m Loading configuration from file: .licenserc.yaml\n"
            "\x1b[36mINFO\x1b[0m Totally checked 14596 files, valid: 11371, invalid: 45, ignored: 3180, fixed: 0\n"
            "\x1b[36mINFO\x1b[0m GITHUB_TOKEN is not set, license-eye won't comment on the pull request\n"
            "\x1b[31mERROR\x1b[0m the following files don't have a valid license header:\n"
            f"{test_file}\n"
            "\x1b[31mERROR\x1b[0m one or more files does not have a valid license header\n",
            encoding="utf-8",
        )

        process_file_list(str(file_list), assets_dir=local_assets_dir, dry_run=False)

        captured = capsys.readouterr()
        assert "Added headers to 1 file(s)" in captured.out
        assert "file not found" not in captured.out.lower()

    def test_process_file_list_extensionless_shell_script(self, tmp_path, capsys, local_assets_dir):
        """Test extensionless shell script is processed via shebang detection."""
        from license_header_migration.migrate import process_file_list

        script_path = tmp_path / "control"
        script_path.write_text(
            "#!/bin/bash\nset -e\necho 'hello'\n",
            encoding="utf-8",
        )

        file_list = tmp_path / "files.txt"
        file_list.write_text(f"{script_path}\n", encoding="utf-8")

        process_file_list(str(file_list), assets_dir=local_assets_dir, dry_run=False)

        captured = capsys.readouterr()
        assert "Added headers to 1 file(s)" in captured.out

        content = script_path.read_text(encoding="utf-8")
        assert content.startswith("#!/bin/bash\n")
        assert "SPDX-License-Identifier: Apache-2.0" in content
        assert "National Digital Twin Programme" in content
