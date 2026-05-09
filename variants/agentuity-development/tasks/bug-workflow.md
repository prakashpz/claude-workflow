---
name: bug-workflow
description: Orchestrate bug investigation and fix delivery for Agentuity projects
---

# Bug Workflow Task (Agentuity Variant)

Structured workflow for bug investigation and resolution in Agentuity projects, routing fix generation to specialized agents based on which layer (agent, route, frontend) is affected.

## Operations

### `investigate`

Full bug investigation workflow.

**Inputs:**
- `description`: Bug description
- `linearIssue`: Task management issue ID (optional)
- `affectedFiles`: Known affected files (optional)
- `reproSteps`: Reproduction steps (optional)

**Steps:**
1. **Triage Phase:**
   - Categorize severity: Critical / High / Medium / Low
   - Assess impact: Users affected, systems impacted
   - Identify affected layer: agent, route, frontend, storage, platform
   - Check for workarounds
   - If issue provided, fetch full details via `mcp-sync`

2. **Investigation Phase:**
   - Invoke `context-loader.loadForBug` to gather context
   - Analyze suspected code paths
   - Check for common Agentuity issues:
     - Schema validation failures (input doesn't match, output doesn't match)
     - Thread state TTL expiration (~1 hour lifetime)
     - KV namespace mismatches or missing data
     - Vector search returning unexpected results (similarity threshold)
     - Agent-to-agent `.run()` call failures or timeouts
     - AI Gateway model errors or rate limits
     - Hono route handler exceptions
     - `c.var.*` vs `ctx.*` confusion (routes vs agents)
     - Missing `await` on async storage operations
     - `ctx.waitUntil()` swallowing errors silently
     - SPA relative import path errors (no `@/*` alias)
     - React Router path mismatches
   - Review recent changes to affected files (git blame/log)
   - Search for similar patterns in codebase
   - Document minimal reproduction steps

3. **Root Cause Analysis:**
   - Trace issue to source
   - Classify issue type:
     - `schema_validation` - Input/output schema mismatch
     - `state_management` - Thread state, KV, or vector storage issue
     - `agent_communication` - Agent-to-agent call failure
     - `ai_gateway` - Model error, rate limit, or unexpected response
     - `route_handler` - Hono route exception or incorrect response
     - `storage_error` - KV, vector, or stream API failure
     - `frontend_render` - React component or routing error
     - `frontend_api` - Client-side fetch or data handling error
     - `build_error` - TypeScript compilation or Vite build issue
     - `logic_error` - Incorrect business logic
     - `race_condition` - Timing/concurrency issue
   - Assess if architectural problem
   - Document unhandled edge cases

4. **Approval Checkpoint:**
   - Present findings summary
   - Proposed fix approach
   - Risk assessment
   - Wait for user confirmation

5. **Fix Phase (after approval):**
   - Route to appropriate specialist agent based on root cause:
     - Agent logic bugs -> `agentuity-agent-architect`
     - Route handler bugs -> `agentuity-route-designer`
     - Frontend bugs -> `react-spa-writer`
   - Generate fix code
   - Include defensive improvements

6. **Verification Phase:**
   - Outline test cases or agent evaluations for the fix
   - Check for regression risks
   - Verify edge cases covered

7. **Delivery Phase:**
   - Update task management issue via `mcp-sync`
   - Update session state
   - Generate fix summary

**Outputs:**
```json
{
  "bug": {
    "description": "Agent returns undefined instead of schema output",
    "severity": "High",
    "linearIssue": "PROJ-55"
  },
  "investigation": {
    "rootCause": "Handler missing return statement, schema output not validated",
    "issueType": "schema_validation",
    "affectedFiles": ["src/agent/Financial-Analyst/index.ts"],
    "reproSteps": [...]
  },
  "fix": {
    "approach": "Add return statement matching output schema, add eval to catch future regressions",
    "filesModified": [...],
    "linesChanged": 15,
    "agent": "agentuity-agent-architect"
  },
  "verification": {
    "testCases": [...],
    "evaluations": [...],
    "regressionRisk": "Low"
  },
  "status": "fixed|investigating|blocked"
}
```

