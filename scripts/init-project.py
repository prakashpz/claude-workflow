#!/usr/bin/env python3
"""
Claude Workflow System - Project Initializer

Initializes a new project with the Claude Workflow System by:
1. Copying base layer components
2. Applying variant-specific configurations
3. Creating project structure
4. Setting up GitHub Actions workflows
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add scripts directory to path for imports
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


def copy_directory(src: Path, dst: Path, exclude: List[str] = None) -> None:
    """Copy directory contents, optionally excluding patterns."""
    exclude = exclude or []

    if not src.exists():
        print(f"Warning: Source directory does not exist: {src}")
        return

    for item in src.iterdir():
        if any(item.name.endswith(ex) or item.name == ex for ex in exclude):
            continue

        dst_item = dst / item.name

        if item.is_dir():
            dst_item.mkdir(parents=True, exist_ok=True)
            copy_directory(item, dst_item, exclude)
        else:
            dst_item.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dst_item)


def process_template(template_path: Path, output_path: Path, variables: Dict[str, str]) -> None:
    """Process a template file, replacing variables."""
    with open(template_path, 'r') as f:
        content = f.read()

    for key, value in variables.items():
        content = content.replace(f'{{{{{key}}}}}', value)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove .template extension if present
    if output_path.suffix == '.template':
        output_path = output_path.with_suffix('')

    with open(output_path, 'w') as f:
        f.write(content)


def get_available_variants() -> List[str]:
    """Get list of available variants."""
    variants_dir = REPO_ROOT / 'variants'
    if not variants_dir.exists():
        return []

    variants = []
    for item in variants_dir.iterdir():
        if item.is_dir() and (item / 'manifest.json').exists():
            variants.append(item.name)

    return variants


def load_variant_manifest(variant_name: str) -> Optional[Dict]:
    """Load a variant's manifest file."""
    manifest_path = REPO_ROOT / 'variants' / variant_name / 'manifest.json'
    if not manifest_path.exists():
        return None
    return load_json(manifest_path)


def init_base_layer(project_path: Path) -> None:
    """Initialize the base layer in the project."""
    print("Initializing base layer...")

    base_dir = REPO_ROOT / 'base'

    # Copy commands
    commands_src = base_dir / 'commands'
    commands_dst = project_path / '.claude' / 'commands'
    if commands_src.exists():
        copy_directory(commands_src, commands_dst)
        print(f"  Copied commands to {commands_dst}")

    # Copy agents
    agents_src = base_dir / 'agents'
    agents_dst = project_path / '.claude' / 'agents'
    if agents_src.exists():
        copy_directory(agents_src, agents_dst)
        print(f"  Copied agents to {agents_dst}")

    # Copy tasks
    tasks_src = base_dir / 'tasks'
    tasks_dst = project_path / '.claude' / 'tasks'
    if tasks_src.exists():
        copy_directory(tasks_src, tasks_dst)
        print(f"  Copied tasks to {tasks_dst}")

    # Copy GitHub workflows
    workflows_src = base_dir / 'github-workflows'
    workflows_dst = project_path / '.github' / 'workflows'
    if workflows_src.exists():
        copy_directory(workflows_src, workflows_dst)
        print(f"  Copied GitHub workflows to {workflows_dst}")


def init_templates(project_path: Path, variables: Dict[str, str]) -> None:
    """Initialize template files in the project."""
    print("Initializing templates...")

    templates_dir = REPO_ROOT / 'base' / 'templates'

    for template_file in templates_dir.rglob('*.template'):
        relative_path = template_file.relative_to(templates_dir)
        output_path = project_path / relative_path

        # Remove .template extension
        output_path = output_path.with_suffix('')

        process_template(template_file, output_path, variables)
        print(f"  Created {output_path}")

    # Copy non-template files (like .gitkeep)
    for other_file in templates_dir.rglob('*'):
        if other_file.is_file() and not other_file.suffix == '.template':
            relative_path = other_file.relative_to(templates_dir)
            output_path = project_path / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(other_file, output_path)


