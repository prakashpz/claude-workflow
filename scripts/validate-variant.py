#!/usr/bin/env python3
"""
Claude Workflow System - Variant Validator

Validates variant manifests and component files against schemas and conventions.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent


def load_json(path: Path) -> Dict:
    """Load and parse a JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def load_schema(schema_name: str) -> Dict:
    """Load a JSON schema from the base/schema directory."""
    schema_path = REPO_ROOT / 'base' / 'schema' / schema_name
    return load_json(schema_path)


def validate_manifest_structure(manifest: Dict) -> List[str]:
    """Validate manifest has required fields."""
    errors = []
    required_fields = ['name', 'version', 'description', 'projectType']

    for field in required_fields:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    # Validate version format
    if 'version' in manifest:
        version = manifest['version']
        parts = version.split('.')
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            errors.append(f"Invalid version format: {version} (expected X.Y.Z)")

    # Validate projectType
    valid_types = ['nextjs', 'react', 'node', 'python', 'crewai', 'generic']
    if 'projectType' in manifest and manifest['projectType'] not in valid_types:
        errors.append(f"Invalid projectType: {manifest['projectType']} (expected one of {valid_types})")

    # Validate name format
    if 'name' in manifest:
        name = manifest['name']
        if not name[0].islower() or not all(c.islower() or c.isdigit() or c == '-' for c in name):
            errors.append(f"Invalid name format: {name} (expected lowercase with hyphens)")

    return errors


def validate_components(manifest: Dict, variant_dir: Path) -> List[str]:
    """Validate that all referenced component files exist."""
    errors = []
    components = manifest.get('components', {})

    for component_type, items in components.items():
        if not isinstance(items, list):
            errors.append(f"Invalid components.{component_type}: expected array")
            continue

        for item in items:
            if not isinstance(item, dict):
                errors.append(f"Invalid item in components.{component_type}: expected object")
                continue

            # Check required fields
            if component_type == 'templates':
                if 'source' not in item:
                    errors.append(f"Missing 'source' in components.{component_type} item")
                elif not (variant_dir / item['source']).exists():
                    errors.append(f"Component file not found: {item['source']}")
                if 'destination' not in item:
                    errors.append(f"Missing 'destination' in components.{component_type} item")
            else:
                if 'name' not in item:
                    errors.append(f"Missing 'name' in components.{component_type} item")
                if 'path' not in item:
                    errors.append(f"Missing 'path' in components.{component_type} item")
                elif not (variant_dir / item['path']).exists():
                    errors.append(f"Component file not found: {item['path']}")

    return errors


def validate_markdown_frontmatter(file_path: Path, expected_fields: List[str]) -> List[str]:
    """Validate markdown file has proper frontmatter."""
    errors = []

    content = file_path.read_text()

    if not content.startswith('---'):
        errors.append(f"{file_path.name}: Missing frontmatter")
        return errors

    # Find frontmatter end
    end_marker = content.find('---', 3)
    if end_marker == -1:
        errors.append(f"{file_path.name}: Incomplete frontmatter")
        return errors

    frontmatter = content[3:end_marker].strip()

    # Simple YAML parsing for validation
    fields = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            fields[key.strip()] = value.strip()

    for field in expected_fields:
        if field not in fields:
            errors.append(f"{file_path.name}: Missing frontmatter field '{field}'")

    return errors


def validate_agent_files(variant_dir: Path, manifest: Dict) -> List[str]:
    """Validate agent definition files."""
    errors = []
    agents = manifest.get('components', {}).get('agents', [])

    for agent in agents:
        if 'path' not in agent:
            continue

        file_path = variant_dir / agent['path']
        if not file_path.exists():
            continue

        errors.extend(validate_markdown_frontmatter(
            file_path,
            ['name', 'description']
        ))

    return errors


def validate_command_files(variant_dir: Path, manifest: Dict) -> List[str]:
    """Validate command definition files."""
    errors = []
    commands = manifest.get('components', {}).get('commands', [])

    for command in commands:
        if 'path' not in command:
            continue

        file_path = variant_dir / command['path']
        if not file_path.exists():
            continue

        errors.extend(validate_markdown_frontmatter(
            file_path,
            ['name', 'description']
        ))

    return errors


def validate_task_files(variant_dir: Path, manifest: Dict) -> List[str]:
    """Validate task definition files."""
    errors = []
    tasks = manifest.get('components', {}).get('tasks', [])

    for task in tasks:
        if 'path' not in task:
            continue

        file_path = variant_dir / task['path']
        if not file_path.exists():
            continue

        errors.extend(validate_markdown_frontmatter(
            file_path,
            ['name', 'description']
        ))

    return errors


def validate_variant(variant_path: Path) -> Tuple[List[str], List[str]]:
    """
    Validate a variant directory.

    Returns tuple of (errors, warnings).
    """
    errors = []
    warnings = []

    # Check manifest exists
    manifest_path = variant_path / 'manifest.json'
    if not manifest_path.exists():
        errors.append(f"Manifest not found: {manifest_path}")
        return errors, warnings

    # Load manifest
    try:
        manifest = load_json(manifest_path)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in manifest: {e}")
        return errors, warnings

    # Validate manifest structure
    errors.extend(validate_manifest_structure(manifest))

    # Validate components exist
    errors.extend(validate_components(manifest, variant_path))

    # Validate component files
    errors.extend(validate_agent_files(variant_path, manifest))
    errors.extend(validate_command_files(variant_path, manifest))
    errors.extend(validate_task_files(variant_path, manifest))

    # Check for recommended files
    if not (variant_path / 'README.md').exists():
        warnings.append("Missing README.md")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description='Validate Claude Workflow System variant'
    )
    parser.add_argument(
        'variant',
        type=str,
        help='Variant name or path to validate'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    # Determine variant path
    if Path(args.variant).is_absolute():
        variant_path = Path(args.variant)
    elif Path(args.variant).exists():
        variant_path = Path(args.variant).resolve()
    else:
        variant_path = REPO_ROOT / 'variants' / args.variant

    if not variant_path.exists():
        print(f"Error: Variant not found: {variant_path}")
        return 1

    print(f"Validating variant: {variant_path.name}")
    print(f"Path: {variant_path}")
    print()

    errors, warnings = validate_variant(variant_path)

    # Print results
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  ✗ {error}")
        print()

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        print()

    # Summary
    if not errors and not warnings:
        print("✓ Variant is valid!")
        return 0
    elif not errors:
        print(f"✓ Variant is valid with {len(warnings)} warning(s)")
        return 1 if args.strict else 0
    else:
        print(f"✗ Validation failed with {len(errors)} error(s) and {len(warnings)} warning(s)")
        return 1


if __name__ == '__main__':
    sys.exit(main())
