# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

"""License header migration tool for NDT.

This module provides functionality to migrate license headers from Acryl Data format
to National Digital Twin Programme format.
"""
import argparse
import os
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
import yaml


# Constants for license headers
HEADER_PREAMBLE_TEXT = (
    "Originally developed by Acryl Data, Inc.; subsequently adapted, enhanced, "
    "and maintained by the National Digital Twin Programme."
)
SPDX_ID = "SPDX-License-Identifier: Apache-2.0"

FOOTER_MODIFIED_TEXT = """
This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
"""

# Header for files with no existing license
NDT_ONLY_HEADER_TEXT = """SPDX-License-Identifier: Apache-2.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme."""

# Crown Copyright header for markdown files
CROWN_COPYRIGHT_HEADER = """**SPDX-License-Identifier:** OGL-UK-3.0

**Copyright Owner:** © Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

© Crown Copyright 2025. This work has been developed by the National Digital Twin Programme and is legally attributed to the Department for Business and Trade (UK) as the governing entity.

Licensed under the Open Government Licence v3.0.

---
"""

# Markdown files that should be excluded from header addition
EXCLUDED_MARKDOWN_FILES = {
    'LICENSE.md',
    'NOTICE.md',
    'ACKNOWLEDGEMENTS.md',
    'CHANGELOG.md',
    'CODE_OF_CONDUCT.md',
    'CONTRIBUTING.md',
    'MAINTAINERS.md',
    'OGL_LICENSE.md',
    'README.md',
    'SECURITY.md',
}

LICENSE_KEYWORDS = ["copyright", "license", "spdx", "licensed"]


