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
import tempfile
import urllib.error
import urllib.request
from fnmatch import fnmatch
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

# OGL header for markdown/doc files (HTML comment style)
CROWN_COPYRIGHT_HEADER = """<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

"""

LICENSE_KEYWORDS = ["copyright", "license", "spdx", "licensed"]

RUNTIME_ASSET_URLS = {
    "languages.yaml": "https://raw.githubusercontent.com/apache/skywalking-eyes/main/assets/languages.yaml",
    "styles.yaml": "https://raw.githubusercontent.com/apache/skywalking-eyes/main/assets/styles.yaml",
}

ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def ensure_trailing_newline(content: str) -> str:
    """Ensure file content ends with a single trailing newline."""
    if not content.endswith("\n"):
        return content + "\n"
    return content


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from terminal-captured text."""
    return ANSI_ESCAPE_RE.sub("", text)


def is_skippable_file_list_line(line: str) -> bool:
    """Return True when a file-list line is metadata/logging, not a path."""
    cleaned = strip_ansi(line).strip()
    if not cleaned:
        return True
    if cleaned.startswith("#"):
        return True

    upper = cleaned.upper()
    if upper.startswith(("INFO ", "ERROR ", "WARN ", "WARNING ")):
        return True
    if "don't have a valid license header" in cleaned:
        return True
    if "one or more files does not have a valid license header" in cleaned:
        return True

    return False


def resolve_asset_paths(assets_dir: Optional[str]) -> Optional[Tuple[str, str]]:
    """Resolve paths for languages.yaml and styles.yaml.

    If assets_dir is provided, reads from that local directory.
    Otherwise downloads runtime copies from GitHub into a temp cache dir.
    """
    if assets_dir:
        languages_path = os.path.join(assets_dir, "languages.yaml")
        styles_path = os.path.join(assets_dir, "styles.yaml")

        if not os.path.exists(languages_path):
            print(f"\n{'='*70}")
            print("❌ ERROR: ASSETS NOT FOUND")
            print(f"{'='*70}")
            print(f"Missing: {languages_path}")
            print(f"Assets directory: {assets_dir}")
            print("\nThe assets directory must contain:")
            print("  - languages.yaml")
            print("  - styles.yaml")
            print(f"{'='*70}\n")
            return None

        if not os.path.exists(styles_path):
            print(f"\n{'='*70}")
            print("❌ ERROR: ASSETS NOT FOUND")
            print(f"{'='*70}")
            print(f"Missing: {styles_path}")
            print(f"Assets directory: {assets_dir}")
            print(f"{'='*70}\n")
            return None

        return languages_path, styles_path

    cache_dir = Path(tempfile.gettempdir()) / "licence-header-utils-assets"
    cache_dir.mkdir(parents=True, exist_ok=True)

    languages_path = str(cache_dir / "languages.yaml")
    styles_path = str(cache_dir / "styles.yaml")

    print(f"\n{'='*70}")
    print("DOWNLOADING RUNTIME ASSETS")
    print(f"{'='*70}")
    print("Source: apache/skywalking-eyes")

    try:
        for file_name, url in RUNTIME_ASSET_URLS.items():
            destination = cache_dir / file_name
            with urllib.request.urlopen(url, timeout=20) as response:
                content = response.read()
            destination.write_bytes(content)
            print(f"✓ Downloaded: {file_name}")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"\n{'='*70}")
        print("❌ ERROR: FAILED TO DOWNLOAD ASSETS")
        print(f"{'='*70}")
        print("Could not download required runtime assets from GitHub.")
        print(f"Error: {exc}")
        print("Pass --assets-dir to use local copies if needed.")
        print(f"{'='*70}\n")
        return None

    print(f"Cache directory: {cache_dir}")
    print(f"{'='*70}\n")

    return languages_path, styles_path


def load_yaml(path: str) -> dict:
    """Load and parse a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_license_configs(repo_root: str) -> Tuple[Optional[dict], Optional[dict]]:
    """Load license configuration files.
    
    Args:
        repo_root: Root directory of the repository
        
    Returns:
        Tuple of (markdown_config, general_config)
    """
    md_config_path = os.path.join(repo_root, '.licenserc-markdown.yaml')
    general_config_path = os.path.join(repo_root, '.licenserc.yaml')
    
    print(f"\n{'='*70}")
    print("LOADING LICENSE CONFIGURATIONS")
    print(f"{'='*70}")
    print(f"Repository root: {repo_root}")
    
    md_config = None
    general_config = None
    
    if os.path.exists(md_config_path):
        md_config = load_yaml(md_config_path)
        print(f"✓ Loaded markdown config: {md_config_path}")
    else:
        print(f"⚠ WARNING: Markdown config not found: {md_config_path}")
        print("  Using fallback markdown exclusion list")
    
    if os.path.exists(general_config_path):
        general_config = load_yaml(general_config_path)
        print(f"✓ Loaded general config: {general_config_path}")
    else:
        print(f"⚠ WARNING: General config not found: {general_config_path}")
        print("  No file exclusions will be applied (except hardcoded markdown files)")
    
    print(f"{'='*70}\n")
    
    return md_config, general_config


