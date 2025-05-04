import argparse
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Any


def main():
    _log_info("Markdown findings to SysReptor JSON converter, by @tiagomanunes")
    _log_warn(
        "This script is provided as-is."
        "Use at your own risk, and definitely don't blame SysReptor for any issues\n"
    )
    args = _parse_args()

    md_files = _find_markdown_files(args.path, args.recurse)
    if not md_files:
        _log_error("No markdown files found, quitting!")
        sys.exit(1)

    aggregate_results = []
    overwrite_settings = {
        "always": args.overwrite,
        "never": False,
    }
    proceed_settings = {
        "always": False,
    }
    abort = False

    _log_info(f"Found {len(md_files)} markdown file(s) to process")

    for md_file in md_files:
        _log_start(f"Processing file: '{md_file}'")
        result = _process_markdown_file(md_file, args.strict, args.custom_fields)

        if result is None:
            if _should_abort(proceed_settings):
                abort = True
                break
            else:
                continue

        aggregate_results.append(result)

        if not args.aggregate_only:
            output_file = md_file.with_suffix('.json')
            if _should_write(output_file, overwrite_settings):
                _write_json(output_file, result)

    aggregate_file = Path("aggregated_findings.json")
    if not abort and _should_write(aggregate_file, overwrite_settings):
        _log_start("Aggregating results.")
        _write_json(aggregate_file, aggregate_results)
        _print_next_steps()
    else:
        _log_warn(
            "If you're reading this, something went wrong."
            "Do not push to SysReptor. Please check the output above."
        )
        sys.exit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=
            "convert markdown files to JSON format,"
            "and aggregate them into a single JSON file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "path",
        nargs='+',
        help="markdown file(s) or directory to process (only .md files will be processed)"
    )
    parser.add_argument(
        "--recurse",
        action="store_true",
        help="recursively process markdown files in sub-directories"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="enable strict mode, failing if any expected field fails to be processed"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="automatically overwrite existing JSON files without prompting"
    )
    parser.add_argument(
        "--aggregate-only",
        action="store_true",
        help="skip producing individual JSON files, only produce aggregate JSON file"
    )
    parser.add_argument(
        "--custom-fields",
        action="store_true",
        help="only parse custom fields, marked with '*' in the markdown headings"
    )
    args = parser.parse_args()

    _log_args(args)
    return args

def _find_markdown_files(paths: List[str], recurse: bool = False) -> List[Path]:
    """
    Find markdown files given paths and recursion flag.
    """
    md_files = []
    for path in map(Path, paths):
        if path.is_dir():
            md_files.extend(path.rglob("*.md") if recurse else path.glob("*.md"))
        elif path.is_file() and path.suffix == '.md':
            md_files.append(path)
    return md_files

def _process_markdown_file(md_file: Path, strict: bool, custom_fields: bool = False) -> Dict[str, Any]:
    """
    Process a markdown file and convert it to JSON.
    """
    try:
        content = md_file.read_text(encoding='utf-8')
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as e:
        _log_error(f"Error processing '{md_file}': {str(e)}", True)
        return None

    json_output = {
        "status": "in-progress",
        "data": {
            "cvss": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N",
            "title": "",
            "summary": "",
            "impact": "",
            "recommendation": "",
            "references": [],
            "affected_components": []
        }
    }

    sections = _extract_sections(content, strict)
    if not sections:
        _log_warn(f"No sections found in '{md_file}'", True)
        return None

    if custom_fields:
        process_custom(sections, json_output)
    else:
        process_native(sections, json_output, strict, md_file)

    return json_output

def process_custom(sections: Dict[str, str], json_output: Dict[str, Any]) -> None:
    """
    Process custom fields, marked with '*' in the markdown headings.
    """
    for key, content in sections.items():
        if re.match(r"^\*[^\s\*]+$", key):
            clean_key = key[1:]
            json_output["data"][clean_key] = content

def process_native(sections: Dict[str, str], json_output: Dict[str, Any], strict: bool, md_file: Path) -> None:
    """
    Process native fields, using the _PROCESSORS dictionary to convert markdown sections to JSON.
    """
    for key, processor in _PROCESSORS.items():
        processed = False
        if key in sections:
            json_output["data"][key] = processor(sections[key])
            processed = True
        elif strict:
            _log_error(
                f"Missing required section '{key}' in '{md_file}',"
                "aborting due to strictness level", True
            )
            return None
        else:
            _log_warn(f"Missing section '{key}' in '{md_file}'", True)

        if processed and not json_output["data"][key]:
            if strict:
                _log_error(
                    f"Section '{key}' in '{md_file}' is present but empty,"
                    "aborting due to strictness level", True
                )
                return None
            else:
                _log_warn(f"Section '{key}' in '{md_file}' is present but empty", True)

def _md_list_to_json_array(markdown: str) -> List[str]:
    """
    Turns a markdown list into a JSON array.
    """
    items = []
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            item = line[2:].strip()
            if item:
                items.append(item)
    return items

_PROCESSORS = {
    "title": lambda s: s,
    "summary": lambda s: s,
    "impact": lambda s: s,
    "recommendation": lambda s: s,
    "references": _md_list_to_json_array,
    "affected_components": _md_list_to_json_array,
    "description": lambda s: s
}