def load_yaml(path: str) -> dict:
    """Load and parse a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_styles_with_additions(styles_path: str) -> list:
    """Load styles.yaml and merge with styles-additions.yaml if it exists.
    
    This allows us to add custom styles without modifying the upstream styles.yaml
    which can be safely re-downloaded from apache/skywalking-eyes.
    
    Args:
        styles_path: Path to the main styles.yaml file
        
    Returns:
        List of style definitions (merged)
    """
    styles = load_yaml(styles_path)
    
    # Try to load additions file
    additions_path = Path(styles_path).parent / "styles-additions.yaml"
    if additions_path.exists():
        additions = load_yaml(str(additions_path))
        if additions and isinstance(additions, list):
            styles.extend(additions)
    
    return styles


def build_extension_style_map(languages_yaml: dict, styles_yaml: list) -> Dict[str, dict]:
    """Build a mapping from file extensions to comment styles.
    
    Args:
        languages_yaml: Dictionary of language configurations
        styles_yaml: List of comment style configurations
        
    Returns:
        Dictionary mapping file extensions to style dictionaries
    """
    ext_to_style = {}
    style_ids = {s["id"]: s for s in styles_yaml if "id" in s}
    
    for lang, props in languages_yaml.items():
        if "extensions" not in props:
            continue
            
        style_id = props.get("comment_style_id")
        if style_id and style_id in style_ids:
            for ext in props["extensions"]:
                ext_to_style[ext] = style_ids[style_id]
        else:
            # Fallback based on ace_mode
            ace = props.get("ace_mode", "")
            for ext in props["extensions"]:
                if ace in ("c_cpp", "java", "css", "csharp", "scala"):
                    ext_to_style[ext] = style_ids.get("SlashAsterisk")
                elif ace == "markdown":
                    # Use PlainText for markdown files
                    ext_to_style[ext] = style_ids.get("PlainText")
                elif ace in ("xml", "html"):
                    ext_to_style[ext] = style_ids.get("AngleBracket")
                elif ace in ("python", "ruby", "sh", "yaml"):
                    ext_to_style[ext] = style_ids.get("Hashtag")
                elif ace == "actionsheet":
                    ext_to_style[ext] = style_ids.get("PythonDocStringStyle")
                elif ace == "php":
                    ext_to_style[ext] = style_ids.get("PhpTag")
                else:
                    ext_to_style[ext] = style_ids.get("DoubleSlash")
    
    return ext_to_style


def format_comment(text: str, style: dict, multiline: bool = False) -> str:
    """Format text as a comment using the given style.
    
    Args:
        text: The text to format as a comment
        style: Comment style configuration
        multiline: Whether to use multiline comment formatting
        
    Returns:
        Formatted comment string
    """
    if not text.strip():
        return style.get("start", "")
    
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    has_different_end = style.get("end") and style["end"] != style["start"]
    
    if has_different_end and multiline and "middle" in style and style["middle"]:
        # Multi-line block comment with middle marker (/* ... */)
        body = ""
        for line in lines:
            body += f"{style['middle']} {line}\n"
        return f"{style['start']}\n{body}{style['end']}"
    elif has_different_end:
        # Multi-line block comment without middle or single line
        if len(lines) == 1:
            return f"{style['start']} {lines[0]} {style['end']}"
        else:
            return f"{style['start']}\n{chr(10).join(lines)}\n{style['end']}"
    elif style.get("start"):
        # Single-line comment style (# or //)
        return "\n".join([f"{style['start']} {line}" for line in lines])
    
    return text.strip()


def is_valid_license_header(content_chunk: str) -> bool:
    """Check if a content chunk contains license header keywords."""
    lower_content = content_chunk.lower()
    return any(kw in lower_content for kw in LICENSE_KEYWORDS)


def find_after_block(style: dict, content: str) -> Tuple[Optional[int], Optional[str]]:
    """Find and return the 'after' block if present in the file.
    
    Returns:
        Tuple of (end_index, block_content) or (None, None) if not found
    """
    after_regex = style.get("after")
    if not after_regex:
        return None, None
        
    try:
        after_pat = re.compile(after_regex, re.MULTILINE)
    except Exception:
        return None, None
        
    match = after_pat.search(content[:1024])
    if match:
        return match.end(), match.group(0)
    return None, None


def add_ndt_header_to_file(content: str, style: dict) -> Optional[str]:
    """Add NDT license header to a file without an existing license header.
    
    Args:
        content: Original file content
        style: Comment style configuration
        
    Returns:
        Content with NDT header added, or None if already has NDT header
    """
    # Skip files already processed
    if "National Digital Twin Programme" in content and "SPDX-License-Identifier" in content[:200]:
        return None
    
    # Determine where to insert header
    insert_at = 0
    insert_after_block = ""
    
    after_idx, after_block = find_after_block(style, content)
    if after_idx:
        insert_at = after_idx
        insert_after_block = after_block
    else:
        leading_ws = re.match(r'^\s*', content)
        insert_at = leading_ws.end() if leading_ws else 0
    
    # Format the NDT-only header
    formatted_header = format_comment(NDT_ONLY_HEADER_TEXT, style, multiline=True)
    
    # Build the new content
    pre_header = content[:insert_at]
    post_header = content[insert_at:]
    
    final_content = pre_header
    if insert_after_block:
        final_content += insert_after_block + "\n"
    final_content += formatted_header + "\n\n" + post_header
    
    return final_content


def add_crown_copyright_to_markdown(content: str) -> Optional[str]:
    """Add Crown Copyright header to a markdown file.
    
    Args:
        content: Original markdown file content
        
    Returns:
        Content with Crown Copyright header added, or None if already present
    """
    # Skip files already processed
    if "Crown Copyright 2025" in content[:500]:
        return None
    
    # Skip files that already have OGL license
    if "Open Government Licence" in content[:500]:
        return None
    
    # Add header at the top
    return CROWN_COPYRIGHT_HEADER + content


def migrate_file_content(content: str, style: dict) -> Optional[str]:
    """Migrate the license header in file content.
    
    Args:
        content: Original file content
        style: Comment style configuration
        
    Returns:
        Migrated content or None if no migration needed/possible
    """
    # Skip files already processed
    if "National Digital Twin Programme" in content and "SPDX-License-Identifier" in content[:200]:
        return None

    # Determine where to insert header
    insert_at = 0
    insert_after_block = ""
    
    after_idx, after_block = find_after_block(style, content)
    if after_idx:
        insert_at = after_idx
        insert_after_block = after_block
    else:
        leading_ws = re.match(r'^\s*', content)
        insert_at = leading_ws.end() if leading_ws else 0

    # Find existing header comment block
    if style.get("end") and style["end"] != style["start"]:
        # Multi-line comment style
        block_pattern = re.compile(
            re.escape(style["start"]) + r'[\s\S]*?' + re.escape(style["end"]),
            re.MULTILINE
        )
        match = block_pattern.search(content, insert_at)
    else:
        # Single-line comment style
        remaining_content = content[insert_at:]
        lines = remaining_content.split('\n')
        comment_lines = []
        start_idx = insert_at
        current_pos = insert_at
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(style["start"]):
                comment_lines.append(line)
                current_pos += len(line) + 1
            elif stripped == "":
                comment_lines.append(line)
                current_pos += len(line) + 1
            else:
                break
        
        if comment_lines:
            class MockMatch:
                def __init__(self, start, end, text):
                    self._start = start
                    self._end = end
                    self._text = text
                def start(self):
                    return self._start
                def end(self):
                    return self._end
                def group(self, x):
                    return self._text
            
            header_block = '\n'.join(comment_lines)
            match = MockMatch(start_idx, current_pos - 1, header_block)
        else:
            match = None
    
    # Validate match is near top of file
    if not match or match.start() > insert_at + 800:
        # No existing license header found - add NDT-only header
        return add_ndt_header_to_file(content, style)
        
    header_block = match.group(0)
    if not is_valid_license_header(header_block):
        # Found comment block but it's not a license header - add NDT-only header
        return add_ndt_header_to_file(content, style)

    # Build new content
    start = match.start()
    end = match.end()
    pre_header = content[:insert_at]
    after_header = content[insert_at:start]
    license_block = content[start:end]
    post_header = content[end:]

    formatted_spdx = format_comment(SPDX_ID, style, multiline=False)
    formatted_preamble = format_comment(HEADER_PREAMBLE_TEXT, style, multiline=True)
    formatted_footer = format_comment(FOOTER_MODIFIED_TEXT, style, multiline=True)
    blank_comment = format_comment("", style, multiline=False)

    new_header_section = f"{formatted_spdx}\n{formatted_preamble}\n{blank_comment}\n"

    final_content = pre_header
    if insert_after_block:
        final_content += insert_after_block + "\n"
    final_content += after_header + new_header_section + license_block + "\n" + formatted_footer + post_header

    return final_content


def process_file(file_path: str, style: dict, dry_run: bool = False) -> Optional[str]:
    """Process a single file, migrating its license header.
    
    Args:
        file_path: Path to the file to process
        style: Comment style configuration
        dry_run: If True, don't write changes to disk
        
    Returns:
        "added" if header was added to file without one
        "wrapped" if existing Acryl header was wrapped
        None if file was skipped (already migrated, excluded, etc.)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return None
    
    # Check if this is a markdown file
    file_path_obj = Path(file_path)
    is_markdown = file_path_obj.suffix.lower() in {'.md', '.mdx', '.markdown', '.mdown', '.mdwn'}
    
    # Check if this is an excluded markdown file
    if is_markdown and file_path_obj.name in EXCLUDED_MARKDOWN_FILES:
        return None
    
    # Determine the action type
    action_type = None
    has_existing_header = is_valid_license_header(content[:500]) if not is_markdown else False
    
    # Handle markdown files separately with Crown Copyright header
    if is_markdown and style.get('id') == 'PlainText':
        migrated_content = add_crown_copyright_to_markdown(content)
        if migrated_content is not None:
            action_type = "added"
    else:
        # Regular migration for code files
        migrated_content = migrate_file_content(content, style)
        if migrated_content is not None:
            # Determine if we wrapped an existing header or added a new one
            action_type = "wrapped" if has_existing_header else "added"
    
    if migrated_content is None:
        return None
    
    if not dry_run:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(migrated_content)
        print(f"Migrated: {file_path}")
    else:
        print(f"Would migrate: {file_path}")
    
    return action_type
    return action_type