def matches_pattern(file_path: str, patterns: list) -> bool:
    """Check if file path matches any glob pattern.
    
    Args:
        file_path: Full or relative file path
        patterns: List of glob patterns
        
    Returns:
        True if file matches any pattern
    """
    if not patterns:
        return False
        
    file_name = os.path.basename(file_path)
    
    for pattern in patterns:
        # Try matching against full path and just filename
        if fnmatch(file_path, pattern) or fnmatch(file_name, pattern):
            return True
    return False


def should_exclude_file(file_path: str, md_config: Optional[dict], general_config: Optional[dict]) -> Tuple[bool, bool]:
    """Check if file should be excluded based on license configs.
    
    Args:
        file_path: Path to the file
        md_config: Markdown license config
        general_config: General license config
        
    Returns:
        Tuple of (should_exclude, is_markdown)
    """
    file_path_obj = Path(file_path)
    file_name = file_path_obj.name
    
    # Check markdown config first
    if md_config and 'header' in md_config:
        header = md_config['header']
        md_paths = header.get('paths', [])
        md_ignore = header.get('paths-ignore', [])
        
        # Check if it's a markdown file
        is_markdown = matches_pattern(file_path, md_paths)
        
        if is_markdown:
            # Check if excluded in markdown config
            if matches_pattern(file_path, md_ignore):
                return (True, True)
            return (False, True)
    else:
        # Fallback: check by extension if no config available
        is_markdown = file_path_obj.suffix.lower() in {'.md', '.mdx', '.markdown', '.mdown', '.mdwn'}
        if is_markdown:
            # Fallback excluded markdown files (if no config)
            excluded_names = {
                'LICENSE.md', 'NOTICE.md', 'ACKNOWLEDGEMENTS.md', 'CHANGELOG.md',
                'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md', 'MAINTAINERS.md',
                'OGL_LICENSE.md', 'README.md', 'SECURITY.md'
            }
            if file_name in excluded_names:
                return (True, True)
            return (False, True)
    
    # Check general config for exclusions
    if general_config and 'header' in general_config:
        header = general_config['header']
        general_ignore = header.get('paths-ignore', [])
        
        if matches_pattern(file_path, general_ignore):
            return (True, False)
    
    return (False, False)


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
    fallback_additions_path = Path(__file__).parent.parent.parent / "assets" / "styles-additions.yaml"

    additions_source = additions_path if additions_path.exists() else fallback_additions_path
    if additions_source.exists():
        additions = load_yaml(str(additions_source))
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
    
    markdown_exts = {'.md', '.mdx', '.markdown', '.mdown', '.mdwn'}

    for lang, props in languages_yaml.items():
        if "extensions" not in props:
            continue
            
        style_id = props.get("comment_style_id")
        if style_id and style_id in style_ids:
            for ext in props["extensions"]:
                if ext.lower() in markdown_exts and "PlainText" in style_ids:
                    ext_to_style[ext] = style_ids["PlainText"]
                else:
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
    
    has_block_comment_style = style.get("end") and style.get("end") != style.get("start")
    header_separator = "\n" if has_block_comment_style else "\n\n"

    final_content = pre_header
    if insert_after_block and not final_content.endswith("\n"):
        final_content += "\n"
    final_content += formatted_header + header_separator + post_header
    
    return final_content


