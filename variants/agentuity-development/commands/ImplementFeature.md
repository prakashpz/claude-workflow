---
description: Implement a feature end-to-end using Agentuity specialist agents for code generation
---

# ImplementFeature

Full feature implementation workflow for Agentuity projects, routing to specialized agents.

## Purpose

Orchestrates the complete feature implementation process using Agentuity-specific agents: discovers requirements, generates specifications, routes work to the appropriate specialist agent, and updates tracking systems.

## Arguments

- `feature`: Feature name or description (required)
- `linearIssue`: Task management issue ID (optional, for linking)
- `stack`: Technology requirements array (optional)
  - `agent` - Requires new or modified Agentuity agents
  - `api` - Requires API routes
  - `ui` - Requires SPA frontend components
  - `database` - Requires schema changes
  - `storage` - Requires KV, vector, or stream integration
- `skipSpec`: Skip specification generation (default: false)

## Execution

1. Invoke `feature-workflow` task with action: `implement`
   - Discovery: Finds requirements from PRDs, documentation, task management
   - Specification: Generates or loads feature spec
   - Approval: Presents plan for confirmation
   - Implementation: Routes to specialist agents (see Agent Routing below)
   - Update: Syncs task management with progress

2. Display:
   - Requirements summary
   - Implementation plan
   - Generated code locations
   - Next steps

## Prerequisites

- Requirements exist in PRD, documentation, or task management
- Session active (recommended)
- Agentuity project with `@agentuity/runtime`

## Output Files

- `/docs/specs/{feature-name}.md` (if generated)
- Code files as specified

## Example

```
/ImplementFeature feature="Cash flow projection agent" linearIssue="PROJ-42" stack=["agent", "api", "ui"]
```

## Related

- `/FixBug` - For bug fixes
- `/RefactorCode` - For refactoring
- `/ReviewCode` - Review implementation
- `/CreateAgent` - Scaffold individual agents
- `/CreateRoute` - Scaffold individual API routes

## Tasks Invoked

- `feature-workflow.implement`
- `requirement-discovery.discover`
- `context-loader.loadForFeature`
- `mcp-sync.syncLinear`

## Agent Routing

| Requirement Type | Agent | When to Use |
|------------------|-------|-------------|
| Agentuity agents (createAgent, schemas, storage, agent-to-agent) | `agentuity-agent-architect` | New agent creation, agent modification, AI Gateway integration |
| API routes (createRouter, Hono, cron, middleware) | `agentuity-route-designer` | HTTP endpoints, webhooks, cron jobs, agent-route wiring |
| Frontend (React components, pages, routing) | `react-spa-writer` | SPA pages, components, client-side logic |
| Database schema | `schema-designer` | Schema changes (Drizzle, Postgres) |
| Tests | `test-planner` | Test specifications and evaluation design |

**Do NOT route to `code-writer`** -- this variant uses specialized agents for all implementation work.

## Approval Checkpoints

The workflow pauses for approval:
1. After specification generation
2. Before agent creation or modification
3. Before major file creation
