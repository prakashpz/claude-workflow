#!/usr/bin/env python3
"""
Claude Workflow System - Sync Tool

Synchronizes workflow components between the workflow repository and a target project.
Supports selective sync of components and handles merge strategies.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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


def get_file_hash(path: Path) -> str:
    """Get a simple hash of file contents for comparison."""
    import hashlib
    if not path.exists():
        return ""
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def files_differ(src: Path, dst: Path) -> bool:
    """Check if two files have different contents."""
    return get_file_hash(src) != get_file_hash(dst)


def sync_directory(
    src: Path,
    dst: Path,
    strategy: str = 'overlay',
    dry_run: bool = False
) -> List[Tuple[str, str]]:
    """
    Sync a directory with specified strategy.

    Strategies:
    - overlay: Copy new files, update existing (src wins)
    - replace: Delete dst contents, copy all from src
    - merge: Only copy files that don't exist in dst

    Returns list of (action, path) tuples.
    """
    actions = []

    if not src.exists():
        return [(f"skip (not found)", str(src))]

    if strategy == 'replace':
        if dst.exists() and not dry_run:
            shutil.rmtree(dst)
        actions.append(('replace', str(dst)))

    if not dst.exists() and not dry_run:
        dst.mkdir(parents=True, exist_ok=True)

    for item in src.rglob('*'):
        if item.is_dir():
            continue

        relative_path = item.relative_to(src)
        dst_item = dst / relative_path

        if dst_item.exists():
            if strategy == 'merge':
                actions.append(('skip (exists)', str(relative_path)))
                continue
            elif files_differ(item, dst_item):
                actions.append(('update', str(relative_path)))
                if not dry_run:
                    dst_item.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dst_item)
            else:
                actions.append(('unchanged', str(relative_path)))
        else:
            actions.append(('create', str(relative_path)))
            if not dry_run:
                dst_item.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_item)

    return actions


def detect_project_variant(project_path: Path) -> Optional[str]:
    """Detect the variant used by a project."""
    settings_path = project_path / '.claude' / 'settings.json'
    if settings_path.exists():
        try:
            settings = load_json(settings_path)
            return settings.get('project', {}).get('variant')
        except:
            pass
    return None


def get_base_version() -> str:
    """Get the current base layer version."""
    version_file = REPO_ROOT / 'base' / 'VERSION'
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"


def sync_base_layer(
    project_path: Path,
    components: List[str],
    strategy: str = 'overlay',
    dry_run: bool = False
) -> Dict[str, List[Tuple[str, str]]]:
    """Sync base layer components to project."""
    results = {}
    base_dir = REPO_ROOT / 'base'

    component_mapping = {
        'commands': ('.claude/commands', 'commands'),
        'agents': ('.claude/agents', 'agents'),
        'tasks': ('.claude/tasks', 'tasks'),
        'workflows': ('.github/workflows', 'github-workflows'),
    }

    for component in components:
        if component not in component_mapping:
            results[component] = [('error', f'Unknown component: {component}')]
            continue

        dst_rel, src_rel = component_mapping[component]
        src = base_dir / src_rel
        dst = project_path / dst_rel

        actions = sync_directory(src, dst, strategy, dry_run)
        results[component] = actions

    return results


def sync_variant_layer(
    project_path: Path,
    variant_name: str,
    components: List[str],
    strategy: str = 'overlay',
    dry_run: bool = False
) -> Dict[str, List[Tuple[str, str]]]:
    """Sync variant layer components to project."""
    results = {}
    variant_dir = REPO_ROOT / 'variants' / variant_name

    manifest_path = variant_dir / 'manifest.json'
    if not manifest_path.exists():
        return {'error': [('error', f'Variant manifest not found: {variant_name}')]}

    manifest = load_json(manifest_path)
    manifest_components = manifest.get('components', {})

    for component in components:
        if component not in manifest_components:
            results[component] = [('skip', 'Not in variant')]
            continue

        actions = []
        for item in manifest_components[component]:
            src = variant_dir / item['path']

            # Determine destination based on component type
            if component == 'agents':
                dst = project_path / '.claude' / 'agents' / Path(item['path']).name
            elif component == 'commands':
                dst = project_path / '.claude' / 'commands' / Path(item['path']).name
            elif component == 'tasks':
                dst = project_path / '.claude' / 'tasks' / Path(item['path']).name
            elif component == 'templates':
                dst = project_path / item['destination']
            else:
                dst = project_path / item['path']

            item_strategy = item.get('mergeStrategy', strategy)

            if not src.exists():
                actions.append(('skip (not found)', item['path']))
                continue

            if dst.exists():
                if item_strategy == 'skip_if_exists' or (item_strategy == 'merge'):
                    actions.append(('skip (exists)', item['path']))
                    continue
                elif files_differ(src, dst):
                    actions.append(('update', item['path']))
                    if not dry_run:
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dst)
                else:
                    actions.append(('unchanged', item['path']))
            else:
                actions.append(('create', item['path']))
                if not dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)

        results[component] = actions

    return results


def print_sync_results(results: Dict[str, List[Tuple[str, str]]], dry_run: bool = False) -> None:
    """Print sync results in a readable format."""
    if dry_run:
        print("\n[DRY RUN - No changes made]\n")

    for component, actions in results.items():
        print(f"\n{component}:")
        for action, path in actions:
            icon = {
                'create': '  + ',
                'update': '  ~ ',
                'skip': '  - ',
                'skip (exists)': '  - ',
                'skip (not found)': '  ! ',
                'unchanged': '  = ',
                'replace': '  * ',
                'error': '  ! ',
            }.get(action, '  ? ')
            print(f"{icon}{path} ({action})")


def main():
    parser = argparse.ArgumentParser(
        description='Sync Claude Workflow System components to a project'
    )
    parser.add_argument(
        'project_path',
        type=Path,
        help='Path to the target project'
    )
    parser.add_argument(
        '--components',
        '-c',
        nargs='+',
        default=['commands', 'agents', 'tasks', 'workflows'],
        choices=['commands', 'agents', 'tasks', 'workflows', 'templates'],
        help='Components to sync'
    )
    parser.add_argument(
        '--variant',
        '-v',
        type=str,
        help='Variant to sync (auto-detected if not specified)'
    )
    parser.add_argument(
        '--strategy',
        '-s',
        choices=['overlay', 'replace', 'merge'],
        default='overlay',
        help='Sync strategy: overlay (default), replace, or merge'
    )
    parser.add_argument(
        '--base-only',
        action='store_true',
        help='Only sync base layer, skip variant'
    )
    parser.add_argument(
        '--variant-only',
        action='store_true',
        help='Only sync variant layer, skip base'
    )
    parser.add_argument(
        '--dry-run',
        '-n',
        action='store_true',
        help='Show what would be done without making changes'
    )

    args = parser.parse_args()
    project_path = args.project_path.resolve()

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        return 1

    # Detect variant if not specified
    variant = args.variant or detect_project_variant(project_path)

    print(f"Syncing Claude Workflow System to: {project_path}")
    print(f"Base version: {get_base_version()}")
    if variant:
        print(f"Variant: {variant}")
    print(f"Components: {', '.join(args.components)}")
    print(f"Strategy: {args.strategy}")

    # Sync base layer
    if not args.variant_only:
        print("\n--- Base Layer ---")
        base_results = sync_base_layer(
            project_path,
            args.components,
            args.strategy,
            args.dry_run
        )
        print_sync_results(base_results, args.dry_run)

    # Sync variant layer
    if variant and not args.base_only:
        print(f"\n--- Variant Layer ({variant}) ---")
        variant_results = sync_variant_layer(
            project_path,
            variant,
            args.components,
            args.strategy,
            args.dry_run
        )
        print_sync_results(variant_results, args.dry_run)

    if not args.dry_run:
        print("\n✓ Sync completed!")
    else:
        print("\n[DRY RUN] No changes were made.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