def add_crown_copyright_to_markdown(content: str) -> Optional[str]:
    """Add Crown Copyright header to a markdown file.
    
    Args:
        content: Original markdown file content
        
    Returns:
        Content with Crown Copyright header added, or None if already present
    """
    # Skip files that already have the markdown/doc OGL header
    if "SPDX-License-Identifier: OGL-UK-3.0" in content[:500] and "National Digital Twin Programme" in content[:800]:
        return None
    
    # Skip files that already have older OGL license wording
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
        # Make leading spaces in end marker optional to match both " */" and "*/"
        end_marker = style["end"].lstrip()
        start_marker = style["start"]
        block_pattern = re.compile(
            re.escape(start_marker) + r'[\s\S]*?' + r'\s*' + re.escape(end_marker),
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

    # Ensure the shebang (or any "after" block) is separated from the header
    # by a newline.  The "after" regex uses $ which stops before \n, so
    # insert_at points to the char just before the newline; without this
    # guard the header is concatenated directly onto the shebang line.
    if insert_after_block and not pre_header.endswith("\n"):
        pre_header += "\n"
        after_header = after_header.lstrip("\n")

    formatted_spdx = format_comment(SPDX_ID, style, multiline=False)
    formatted_preamble = format_comment(HEADER_PREAMBLE_TEXT, style, multiline=True)
    formatted_footer = format_comment(FOOTER_MODIFIED_TEXT, style, multiline=True)
    blank_comment = format_comment("", style, multiline=False)

    new_header_section = f"{formatted_spdx}\n{formatted_preamble}\n{blank_comment}\n"

    final_content = pre_header
    final_content += after_header + new_header_section + license_block + "\n" + formatted_footer + post_header

    return final_content


def process_file(file_path: str, style: dict, dry_run: bool = False, md_config: Optional[dict] = None, general_config: Optional[dict] = None) -> Optional[str]:
    """Process a single file, migrating its license header.
    
    Args:
        file_path: Path to the file to process
        style: Comment style configuration
        dry_run: If True, don't write changes to disk
        md_config: Markdown license config (optional)
        general_config: General license config (optional)
        
    Returns:
        "added" - header was added to file without one
        "wrapped" - existing Acryl header was wrapped
        "excluded" - file filtered out by config
        "already_migrated" - file already has correct header
        "decode_error" - can't read file (encoding issue)
    """
    # Check if file should be excluded based on configs
    should_exclude, is_markdown = should_exclude_file(file_path, md_config, general_config)
    if should_exclude:
        return "excluded"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        return "decode_error"
    
    # Determine the action type
    action_type = None
    has_existing_header = is_valid_license_header(content[:500]) if not is_markdown else False
    
    # Handle markdown files separately with Crown Copyright header
    if is_markdown:
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
        return "already_migrated"

    migrated_content = ensure_trailing_newline(migrated_content)
    
    if not dry_run:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(migrated_content)
        print(f"Migrated: {file_path}")
    else:
        print(f"Would migrate: {file_path}")
    
    return action_type


def resolve_style_for_file(file_path: str, ext_to_style: Dict[str, dict]) -> Optional[dict]:
    """Resolve comment style for a file using extension, then shebang fallback."""
    _, ext = os.path.splitext(file_path)
    style = ext_to_style.get(ext) or ext_to_style.get(ext.lower())
    if style:
        return style

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
    except (OSError, UnicodeDecodeError):
        return None

    if first_line.startswith("#!"):
        shebang = first_line.lower()
        if any(shell in shebang for shell in ("bash", "sh", "zsh", "ksh", "dash", "ash")):
            return ext_to_style.get(".sh") or {
                "id": "Hashtag",
                "start": "#",
                "middle": "#",
                "end": "#",
                "after": "(?m)^#!.*$",
            }

    return None


def process_file_list(file_list_path: str, assets_dir: Optional[str] = None, dry_run: bool = False, repo_root: Optional[str] = None):
    """Process files listed in a text file.
    
    Args:
        file_list_path: Path to text file containing one file path per line
        assets_dir: Directory containing languages.yaml and styles.yaml
        dry_run: If True, don't write changes to disk
        repo_root: Root directory of repository (for finding .licenserc files)
    """
    if repo_root is None:
        # Default to parent directory of licence-header-utils
        module_dir = Path(__file__).parent
        repo_root = str(module_dir.parent.parent.parent)

    asset_paths = resolve_asset_paths(assets_dir)
    if not asset_paths:
        return

    languages_path, styles_path = asset_paths
    
    # Load license configs
    md_config, general_config = load_license_configs(repo_root)
    
    languages_yaml = load_yaml(languages_path)
    styles_yaml = load_styles_with_additions(styles_path)
    ext_to_style = build_extension_style_map(languages_yaml, styles_yaml)
    
    # Read file list
    with open(file_list_path, 'r', encoding='utf-8') as f:
        file_paths = []
        for line in f:
            if is_skippable_file_list_line(line):
                continue
            file_paths.append(strip_ansi(line).strip())
    
    stats = {
        'added': 0,
        'wrapped': 0,
        'excluded': 0,
        'already_migrated': 0,
        'decode_error': 0,
        'file_not_found': 0,
        'no_style': 0
    }
    
    for file_path in file_paths:
        # Skip if file doesn't exist
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            stats['file_not_found'] += 1
            continue
        
        style = resolve_style_for_file(file_path, ext_to_style)
        
        if not style:
            stats['no_style'] += 1
            continue
        
        try:
            result = process_file(file_path, style, dry_run, md_config, general_config)
            if result in stats:
                stats[result] += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            stats['decode_error'] += 1
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Added headers to {stats['added']} file(s)")
    print(f"Wrapped headers in {stats['wrapped']} file(s)")
    
    # Breakdown of skipped files
    total_skipped = (stats['excluded'] + stats['already_migrated'] + 
                     stats['no_style'] + stats['file_not_found'] + stats['decode_error'])
    if total_skipped > 0:
        print(f"\nSkipped {total_skipped} file(s):")
        if stats['excluded'] > 0:
            print(f"  - {stats['excluded']} excluded by config (.licenserc)")
        if stats['already_migrated'] > 0:
            print(f"  - {stats['already_migrated']} already have correct headers")
        if stats['no_style'] > 0:
            print(f"  - {stats['no_style']} unsupported file type")
        if stats['file_not_found'] > 0:
            print(f"  - {stats['file_not_found']} file not found")
        if stats['decode_error'] > 0:
            print(f"  - {stats['decode_error']} encoding errors")
    
    print(f"\nTotal processed: {stats['added'] + stats['wrapped']} file(s)")
    print("="*60)


def main(root_dir: str = "./", assets_dir: Optional[str] = None, dry_run: bool = False, repo_root: Optional[str] = None):
    """Main function to process all files in a directory tree.
    
    Args:
        root_dir: Root directory to start processing from
        assets_dir: Directory containing languages.yaml and styles.yaml
        dry_run: If True, don't write changes to disk
        repo_root: Root directory of repository (for finding .licenserc files)
    """
    if repo_root is None:
        # Default to parent directory of licence-header-utils
        module_dir = Path(__file__).parent
        repo_root = str(module_dir.parent.parent.parent)

    asset_paths = resolve_asset_paths(assets_dir)
    if not asset_paths:
        return

    languages_path, styles_path = asset_paths
    
    # Load license configs
    md_config, general_config = load_license_configs(repo_root)
    
    languages_yaml = load_yaml(languages_path)
    styles_yaml = load_styles_with_additions(styles_path)
    ext_to_style = build_extension_style_map(languages_yaml, styles_yaml)
    
    stats = {
        'added': 0,
        'wrapped': 0,
        'excluded': 0,
        'already_migrated': 0,
        'decode_error': 0
    }
    
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and exclude node_modules and build folders
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "build")]
        
        for file in files:
            full_path = os.path.join(root, file)
            style = resolve_style_for_file(full_path, ext_to_style)
            if style:
                result = process_file(full_path, style, dry_run, md_config, general_config)
                if result in stats:
                    stats[result] += 1
    
    # Print summary
    total_processed = stats['added'] + stats['wrapped']
    total_skipped = stats['excluded'] + stats['already_migrated'] + stats['decode_error']
    
    print(f"\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Added headers to {stats['added']} file(s)")
    print(f"Wrapped headers in {stats['wrapped']} file(s)")
    
    if total_skipped > 0:
        print(f"\nSkipped {total_skipped} file(s):")
        if stats['excluded'] > 0:
            print(f"  - {stats['excluded']} excluded by config")
        if stats['already_migrated'] > 0:
            print(f"  - {stats['already_migrated']} already have correct headers")
        if stats['decode_error'] > 0:
            print(f"  - {stats['decode_error']} encoding errors")
    
    print(f"\nTotal processed: {total_processed} file(s)")
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
    parser.add_argument(
        '--repo-root',
        help='Root directory of repository (for finding .licenserc files)'
    )
    
    args = parser.parse_args()
    
    if args.file_list:
        process_file_list(args.path, assets_dir=args.assets_dir, dry_run=args.dry_run, repo_root=args.repo_root)
    else:
        main(root_dir=args.path, assets_dir=args.assets_dir, dry_run=args.dry_run, repo_root=args.repo_root)

