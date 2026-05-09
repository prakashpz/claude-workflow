#!/usr/bin/env python3
"""
Claude Workflow System - Layer Merger

Merges base and variant layers into a target directory with configurable strategies.
Used internally by init-project.py and sync-workflow.py.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent


def load_json(path: Path) -> Dict:
    """Load and parse a JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def save_json(path: Path, data: Dict) -> None:
    """Save data to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def deep_merge(base: Dict, overlay: Dict) -> Dict:
    """
    Recursively merge two dictionaries.
    Overlay values take precedence.
    Arrays are replaced, not merged.
    """
    result = base.copy()

    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value

    return result


def merge_markdown_files(base_path: Path, overlay_path: Path, output_path: Path) -> None:
    """
    Merge two markdown files intelligently.

    Preserves frontmatter from overlay if present, otherwise uses base.
    Merges content sections by header.
    """
    base_content = base_path.read_text() if base_path.exists() else ""
    overlay_content = overlay_path.read_text() if overlay_path.exists() else ""

    def parse_markdown(content: str) -> tuple:
        """Parse markdown into frontmatter and sections."""
        frontmatter = ""
        body = content

        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                frontmatter = content[:end + 3]
                body = content[end + 3:].strip()

        # Parse sections by headers
        sections = {}
        current_header = "__intro__"
        current_content = []

        for line in body.split('\n'):
            if line.startswith('#'):
                if current_content:
                    sections[current_header] = '\n'.join(current_content)
                current_header = line
                current_content = []
            else:
                current_content.append(line)

        if current_content:
            sections[current_header] = '\n'.join(current_content)

        return frontmatter, sections

    base_fm, base_sections = parse_markdown(base_content)
    overlay_fm, overlay_sections = parse_markdown(overlay_content)

    # Use overlay frontmatter if present
    final_fm = overlay_fm if overlay_fm else base_fm

    # Merge sections (overlay wins for same headers)
    merged_sections = base_sections.copy()
    merged_sections.update(overlay_sections)

    # Reconstruct document
    result = []
    if final_fm:
        result.append(final_fm)
        result.append("")

    # Preserve order from overlay if available
    ordered_headers = list(overlay_sections.keys()) if overlay_sections else []
    for header in base_sections.keys():
        if header not in ordered_headers:
            ordered_headers.append(header)

    for header in ordered_headers:
        if header in merged_sections:
            if header != "__intro__":
                result.append(header)
            result.append(merged_sections[header])
            result.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text('\n'.join(result).strip() + '\n')


def merge_json_files(base_path: Path, overlay_path: Path, output_path: Path, strategy: str = 'deep_merge') -> None:
    """Merge two JSON files."""
    base_data = load_json(base_path) if base_path.exists() else {}
    overlay_data = load_json(overlay_path) if overlay_path.exists() else {}

    if strategy == 'replace':
        result = overlay_data
    elif strategy == 'deep_merge':
        result = deep_merge(base_data, overlay_data)
    else:  # overlay (shallow merge)
        result = base_data.copy()
        result.update(overlay_data)

    save_json(output_path, result)


def merge_file(
    base_path: Path,
    overlay_path: Path,
    output_path: Path,
    strategy: str = 'overlay'
) -> str:
    """
    Merge a single file with the specified strategy.

    Returns action taken: 'created', 'merged', 'replaced', 'copied', 'skipped'
    """
    base_exists = base_path.exists()
    overlay_exists = overlay_path.exists()

    if not base_exists and not overlay_exists:
        return 'skipped'

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine file type
    suffix = overlay_path.suffix if overlay_exists else base_path.suffix

    if strategy == 'replace':
        if overlay_exists:
            shutil.copy2(overlay_path, output_path)
            return 'replaced'
        elif base_exists:
            shutil.copy2(base_path, output_path)
            return 'copied'

    elif strategy == 'deep_merge' and suffix == '.json':
        merge_json_files(base_path, overlay_path, output_path, 'deep_merge')
        return 'merged'

    elif strategy == 'overlay':
        if suffix == '.json' and base_exists and overlay_exists:
            merge_json_files(base_path, overlay_path, output_path, 'overlay')
            return 'merged'
        elif suffix == '.md' and base_exists and overlay_exists:
            merge_markdown_files(base_path, overlay_path, output_path)
            return 'merged'
        elif overlay_exists:
            shutil.copy2(overlay_path, output_path)
            return 'created' if not base_exists else 'replaced'
        else:
            shutil.copy2(base_path, output_path)
            return 'copied'

    # Default: copy overlay if exists, else base
    if overlay_exists:
        shutil.copy2(overlay_path, output_path)
        return 'created'
    else:
        shutil.copy2(base_path, output_path)
        return 'copied'


def merge_directories(
    base_dir: Path,
    overlay_dir: Path,
    output_dir: Path,
    strategy: str = 'overlay',
    exclude: List[str] = None
) -> Dict[str, str]:
    """
    Merge two directories into output.

    Returns dict mapping relative paths to actions taken.
    """
    exclude = exclude or []
    results = {}

    # Collect all files from both directories
    all_files = set()

    if base_dir.exists():
        for f in base_dir.rglob('*'):
            if f.is_file():
                all_files.add(f.relative_to(base_dir))

    if overlay_dir.exists():
        for f in overlay_dir.rglob('*'):
            if f.is_file():
                all_files.add(f.relative_to(overlay_dir))

    # Merge each file
    for rel_path in sorted(all_files):
        # Check exclusions
        if any(rel_path.match(ex) for ex in exclude):
            results[str(rel_path)] = 'excluded'
            continue

        base_file = base_dir / rel_path
        overlay_file = overlay_dir / rel_path
        output_file = output_dir / rel_path

        action = merge_file(base_file, overlay_file, output_file, strategy)
        results[str(rel_path)] = action

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Merge base and variant layers'
    )
    parser.add_argument(
        '--base',
        type=Path,
        default=REPO_ROOT / 'base',
        help='Base layer directory'
    )
    parser.add_argument(
        '--variant',
        type=Path,
        help='Variant layer directory'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=Path,
        required=True,
        help='Output directory'
    )
    parser.add_argument(
        '--strategy',
        '-s',
        choices=['overlay', 'replace', 'deep_merge'],
        default='overlay',
        help='Merge strategy'
    )
    parser.add_argument(
        '--component',
        '-c',
        choices=['commands', 'agents', 'tasks', 'templates', 'workflows', 'all'],
        default='all',
        help='Component to merge'
    )
    parser.add_argument(
        '--exclude',
        nargs='*',
        default=[],
        help='Patterns to exclude'
    )
    parser.add_argument(
        '--dry-run',
        '-n',
        action='store_true',
        help='Show what would be done'
    )

    args = parser.parse_args()

    component_dirs = {
        'commands': 'commands',
        'agents': 'agents',
        'tasks': 'tasks',
        'templates': 'templates',
        'workflows': 'github-workflows',
    }

    components_to_merge = list(component_dirs.keys()) if args.component == 'all' else [args.component]

    print(f"Merging layers:")
    print(f"  Base: {args.base}")
    if args.variant:
        print(f"  Variant: {args.variant}")
    print(f"  Output: {args.output}")
    print(f"  Strategy: {args.strategy}")
    print(f"  Components: {', '.join(components_to_merge)}")
    print()

    total_results = {}

    for component in components_to_merge:
        comp_dir = component_dirs[component]
        base_comp = args.base / comp_dir
        variant_comp = args.variant / comp_dir if args.variant else Path('/nonexistent')
        output_comp = args.output / ('.claude' if component in ['commands', 'agents', 'tasks'] else '') / comp_dir

        if component == 'workflows':
            output_comp = args.output / '.github' / 'workflows'

        print(f"\n{component}:")

        if args.dry_run:
            # Just show what would be done
            all_files = set()
            if base_comp.exists():
                for f in base_comp.rglob('*'):
                    if f.is_file():
                        all_files.add(f.relative_to(base_comp))
            if variant_comp.exists():
                for f in variant_comp.rglob('*'):
                    if f.is_file():
                        all_files.add(f.relative_to(variant_comp))

            for f in sorted(all_files):
                base_exists = (base_comp / f).exists()
                variant_exists = (variant_comp / f).exists()
                if base_exists and variant_exists:
                    print(f"  ~ {f} (would merge)")
                elif variant_exists:
                    print(f"  + {f} (from variant)")
                else:
                    print(f"  + {f} (from base)")
        else:
            results = merge_directories(
                base_comp,
                variant_comp,
                output_comp,
                args.strategy,
                args.exclude
            )

            for path, action in results.items():
                icon = {
                    'created': '+',
                    'merged': '~',
                    'replaced': '*',
                    'copied': '+',
                    'skipped': '-',
                    'excluded': 'x',
                }.get(action, '?')
                print(f"  {icon} {path} ({action})")

            total_results[component] = results

    if not args.dry_run:
        print("\n✓ Merge completed!")
    else:
        print("\n[DRY RUN] No changes made.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
