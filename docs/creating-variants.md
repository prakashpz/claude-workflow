# Creating Variants

This guide explains how to create custom variants for the Claude Workflow System.

## Quick Start: Interactive Creation

The easiest way to create a variant is using the `/CreateVariant` command:

```bash
# Create a new variant interactively
/CreateVariant swift-ios

# Or during /SetupWorkflow, select "Create New Variant"
```

This guides you through creating all necessary files and generates a valid variant structure.

## What is a Variant?

A variant extends the base workflow system with project-type-specific components. Variants can:

- Add specialized agents for specific technologies
- Include custom commands for common operations
- Provide project structure templates
- Define technology-specific tasks
- Configure default settings

## Variant Structure

```
variants/
└── your-variant-name/
    ├── manifest.json       # Required: Variant configuration
    ├── README.md           # Recommended: Documentation
    ├── agents/             # Specialized agents
    │   └── your-agent.md
    ├── commands/           # Custom commands
    │   └── YourCommand.md
    ├── tasks/              # Technology-specific tasks
    │   └── your-task.md
    └── templates/          # Project templates
        └── CLAUDE.md.variant
```

## Creating the Manifest

The manifest (`manifest.json`) defines your variant:

```json
{
  "$schema": "../../base/schema/manifest.schema.json",
  "name": "your-variant-name",
  "version": "1.0.0",
  "description": "Description of what this variant provides",
  "projectType": "nextjs",
  "baseVersion": "2.0.0",
  "components": {
    "agents": [...],
    "commands": [...],
    "tasks": [...],
    "templates": [...]
  },
  "configuration": {...},
  "initialization": {...}
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier (lowercase, hyphens) |
| `version` | Semantic version (X.Y.Z) |
| `description` | Human-readable description |
| `projectType` | One of: `nextjs`, `react`, `node`, `python`, `crewai`, `generic` |

### Components Section

Define which components your variant adds:

```json
{
  "components": {
    "agents": [
      {
        "name": "react-specialist",
        "path": "agents/react-specialist.md",
        "mergeStrategy": "overlay"
      }
    ],
    "commands": [
      {
        "name": "CreateComponent",
        "path": "commands/CreateComponent.md",
        "mergeStrategy": "overlay"
      }
    ],
    "tasks": [
      {
        "name": "react-build",
        "path": "tasks/react-build.md",
        "mergeStrategy": "overlay"
      }
    ],
    "templates": [
      {
        "source": "templates/CLAUDE.md.variant",
        "destination": "CLAUDE.md",
        "mergeStrategy": "skip_if_exists"
      }
    ]
  }
}
```

### Merge Strategies

| Strategy | Behavior |
|----------|----------|
| `overlay` | Combine with base, variant wins on conflict |
| `replace` | Completely replace base component |
| `skip_if_exists` | Only copy if target doesn't exist |

### Configuration Section

Define project structure and requirements:

```json
{
  "configuration": {
    "projectStructure": {
      "components": "src/components",
      "pages": "src/pages",
      "lib": "src/lib"
    },
    "requiredDependencies": [
      "react",
      "typescript"
    ],
    "environmentVariables": [
      {
        "name": "API_URL",
        "description": "Backend API URL",
        "required": false
      }
    ]
  }
}
```

### Initialization Section

Define setup steps and prompts:

```json
{
  "initialization": {
    "preInit": [
      "npm init -y"
    ],
    "postInit": [
      "npm install",
      "npm run dev"
    ],
    "prompts": [
      {
        "key": "useTypeScript",
        "message": "Use TypeScript?",
        "type": "confirm",
        "default": "true"
      }
    ]
  }
}
```

## Creating Agents

Agents follow the standard format:

```markdown
---
name: agent-name
description: What this agent specializes in
model: sonnet
---

# Agent Name

Brief description of the agent's expertise.

## Expertise Areas

- Area 1
- Area 2

## Input Contract

- `input1`: Description
- `input2`: Description

## Output Contract

- `output1`: Description
- `output2`: Description