def process_file_list(file_list_path: str, assets_dir: Optional[str] = None, dry_run: bool = False):
    """Process files listed in a text file.
    
    Args:
        file_list_path: Path to text file containing one file path per line
        assets_dir: Directory containing languages.yaml and styles.yaml
        dry_run: If True, don't write changes to disk
    """
    if assets_dir is None:
        # Default to assets directory relative to this module
        module_dir = Path(__file__).parent
        assets_dir = str(module_dir.parent.parent / "assets")
    
    languages_path = os.path.join(assets_dir, "languages.yaml")
    styles_path = os.path.join(assets_dir, "styles.yaml")
    
    languages_yaml = load_yaml(languages_path)
    styles_yaml = load_styles_with_additions(styles_path)
    ext_to_style = build_extension_style_map(languages_yaml, styles_yaml)
    
    # Read file list
    with open(file_list_path, 'r', encoding='utf-8') as f:
        file_paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    stats = {
        'added': 0,
        'wrapped': 0,
        'skipped': 0,
        'errors': 0
    }
    
    for file_path in file_paths:
        # Skip if file doesn't exist
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            stats['errors'] += 1
            continue
        
        _, ext = os.path.splitext(file_path)
        style = ext_to_style.get(ext)
        
        if not style:
            stats['skipped'] += 1
            continue
        
        try:
            result = process_file(file_path, style, dry_run)
            if result == "added":
                stats['added'] += 1
            elif result == "wrapped":
                stats['wrapped'] += 1
            else:
                stats['skipped'] += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            stats['errors'] += 1
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Added headers to {stats['added']} file(s)")
    print(f"Wrapped headers in {stats['wrapped']} file(s)")
    print(f"Skipped {stats['skipped']} file(s)")
    if stats['errors'] > 0:
        print(f"Errors: {stats['errors']} file(s)")
    print(f"Total processed: {stats['added'] + stats['wrapped']} file(s)")
    print("="*60)