def _extract_sections(content: str, strict: bool) -> Dict[str, str]:
    """
    Extract sections from markdown content based on headings.
    Aborts if strict mode is enabled and duplicate headings are found, otherwise merges them.
    Discards any content that is not under a heading.
    """
    sections = {}
    current_heading = None
    current_content = []

    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)')

    for line in content.splitlines():
        line = line.strip()
        match = heading_pattern.match(line)
        if match:
            if current_heading:
                # Save the previous section
                _save_section(sections, current_heading, current_content, strict)

            # Start a new section
            current_heading = match.group(2).strip().lower().replace(" ", "_")
            current_content = []
        else:
            current_content.append(line)

    # Save the last section
    if current_heading:
        _save_section(sections, current_heading, current_content, strict)

    return sections

def _save_section(sections: Dict[str, str], heading: str, content: List[str], strict: bool) -> None:
    if heading in sections:
        if strict:
            _log_error(
                f"Duplicate heading '{heading}' found,"
                "aborting due to strictness level", True
            )
            return None
        else:
            _log_warn(f"Duplicate heading '{heading}' found, merging content", True)
            sections[heading] += "\n" + _trim_and_merge(content)
    else:
        sections[heading] = _trim_and_merge(content)

def _trim_and_merge(current_content) -> None:
    # Remove leading and trailing empty lines
    while current_content and current_content[0] == "":
        current_content.pop(0)
    while current_content and current_content[-1] == "":
        current_content.pop()

    return "\n".join(current_content)

def _should_abort(proceed_settings: Dict[str, bool]) -> bool:
    """
    Handle user confirmation for aborting the process.
    """
    if proceed_settings["always"]:
        _log_warn("Processing failed, but proceeding to next file", True)
        return False

    proceed = _prompt_user("Processing failed, would you like to proceed?", _PROCEED_OPTIONS)
    if proceed == 'n':
        _log_warn("Quitting!")
        return True
    if proceed == 'a':
        proceed_settings["always"] = True

    return False

def _should_write(output_file: Path, overwrite_settings: Dict[str, bool]) -> bool:
    """
    Handle file (over)writing logic based on user input and settings.
    """
    if not output_file.exists():
        return True

    if overwrite_settings["always"]:
        _log_warn(f"Overwriting existing file '{output_file}'", True)
        return True
    if overwrite_settings["never"]:
        _log_warn(f"Not overwriting file '{output_file}'", True)
        return False

    overwrite = _prompt_user(f"Output file '{output_file}' exists, overwrite?", _OVERWRITE_OPTIONS)
    if overwrite == 'n' or overwrite == 'e':
        if overwrite == 'e':
            overwrite_settings["never"] = True
        _log_info(f"Skipping write for '{output_file}'.", True)
        return False

    if overwrite == 'a':
        overwrite_settings["always"] = True
    return True

def _write_json(output_file: Path, data: Dict[str, Any]) -> None:
    """
    Writes JSON data to a file.
    If this fails, something is very wrong, and we should stop the script.
    """
    try:
        output_file.write_text(json.dumps(data, indent=4), encoding='utf-8')
        _log_info(f"Wrote output to {output_file}", True)
    except (PermissionError, UnicodeEncodeError, OSError) as e:
        _log_error(f"Failed to write {output_file}: {str(e)}", True)
        _log_warn("Quitting!")
        sys.exit(1)

def _prompt_user(message: str, options: Dict[str, str]) -> str:
    """
    Prompt the user with a message and return their choice.
    """
    while True:
        choice = input(f" ?  {message} ({', '.join(options.values())}): ").lower()
        if choice in options.keys():
            return choice

def _log_args(args: argparse.Namespace) -> None:
    if args.strict:
        _log_info(
            "Strict mode enabled,"
            "processing will fail if any JSON field fails to be parsed or is missing"
        )
    if args.overwrite:
        _log_warn("Existing files will be overwritten without confirmation")
    if args.aggregate_only:
        _log_info("Skipping output of individual JSON files")
    if args.recurse:
        _log_info("Recursing into sub-directories")
    if args.custom_fields:
        _log_info("Only parsing custom fields, marked with '*' in the markdown headings")

def _print_next_steps():
    _log_info("Processing complete! Next steps:")
    _log_info("- to push a single file to SysReptor, 'cat <your_file.json> | reptor finding'", True)
    _log_info(
        "- to push all processed findings to SysReptor,"
        "'cat aggregated_findings.json | reptor finding'", True
    )

# Eww... but it's not worth more complexity
def _log_start(message: str) -> None:
    print("[+] " + message)

def _log_info(message: str, deep: bool = False) -> None:
    if deep:
        print("    " + message)
    else:
        print("[*] " + message)

def _log_warn(message: str, deep: bool = False) -> None:
    if deep:
        print(" !  " + message)
    else:
        print("[!] " + message)

def _log_error(message: str, deep: bool = False) -> None:
    if deep:
        print(" !  ERROR: " + message)
    else:
        print("[!] ERROR: " + message)


_PROCEED_OPTIONS = {
    'y': "[y]es",
    'a': "[a]lways",
    'n': "[n]o"
}

_OVERWRITE_OPTIONS = {
    'y': "[y]es",
    'a': "[a]lways",
    'n': "[n]o",
    'e': "never [e]ver"
}


if __name__ == "__main__":
    main()