def init_variant(project_path: Path, variant_name: str, variables: Dict[str, str]) -> None:
    """Initialize variant-specific components."""
    print(f"Initializing variant: {variant_name}")

    manifest = load_variant_manifest(variant_name)
    if not manifest:
        print(f"  Warning: Could not load manifest for variant {variant_name}")
        return

    variant_dir = REPO_ROOT / 'variants' / variant_name

    # Process variant components based on manifest
    components = manifest.get('components', {})

    # Copy variant agents (overlay with base)
    for agent in components.get('agents', []):
        src = variant_dir / agent['path']
        dst = project_path / '.claude' / 'agents' / Path(agent['path']).name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Added variant agent: {agent['name']}")

    # Copy variant commands
    for command in components.get('commands', []):
        src = variant_dir / command['path']
        dst = project_path / '.claude' / 'commands' / Path(command['path']).name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Added variant command: {command['name']}")

    # Copy variant tasks
    for task in components.get('tasks', []):
        src = variant_dir / task['path']
        dst = project_path / '.claude' / 'tasks' / Path(task['path']).name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Added variant task: {task['name']}")

    # Copy variant templates
    for template in components.get('templates', []):
        src = variant_dir / template['source']
        dst = project_path / template['destination']

        strategy = template.get('mergeStrategy', 'skip_if_exists')

        if dst.exists() and strategy == 'skip_if_exists':
            print(f"  Skipped (exists): {dst}")
            continue

        if src.exists():
            if src.is_dir():
                copy_directory(src, dst)
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.suffix == '.template':
                    process_template(src, dst, variables)
                else:
                    shutil.copy2(src, dst)
            print(f"  Created: {dst}")


def create_directory_structure(project_path: Path) -> None:
    """Create the basic directory structure."""
    directories = [
        '.claude/commands',
        '.claude/agents',
        '.claude/tasks',
        '.github/workflows',
        'docs/planning',
        'docs/specs',
        'docs/reports',
        'knowledge/prd',
        'knowledge/architecture',
    ]

    for dir_path in directories:
        (project_path / dir_path).mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a project with Claude Workflow System'
    )
    parser.add_argument(
        'project_path',
        type=Path,
        help='Path to the project to initialize'
    )
    parser.add_argument(
        '--variant',
        '-v',
        type=str,
        help='Variant to use (e.g., nextjs-development)'
    )
    parser.add_argument(
        '--name',
        '-n',
        type=str,
        help='Project name (defaults to directory name)'
    )
    parser.add_argument(
        '--description',
        '-d',
        type=str,
        default='A project using Claude Workflow System',
        help='Project description'
    )
    parser.add_argument(
        '--force',
        '-f',
        action='store_true',
        help='Overwrite existing files'
    )
    parser.add_argument(
        '--list-variants',
        action='store_true',
        help='List available variants and exit'
    )

    args = parser.parse_args()

    # List variants if requested
    if args.list_variants:
        variants = get_available_variants()
        if variants:
            print("Available variants:")
            for v in variants:
                manifest = load_variant_manifest(v)
                desc = manifest.get('description', 'No description') if manifest else 'No description'
                print(f"  {v}: {desc}")
        else:
            print("No variants available")
        return 0

    project_path = args.project_path.resolve()

    # Check if project already has workflow system
    if (project_path / '.claude').exists() and not args.force:
        print(f"Error: Project already has .claude directory. Use --force to overwrite.")
        return 1

    # Prepare template variables
    project_name = args.name or project_path.name
    variables = {
        'PROJECT_NAME': project_name,
        'PROJECT_DESCRIPTION': args.description,
        'PROJECT_TYPE': args.variant or 'generic',
        'VARIANT_NAME': args.variant or 'base',
        'TIMESTAMP': '',  # Will be filled dynamically
        'SESSION_ID': '',
        'PROJECT_STRUCTURE': '# See project documentation',
        'PREREQUISITES': '# See project documentation',
        'INSTALLATION_COMMANDS': '# See project documentation',
        'DEV_SERVER_COMMAND': '# See project documentation',
        'TEST_COMMAND': '# See project documentation',
        'BUILD_COMMAND': '# See project documentation',
        'TASK_MANAGEMENT_TOOL': 'Linear',
        'ADDITIONAL_CONTEXT': '',
    }

    print(f"\nInitializing Claude Workflow System for: {project_name}")
    print(f"Project path: {project_path}")
    if args.variant:
        print(f"Variant: {args.variant}")
    print()

    # Create directory structure
    create_directory_structure(project_path)

    # Initialize base layer
    init_base_layer(project_path)

    # Initialize templates
    init_templates(project_path, variables)

    # Initialize variant if specified
    if args.variant:
        if args.variant not in get_available_variants():
            print(f"Warning: Variant '{args.variant}' not found. Skipping variant initialization.")
        else:
            init_variant(project_path, args.variant, variables)

    print("\n✓ Claude Workflow System initialized successfully!")
    print("\nNext steps:")
    print("  1. Review and customize CLAUDE.md")
    print("  2. Configure .claude/settings.json for your project")
    print("  3. Add ANTHROPIC_API_KEY to GitHub secrets for CI workflows")
    print("  4. Run /StartSession to begin your first development session")

    return 0


if __name__ == '__main__':
    sys.exit(main())