def main(root_dir: str = "./", assets_dir: Optional[str] = None, dry_run: bool = False):
    """Main function to process all files in a directory tree.
    
    Args:
        root_dir: Root directory to start processing from
        assets_dir: Directory containing languages.yaml and styles.yaml
        dry_run: If True, don't write changes to disk
    """
    if assets_dir is None:
        # Default to assets directory relative to this module
        module_dir = Path(__file__).parent
        assets_dir = str(module_dir.parent.parent / "assets")
    
    languages_path = os.path.join(assets_dir, "languages.yaml")
    styles_path = os.path.join(assets_dir, "styles.yaml")
    
    languages_yaml = load_yaml(languages_path)
    styles_yaml = load_styles_with_additions(styles_path)
    ext_to_style = build_extension_style_map(languages_yaml, styles_yaml)
    
    stats = {
        'added': 0,
        'wrapped': 0,
        'skipped': 0
    }
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and exclude node_modules and build folders
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "build")]
        
        for file in files:
            _, ext = os.path.splitext(file)
            style = ext_to_style.get(ext)
            if style:
                result = process_file(os.path.join(root, file), style, dry_run)
                if result == "added":
                    stats['added'] += 1
                elif result == "wrapped":
                    stats['wrapped'] += 1
                else:
                    stats['skipped'] += 1
    
    # Print summary
    total_processed = stats['added'] + stats['wrapped']
    print(f"\n" + "="*60)
    print(f"Processed {total_processed} file(s)")
    if total_processed > 0:
        print(f"  - Added headers: {stats['added']}")
        print(f"  - Wrapped headers: {stats['wrapped']}")
    print("="*60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Migrate license headers to NDT format"
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='./',
        help='Directory to process or file list (with --file-list)'
    )
    parser.add_argument(
        '--file-list',
        action='store_true',
        help='Treat path as a text file containing list of files to process'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    parser.add_argument(
        '--assets-dir',
        help='Directory containing languages.yaml and styles.yaml'
    )
    
    args = parser.parse_args()
    
    if args.file_list:
        process_file_list(args.path, assets_dir=args.assets_dir, dry_run=args.dry_run)
    else:
        main(root_dir=args.path, assets_dir=args.assets_dir, dry_run=args.dry_run)

