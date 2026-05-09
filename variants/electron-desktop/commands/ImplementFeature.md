---
description: Implement a feature end-to-end using Electron specialist agents for code generation
---

# ImplementFeature

Full feature implementation workflow for Electron desktop applications.

## Purpose

Orchestrates feature implementation using Electron-specific agents for main process, renderer, and IPC communication patterns.

## Arguments

- `feature`: Feature name or description (required)
- `linearIssue`: Task management issue ID (optional, for linking)
- `stack`: Technology requirements array (optional)
  - `database` - Requires schema/storage changes
  - `api` - Requires IPC channels or external API
  - `ui` - Requires renderer UI components
  - `native` - Requires native OS integration
- `skipSpec`: Skip specification generation (default: false)

## Execution

1. Invoke `feature-workflow` task with action: `implement`
   - Discovery: Finds requirements from PRDs, documentation, task management
   - Specification: Generates or loads feature spec
   - Approval: Presents plan for confirmation
   - Implementation: Routes to specialist agents (see Agent Routing)
   - Update: Syncs task management with progress

2. Display:
   - Requirements summary
   - Implementation plan (main process vs renderer)
   - Generated code locations
   - Next steps

## Prerequisites

- Requirements exist in PRD, documentation, or task management
- Session active (recommended)

## Output Files

- `/docs/specs/{feature-name}.md` (if generated)
- Code files as specified

## Example

```
/ImplementFeature feature="File drag-and-drop import" linearIssue="PROJ-301" stack=["native", "ui"]
```

## Related

- `/FixBug` - For bug fixes
- `/RefactorCode` - For refactoring
- `/CreateComponent` - Scaffold renderer components
- `/BuildInstaller` - Build distribution packages

## Tasks Invoked

- `feature-workflow.implement`
- `requirement-discovery.discover`
- `context-loader.loadForFeature`
- `mcp-sync.syncLinear`

## Agent Routing

| Requirement Type | Agent | When to Use |
|------------------|-------|-------------|
| Database/storage | `schema-designer` | Schema or persistent storage changes |
| IPC channels, main/renderer communication | `ipc-architect` | IPC channel design, preload scripts |
| Main process, native OS, window management | `electron-specialist` | Main process logic, native integration |
| Renderer UI components | `electron-specialist` | Renderer React components, state, theming |
| Tests | `test-planner` | Test specifications |

**Do NOT route to `code-writer`** — this variant uses specialized agents for all implementation work.

## Approval Checkpoints

The workflow pauses for approval:
1. After specification generation
2. Before database/storage migrations
3. Before major file creation
