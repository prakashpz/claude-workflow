---
description: Diagnose and fix bugs in Agentuity applications using specialist agents
---

# FixBug

Structured bug investigation and resolution workflow for Agentuity projects.

## Purpose

Guides the bug fixing process from triage through fix delivery using Agentuity specialist agents for diagnosis and fix generation.

## Arguments

- `description`: Bug description (required)
- `linearIssue`: Task management issue ID (optional)
- `affectedFiles`: Known affected files (optional)
- `severity`: Initial severity assessment (optional: `critical` | `high` | `medium` | `low`)

## Execution

1. Invoke `bug-workflow` task with action: `investigate`
   - Triage: Categorize severity and impact
   - Investigation: Analyze code paths, recent changes
   - Root Cause: Identify source of issue
   - Approval: Present findings before fix
   - Fix: Generate fix via specialist agents (see Agent Routing)
   - Verification: Outline test cases

2. Display:
   - Severity and impact assessment
   - Root cause analysis
   - Fix approach
   - Test verification plan

## Prerequisites

- Bug description or task management issue

## Example

```
/FixBug description="Agent handler returns undefined instead of schema output" linearIssue="PROJ-55" affectedFiles=["src/agent/Financial-Analyst/index.ts"]
```

## Workflow Phases

### 1. Triage
- Categorize: Critical / High / Medium / Low
- Assess impact: Users affected, systems impacted
- Identify layer: Agent logic, API route, SPA frontend, storage, or platform

### 2. Investigation
- Reproduce the issue
- Check for common Agentuity pitfalls:
  - Schema validation failures (input/output mismatch)
  - Thread state TTL expiration (~1 hour)
  - KV key collisions or missing namespaces
  - Agent-to-agent call failures
  - AI Gateway rate limits or model errors
  - Hono route handler errors
  - SPA hydration or routing issues
- Analyze suspected code paths
- Review recent changes (git blame)

### 3. Root Cause Analysis
- Trace issue to source
- Classify: agent logic, schema error, state management, storage, route handler, frontend, integration
- Assess architectural implications

### 4. Approval Checkpoint
**STOP** - Present findings for review before proceeding

### 5. Fix Implementation
- Route to appropriate specialist agent based on root cause
- Include defensive improvements

### 6. Verification
- Define regression tests or agent evaluations
- Outline manual verification steps

## Related

- `/ImplementFeature` - For new features
- `/ReviewCode` - Review the fix
- `/GenerateTests` - Generate test plan

## Tasks Invoked

- `bug-workflow.investigate`
- `context-loader.loadForBug`
- `mcp-sync.syncLinear`

## Agent Routing

| Root Cause Area | Agent | Purpose |
|----------------|-------|---------|
| Agent logic, schemas, storage APIs, AI Gateway | `agentuity-agent-architect` | Agent handler fixes, schema corrections, state management |
| API routes, middleware, cron, validation | `agentuity-route-designer` | Route handler fixes, request/response issues |
| React components, SPA routing, UI rendering | `react-spa-writer` | Frontend fixes, client-side bugs |
| Database/schema | `schema-designer` | Schema fixes |
| Test cases / agent evaluations | `test-planner` | Test and eval generation |

**Do NOT route to `code-writer`** -- this variant uses specialized agents for all fix work.
