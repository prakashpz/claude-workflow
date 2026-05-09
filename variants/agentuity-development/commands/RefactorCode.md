---
description: Plan and execute code refactoring in Agentuity projects using specialist agents
---

# RefactorCode

Structured code refactoring with Agentuity-aware planning, safety checks, and verification.

## Purpose

Guides refactoring efforts using Agentuity specialist agents, ensuring platform best practices and no regressions.

## Arguments

- `target`: File, module, or pattern to refactor (required)
- `goal`: Refactoring goal (optional)
  - `simplify` - Reduce complexity
  - `extract` - Extract reusable agents or components
  - `consolidate` - Merge duplicate code
  - `modernize` - Update to current Agentuity SDK patterns
  - `separate` - Separate concerns (agent vs route vs frontend)
- `linearIssue`: Task management issue ID (optional)

## Execution

1. Invoke `feature-workflow` task with action: `plan` (refactor mode)
   - Analysis: Assess current code structure with Agentuity awareness
   - Plan: Generate refactoring plan
   - Approval: Present plan for confirmation
   - Implementation: Execute refactoring via specialist agents
   - Verification: Ensure no regressions

2. Display:
   - Current code analysis
   - Refactoring plan
   - Risk assessment
   - Implementation steps

## Prerequisites

- Target code exists
- Understanding of current functionality

## Example

```
/RefactorCode target="src/agent/" goal="modernize" linearIssue="PROJ-60"
```

## Refactoring Types

| Goal | Description | Risk Level |
|------|-------------|------------|
| `simplify` | Reduce complexity, improve readability | Low |
| `extract` | Extract shared logic into agents, routes, or components | Medium |
| `consolidate` | Merge duplicate implementations | Medium |
| `modernize` | Update to current Agentuity SDK patterns (schemas, storage, hooks) | High |
| `separate` | Separate agent logic from route/frontend concerns | Medium |

## Safety Checks

Before refactoring:
- Identify all usages of target code
- Check agent-to-agent dependencies
- Check route-to-agent wiring
- Check frontend API client contracts
- Note storage dependencies (KV namespaces, vector indexes)

After refactoring:
- Verify all agent handlers still match schemas
- Run `bun run build` to check compilation
- Verify API routes return expected shapes
- Manual verification of critical paths

## Related

- `/ImplementFeature` - For new features
- `/ReviewCode` - Review the refactoring
- `/GenerateTests` - Add test coverage first

## Tasks Invoked

- `feature-workflow.plan` (refactor mode)
- `context-loader.loadFull`
- `quality-gates.review`

## Agent Routing

| Target Type | Agent | Purpose |
|-------------|-------|---------|
| Agent handlers, schemas, storage APIs | `agentuity-agent-architect` | Agent refactoring |
| API routes, middleware, shared loaders | `agentuity-route-designer` | Route refactoring |
| React components, pages, SPA routing | `react-spa-writer` | Frontend refactoring |
| Database schema | `schema-designer` | Schema refactoring |

**Do NOT route to `code-writer`** -- this variant uses specialized agents for all refactoring work.

## Approval Checkpoint

The workflow pauses for approval after the refactoring plan is generated, before any code changes.
