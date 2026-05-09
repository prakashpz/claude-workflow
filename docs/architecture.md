# Architecture

This document describes the architecture of the Claude Workflow System.

## Design Principles

1. **Modularity**: Components are self-contained and independently versioned
2. **Extensibility**: Easy to add new commands, agents, and variants
3. **Consistency**: Standardized interfaces across all components
4. **Transparency**: Clear documentation and predictable behavior

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Instance Layer                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Your Project                                          │ │
│  │  - Project-specific CLAUDE.md                          │ │
│  │  - Local customizations                                │ │
│  │  - Instance settings                                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ (overlays/extends)
┌─────────────────────────────────────────────────────────────┐
│                     Variant Layer                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  nextjs-development, crewai-python, etc.               │ │
│  │  - Technology-specific agents                          │ │
│  │  - Specialized commands                                │ │
│  │  - Project structure templates                         │ │
│  │  - Framework-specific tasks                            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ (overlays/extends)
┌─────────────────────────────────────────────────────────────┐
│                      Base Layer                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Core Components                                        │ │
│  │  - 29 Commands (StartSession, PRDIntake, CyclePlan...)   │ │
│  │  - 10 Agents (code-writer, prd-validator, cycle-planner) │ │
│  │  - 20 Tasks (session-management, prd-validation, etc.)   │ │
│  │  - GitHub workflow templates                            │ │
│  │  - JSON schemas                                         │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Types

### Commands

User-invocable operations that orchestrate workflows.

```markdown
---
name: CommandName
description: What this command does
---

# /CommandName

User-facing documentation and usage instructions.

## Usage
## Arguments
## Examples
## Workflow
## Related Commands
```

Commands are invoked with `/CommandName` and typically delegate to tasks.

### Agents

AI specialists with defined input/output contracts.

```markdown
---
name: agent-name
description: Agent's expertise
model: sonnet
---

# Agent Name

## Expertise Areas
## Input Contract
## Output Contract
## Behavioral Guidelines
```

Agents are invoked by tasks or other agents via the Task tool.

### Tasks

Orchestration units that coordinate agents and external systems.

```markdown
---
name: task-name
description: Task's purpose
---

# Task Name

## Operations
### `operationName`
**Inputs:**
**Steps:**
**Outputs:**

## Dependencies
## Error Handling
```

Tasks define operations that can be composed into workflows.

## Data Flow

```
User Input
    │
    ▼
┌─────────┐
│ Command │ ──────► User-facing entry point
└─────────┘
    │
    ▼
┌─────────┐
│  Task   │ ──────► Orchestration logic
└─────────┘
    │
    ├──────────────┬──────────────┐
    ▼              ▼              ▼
┌─────────┐  ┌─────────┐   ┌──────────┐
│  Agent  │  │  Agent  │   │ External │
│(Claude) │  │(Claude) │   │  System  │
└─────────┘  └─────────┘   └──────────┘
    │              │              │
    └──────────────┴──────────────┘
                   │
                   ▼
              Result/Output
```

## Planning Workflow

Version 2.0 introduces a structured PRD-to-Cycle planning pipeline:

```
PRD Intake → Validate → Enrich → Feasibility → Sequence → Breakdown
                                                              │
                                                              ▼
                                          Cycle Plan → Commit → Status → Summary → Retro
```

### PRD Pipeline States

```
draft → validating → validated → enriching → enriched → feasibility → ready → breakdown → in-cycle → completed
```

### Cycle States

```
draft → committed → active → completed
                          → cancelled
```

### Planning Components

| Type | Components |
|------|-----------|
| Commands | PRDIntake, PRDValidate, PRDEnrich, PRDFeasibility, PRDSequence, Breakdown, CyclePlan, CycleCommit, CycleStatus, CycleSummary, CycleRetro |
| Agents | prd-validator, technical-analyst, cycle-planner, status-aggregator |
| Tasks | prd-validation, prd-enrichment, technical-feasibility, work-breakdown, cycle-planning, cycle-monitoring, async-checkin |
| Schemas | prd-state.schema.json, cycle-state.schema.json |

## Project Metadata

Every project using the workflow system needs to be connected to external services. The `project-metadata` task manages these connections:

```json
{
  "projectMetadata": {
    "linear": {
      "teamId": "team-uuid",
      "teamName": "Engineering",
      "projectId": "project-uuid",
      "projectName": "My Project"
    },
    "coda": {
      "docId": "document-id",
      "docName": "Project Documentation",
      "pageId": "page-id",
      "pageName": "Requirements"
    },
    "github": {
      "repo": "org/repo-name",
      "owner": "org",
      "name": "repo-name"
    }
  }
}
```

This metadata is:
- Configured via `/SetupProjectMeta` command
- Verified on every `/StartSession`
- Used by `mcp-sync` to target the correct project/document
- Stored in `.claude/settings.json`

## Session Management

Sessions track development context across interactions.

```json
{
  "session": {
    "id": "session-2026-01-16-1000",
    "status": "active",
    "startedAt": "2026-01-16T10:00:00Z"
  },
  "work": {
    "currentTask": { "id": "PROJ-211", "title": "..." },
    "inProgress": [],
    "completed": [],
    "blocked": []
  },
  "git": {
    "branch": "feature/implementation",
    "commitsThisSession": 3
  }
}
```

Session state is stored in:
- `/docs/planning/session-state.json` (machine-readable)
- `/docs/planning/CURRENT-STATE.md` (human-readable)

## Merge Strategies

When combining layers, different strategies apply:

| Strategy | Behavior |
|----------|----------|
| `overlay` | Combine files, variant wins on conflict |
| `replace` | Variant completely replaces base |
| `deep_merge` | Recursively merge JSON/YAML |
| `skip_if_exists` | Only copy if target doesn't exist |

## MCP Integration

The system integrates with external tools via MCP (Model Context Protocol):

```
┌─────────────────────────────────────────────────┐
│              Claude Workflow System             │
│                                                 │
│  ┌─────────────┐     ┌─────────────────────┐    │
│  │  mcp-sync   │────►│  Task Management    │    │
│  │   Task      │     │  (Linear, Jira)     │    │
│  └─────────────┘     └─────────────────────┘    │
│         │                                       │
│         │            ┌─────────────────────┐    │
│         └───────────►│  Documentation      │    │
│                      │  (Coda, Notion)     │    │
│                      └─────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## File Organization

```
claude-workflows/
├── base/
│   ├── VERSION
│   ├── commands/
│   │   ├── StartSession.md
│   │   ├── EndSession.md
│   │   └── ...
│   ├── agents/
│   │   ├── code-writer.md
│   │   ├── reviewer.md
│   │   └── ...
│   ├── tasks/
│   │   ├── session-management.md
│   │   ├── ci-integration.md
│   │   └── ...
│   ├── github-workflows/
│   │   ├── code-review.yml
│   │   └── security-review.yml
│   ├── templates/
│   │   ├── CLAUDE.md.template
│   │   └── ...
│   └── schema/
│       ├── manifest.schema.json
│       ├── session-state.schema.json
│       ├── prd-state.schema.json
│       └── cycle-state.schema.json
├── variants/
│   └── nextjs-development/
│       ├── manifest.json
│       ├── agents/
│       ├── commands/
│       ├── tasks/
│       ├── templates/
│       └── README.md
├── scripts/
│   ├── init-project.py
│   ├── sync-workflow.py
│   ├── validate-variant.py
│   └── merge-layers.py
├── docs/
│   ├── getting-started.md
│   ├── architecture.md
│   └── ...
└── README.md
```

## Versioning

- Base layer version: `/base/VERSION`
- Variant versions: In `manifest.json`
- Compatibility: `baseVersion` in manifest specifies minimum base version

Current base version: **2.1.1** (Folder convention rules)

## Error Handling

Each component defines error handling:

| Component | Error Strategy |
|-----------|----------------|
| Commands | User-friendly messages, suggest fixes |
| Tasks | Structured error output, recovery options |
| Agents | Graceful degradation, request clarification |
| CI | Fail fast, detailed logs |

## Security Considerations

- No secrets in committed files
- API keys via environment variables or GitHub secrets
- Security review workflow for sensitive changes
- OWASP-aware code review
