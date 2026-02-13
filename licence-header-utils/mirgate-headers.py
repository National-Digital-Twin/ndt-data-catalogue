# SPDX-License-Identifier: Apache-2.0
#
# © Crown Copyright 2025. This work has been developed by the National Digital Twin
# Programme and is legally attributed to the Department for Business and Trade (UK) as the governing
# entity

import os
import re
import yaml  # pip install pyyaml

LANGUAGES_YAML_PATH = "assets/languages.yaml" #  https://github.com/apache/skywalking-eyes/blob/main/assets/languages.yaml
STYLES_YAML_PATH = "assets/styles.yaml"  # https://github.com/apache/skywalking-eyes/blob/main/assets/styles.yaml

HEADER_PREAMBLE_TEXT = "Originally developed by Acryl Data, Inc.; subsequently adapted, enhanced, and maintained by the National Digital Twin Programme."
SPDX_ID = "SPDX-License-Identifier: Apache-2.0"

FOOTER_MODIFIED_TEXT = """
This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
"""

LICENSE_KEYWORDS = ["copyright", "license", "spdx", "licensed"]

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_extension_style_map(languages_yaml, styles_yaml):
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
            ace = props.get("ace_mode", "")
            for ext in props["extensions"]:
                if ace in ("c_cpp","java","css","csharp","scala"):
                    ext_to_style[ext] = style_ids.get("SlashAsterisk")
                elif ace in ("xml", "html", "markdown"):
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

def format_comment(text, style, multiline=False):
    # Handle empty text for blank comment lines
    if not text.strip():
        return style.get("start", "")
    
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    
    # Check if this is a multi-line comment style with different start/end
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

def is_valid_license_header(content_chunk):
    lower_content = content_chunk.lower()
    return any(kw in lower_content for kw in LICENSE_KEYWORDS)

def find_after_block(style, content):
    """Returns (end_index, block_content) of after block if found, else (None, None)."""
    after_regex = style.get("after")
    if not after_regex:
        return None, None
    try:
        # The regex in styles.yaml is already a Python regex string.
        after_pat = re.compile(after_regex, re.MULTILINE)
    except Exception:
        return None, None
    # Only search top of file (~first 1K chars)
    match = after_pat.search(content[:1024])
    if match:
        return match.end(), match.group(0)
    return None, None

def process_file(file_path, style):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Skip binary files
        return
    # Skip files that have already been processed or don't need processing
    if "National Digital Twin Programme" in content and "SPDX-License-Identifier" in content[:200]:
        return

    # Where to insert header:
    insert_at = 0
    insert_after_block = ""
    # If 'after' is present, find it
    after_idx, after_block = find_after_block(style, content)
    if after_idx:
        insert_at = after_idx
        insert_after_block = after_block
    else:
        # Otherwise, just start at the first non-whitespace
        leading_ws = re.match(r'^\s*', content)
        insert_at = leading_ws.end() if leading_ws else 0

    # Search for the header comment block after this (skip documentation, only top)
    if style.get("end") and style["end"] != style["start"]:
        # Multi-line comment style (/* ... */)
        block_pattern = re.compile(re.escape(style["start"]) + r'[\s\S]*?' + re.escape(style["end"]), re.MULTILINE)
        match = block_pattern.search(content, insert_at)
    else:
        # Single-line comment style (# or //)
        # Look for consecutive comment lines
        remaining_content = content[insert_at:]
        lines = remaining_content.split('\n')
        comment_lines = []
        start_idx = insert_at
        current_pos = insert_at
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(style["start"]):
                comment_lines.append(line)
                current_pos += len(line) + 1  # +1 for newline
            elif stripped == "":
                comment_lines.append(line)
                current_pos += len(line) + 1
            else:
                break
        
        if comment_lines:
            # Create a match-like object
            header_block = '\n'.join(comment_lines)
            match_start = start_idx
            match_end = current_pos - 1  # -1 to not include the last newline
            
            class MockMatch:
                def start(self):
                    return match_start
                def end(self):
                    return match_end
                def group(self, x):
                    return header_block
            
            match = MockMatch()
        else:
            match = None
    
    # Accept only if it's still near the top
    if not match or match.start() > insert_at + 800:
        return
    header_block = match.group(0)
    if not is_valid_license_header(header_block):
        return

    print(f"Migrating: {file_path}")
    start = match.start()
    end = match.end()
    pre_header = content[:insert_at]
    after_header = content[insert_at:start]
    license_block = content[start:end]
    post_header = content[end:]

    formatted_spdx = format_comment(SPDX_ID, style, multiline=False)
    formatted_preamble = format_comment(HEADER_PREAMBLE_TEXT, style, multiline=True)
    formatted_footer = format_comment(FOOTER_MODIFIED_TEXT, style, multiline=True)
    
    # Add blank comment line after preamble
    blank_comment = format_comment("", style, multiline=False)

    new_header_section = f"{formatted_spdx}\n{formatted_preamble}\n{blank_comment}\n"

    final_content = pre_header
    if insert_after_block:
        final_content += insert_after_block + "\n"
    final_content += after_header + new_header_section + license_block + "\n" + formatted_footer + post_header

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)

def main():
    languages_yaml = load_yaml(LANGUAGES_YAML_PATH)
    styles_yaml = load_yaml(STYLES_YAML_PATH)
    ext_to_style = build_extension_style_map(languages_yaml, styles_yaml)
    root_dir = "./"
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and exclude node_modules and build folders
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "build")]
        for file in files:
            _, ext = os.path.splitext(file)
            style = ext_to_style.get(ext)
            if style:
                process_file(os.path.join(root, file), style)

if __name__ == "__main__":
    main()