## Behavioral Guidelines

### Pattern Name

```code
Example code or pattern
```

## Integration Points

- Works with `other-agent` for X
- Collaborates with `another-agent` for Y
```

## Creating Commands

Commands follow the standard format:

```markdown
---
name: CommandName
description: What this command does
---

# /CommandName

Brief description of the command.

## Usage

```
/CommandName <arg> [options]
```

## Arguments

- `arg`: Required argument description

## Options

- `--option`: Option description

## Examples

```bash
# Example 1
/CommandName value --option

# Example 2
/CommandName other-value
```

## Workflow

1. Step 1
2. Step 2
3. Step 3

## Related Commands

- `/OtherCommand` - Related functionality
```

## Creating Tasks

Tasks define orchestration operations:

```markdown
---
name: task-name
description: What this task orchestrates
---

# Task Name

Description of the task's purpose.

## Operations

### `operationName`

Operation description.

**Inputs:**
- `input`: Description

**Steps:**
1. Step 1
2. Step 2

**Outputs:**
```json
{
  "result": "value"
}
```

## Dependencies

- **other-task**: For X functionality
- **agent-name**: For Y operations

## Error Handling

| Error | Action |
|-------|--------|
| Error type | How to handle |
```

## Testing Your Variant

Use the validation script:

```bash
python scripts/validate-variant.py variants/your-variant-name
```

This checks:
- Manifest structure and required fields
- Referenced files exist
- Markdown frontmatter is valid
- Version format is correct

## Example: Creating a Python Variant

1. Create the directory structure:

```bash
mkdir -p variants/python-development/{agents,commands,tasks,templates}
```

2. Create the manifest:

```json
{
  "name": "python-development",
  "version": "1.0.0",
  "description": "Python development with pytest, mypy, and modern tooling",
  "projectType": "python",
  "baseVersion": "2.0.0",
  "components": {
    "agents": [
      {
        "name": "python-specialist",
        "path": "agents/python-specialist.md"
      }
    ],
    "commands": [
      {
        "name": "CreateModule",
        "path": "commands/CreateModule.md"
      }
    ]
  },
  "configuration": {
    "projectStructure": {
      "source": "src",
      "tests": "tests"
    },
    "requiredDependencies": [
      "pytest",
      "mypy"
    ]
  }
}
```

3. Create the python-specialist agent:

```markdown
---
name: python-specialist
description: Expert in Python development with modern practices
model: sonnet
---

# Python Specialist Agent

...
```

4. Validate:

```bash
python scripts/validate-variant.py variants/python-development
```

5. Test by initializing a project:

```bash
python scripts/init-project.py /tmp/test-project --variant python-development
```

## Publishing Your Variant

### Using /SubmitVariant (Recommended)

The easiest way to contribute your variant:

```bash
# Validate and submit via PR
/SubmitVariant swift-ios
```

This command:
1. Validates your variant passes all checks
2. Creates a branch (never pushes to main)
3. Commits your variant files
4. Creates a pull request for review

### Manual Submission

If you prefer manual control:

1. Ensure validation passes:
   ```bash
   python scripts/validate-variant.py variants/your-variant-name
   ```

2. Create a feature branch:
   ```bash
   git checkout -b variant/your-variant-name
   ```

3. Add and commit your variant:
   ```bash
   git add variants/your-variant-name/
   git commit -m "feat(variant): Add your-variant-name variant"
   ```

4. Push and create PR:
   ```bash
   git push origin variant/your-variant-name
   gh pr create --title "Add your-variant-name variant" --body "..."
   ```

### Contribution Guidelines

- **Never push directly to main** - All changes must go through pull requests
- **Validation required** - Your variant must pass `validate-variant.py`
- **Documentation required** - Include a comprehensive README.md
- **Review process** - Maintainers will review before merging

### Maintaining a Private Variant

If you don't want to publish, you can:
- Keep your variant in a local/private directory
- Maintain it in a separate repository
- Use it with your projects without submitting