### `triage`

Quick triage without full investigation.

**Inputs:**
- `description`: Bug description
- `linearIssue`: Issue ID (optional)

**Steps:**
1. Categorize severity
2. Assess impact
3. Identify affected layer (agent, route, frontend, storage)
4. Recommend priority
5. Return triage summary

**Outputs:**
```json
{
  "severity": "High",
  "impact": "Agent responses fail for all users",
  "layer": "agent",
  "issueCategory": "schema_validation",
  "recommendedPriority": "P1",
  "suggestedAssignee": "self",
  "workaround": "Use raw handler without schema temporarily"
}
```

### `analyzeOnly`

Root cause analysis without fix generation.

**Inputs:**
- `description`: Bug description
- `affectedFiles`: Files to analyze

**Steps:**
1. Run investigation phase
2. Run root cause analysis
3. Return analysis without fix

**Outputs:**
```json
{
  "rootCause": "...",
  "issueType": "...",
  "suggestedFix": "...",
  "recommendedAgent": "agentuity-agent-architect|agentuity-route-designer|react-spa-writer",
  "estimatedComplexity": "Low|Medium|High"
}
```

## Severity Classification

| Severity | Criteria | Response |
|----------|----------|----------|
| Critical | Production down, data loss, security breach | Immediate fix |
| High | Major feature broken, significant user impact | Same day |
| Medium | Feature degraded, workaround exists | This sprint |
| Low | Minor issue, cosmetic, edge case | Backlog |

## Issue Type Classification (Agentuity Specific)

| Type | Description | Typical Agent |
|------|-------------|---------------|
| `schema_validation` | Agent input/output doesn't match schema | `agentuity-agent-architect` |
| `state_management` | Thread state TTL, KV missing data | `agentuity-agent-architect` |
| `agent_communication` | Agent-to-agent call failure | `agentuity-agent-architect` |
| `ai_gateway` | Model error, rate limit, bad response | `agentuity-agent-architect` |
| `route_handler` | Hono route exception | `agentuity-route-designer` |
| `storage_error` | KV/vector/stream API failure | `agentuity-agent-architect` or `agentuity-route-designer` |
| `frontend_render` | React component error | `react-spa-writer` |
| `frontend_api` | Client fetch/data error | `react-spa-writer` |
| `build_error` | TypeScript or Vite build failure | Depends on affected layer |
| `logic_error` | Incorrect business logic | Depends on affected layer |

## Workflow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Triage    │────>│ Investigate │────>│  Root Cause │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                    ┌─────────────────────────┘
                    v
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Approval   │────>│  Fix via    │────>│   Verify    │
│ Checkpoint  │     │  Specialist │     │  & Deliver  │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Agent Routing

| Root Cause Area | Agent | Purpose |
|----------------|-------|---------|
| Agent handlers, schemas, storage, AI Gateway | `agentuity-agent-architect` | Agent-level fixes |
| Hono routes, middleware, cron, validation | `agentuity-route-designer` | Route-level fixes |
| React components, SPA routing, client API | `react-spa-writer` | Frontend fixes |
| Database/schema | `schema-designer` | Schema fixes |
| Test cases / agent evaluations | `test-planner` | Test and eval generation |

**This variant does NOT use the base `code-writer` agent.** All fix work is routed to specialized agents above.

## Dependencies

- **context-loader**: For bug context
- **mcp-sync**: For task management updates
- **session-management**: For state updates

## Approval Checkpoints

Workflow pauses for approval:
1. After root cause analysis (before fix)
2. Before applying fix to critical files

## Error Handling

| Error | Action |
|-------|--------|
| Cannot reproduce | Document attempts, request more info |
| Root cause unclear | Present multiple hypotheses |
| Fix introduces regression | Rollback, revise approach |
| Blocked by external | Mark as blocked, document dependency |

## Git Integration

Bug fixes follow this branch convention:
- Branch: `fix/{issue-id}-{short-description}`
- Commit: `fix({scope}): {description}`
- PR title: `Fix: {description} (#{issue-id})`
