---
name: feature-workflow
description: Orchestrate feature implementation for Agentuity projects using specialist agents
---

# Feature Workflow Task (Agentuity Variant)

End-to-end orchestration for feature implementation in Agentuity projects, coordinating requirement discovery, specification generation, and routing to specialized agents for agents, routes, and frontend.

## Operations

### `implement`

Full feature implementation workflow.

**Inputs:**
- `feature`: Feature name or description
- `linearIssue`: Optional task management issue ID
- `stack`: Technology requirements (e.g., `["agent", "api", "ui", "storage"]`)
- `skipSpec`: Skip spec generation if already exists (default: false)

**Steps:**
1. **Discovery Phase:**
   - Invoke `requirement-discovery.discover(query: feature)`
   - Invoke `context-loader.loadForFeature(featureName: feature)`
   - If issue provided, fetch full details

2. **Specification Phase (unless skipSpec):**
   - Check for existing spec in `/docs/specs/`
   - If missing, generate feature specification:
     - Agent architecture (which agents needed, schemas, communication patterns)
     - API design (Hono routes, middleware, validation)
     - Frontend design (React components, routing, data flow)
     - Storage strategy (KV, vector, stream, thread state)
   - Write spec to `/docs/specs/{feature-name}.md`

3. **Approval Checkpoint:**
   - Present specification summary
   - List files to create/modify
   - Wait for user confirmation
   - If rejected, return to specification phase

4. **Implementation Phase:**
   - If `agent` in stack:
     - Route to `agentuity-agent-architect` agent with:
       - Agent spec, schema design, storage requirements, AI Gateway needs
   - If `api` in stack:
     - Route to `agentuity-route-designer` agent with:
       - Route spec, agent wiring, middleware, validation requirements
   - If `ui` in stack:
     - Route to `react-spa-writer` agent with:
       - Component spec, page design, API client integration
   - If `database` in stack:
     - Route to `schema-designer` agent
   - Collect generated code

5. **Integration Phase:**
   - Verify agent schemas match route validators
   - Verify API response shapes match frontend expectations
   - Check agent-to-agent wiring is correct
   - Verify storage namespace consistency

6. **Update Phase:**
   - Update task management issue with progress via `mcp-sync`
   - Update session state with completed work
   - Generate implementation summary

**Outputs:**
```json
{
  "feature": "Cash Flow Projection",
  "status": "completed|partial|blocked",
  "specification": {
    "path": "/docs/specs/cash-flow-projection.md",
    "generated": true
  },
  "implementation": {
    "filesCreated": [...],
    "filesModified": [...],
    "linesOfCode": 350
  },
  "linearUpdates": {
    "issueId": "PROJ-42",
    "newState": "In Review"
  },
  "nextSteps": [...]
}
```

### `plan`

Generate implementation plan without executing.

**Inputs:**
- `feature`: Feature name or description
- `linearIssue`: Optional issue ID

**Steps:**
1. Run discovery phase only
2. Generate specification
3. Create implementation plan with Agentuity-specific agent routing
4. Return plan without executing

**Outputs:**
```json
{
  "feature": "Cash Flow Projection",
  "plan": {
    "phases": [
      {
        "name": "Agent",
        "tasks": [...],
        "agent": "agentuity-agent-architect"
      },
      {
        "name": "API Routes",
        "tasks": [...],
        "agent": "agentuity-route-designer"
      },
      {
        "name": "Frontend",
        "tasks": [...],
        "agent": "react-spa-writer"
      }
    ],
    "estimatedFiles": 6,
    "dependencies": [...]
  }
}
```

### `resume`

Resume a partially completed feature.

**Inputs:**
- `feature`: Feature name
- `fromPhase`: Phase to resume from

**Steps:**
1. Load existing spec from `/docs/specs/`
2. Check session state for progress
3. Identify remaining work
4. Continue from specified phase

**Outputs:**
Same as `implement`

## Workflow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Discovery  │────>│   Spec Gen  │────>│  Approval   │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                    ┌─────────────────────────┘
                    v
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Agents    │────>│ API Routes  │────>│  Frontend   │
│agent-archit │     │route-design │     │ spa-writer  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                    ┌─────────────────────────┘
                    v
┌─────────────┐     ┌─────────────┐
│ Integration │────>│   Update    │
│   Verify    │     │   Tracking  │
└─────────────┘     └─────────────┘
```

## Agent Routing

| Requirement Type | Agent | Input |
|------------------|-------|-------|
| Agentuity agents, schemas, storage, AI | `agentuity-agent-architect` | Agent spec, patterns |
| Hono routes, middleware, cron | `agentuity-route-designer` | Route spec, agent wiring |
| React components, pages, layouts | `react-spa-writer` | Component spec, API contracts |
| Database schema | `schema-designer` | Requirements, existing schema |
| Tests and evaluations | `test-planner` | Implementation, acceptance criteria |

**This variant does NOT use the base `code-writer` agent.** All implementation work is routed to the specialized agents above.

## Specification Template

Generated specs follow this structure:

```markdown
# Feature: {name}

## Overview
{description}

## Requirements
{from requirement-discovery}

## Architecture

### Agents
- Agent name, purpose, schema, storage needs
- Agent-to-agent communication pattern

### API Routes
- Endpoint paths, methods, request/response shapes
- Agent wiring and middleware

### Frontend
- Components, pages, routing
- API client integration

### Storage Strategy
- KV namespaces and TTLs
- Vector indexes (if needed)
- Thread state usage

## Files to Create
- src/agent/{Name}/index.ts
- src/api/{path}.ts
- src/web/routes/{page}.tsx

## Files to Modify
- existing/file.ts - changes needed

## Testing Strategy
{outline including agent evaluations}

## Acceptance Criteria
{from requirements}
```

## Dependencies

- **requirement-discovery**: For requirements
- **context-loader**: For project context
- **mcp-sync**: For task management updates
- **session-management**: For state updates

## Agents Used

- **agentuity-agent-architect**: Agent creation and modification
- **agentuity-route-designer**: API route creation
- **react-spa-writer**: Frontend components and pages
- **schema-designer**: Database design (when needed)

## Error Handling

| Error | Action |
|-------|--------|
| Requirements not found | Prompt for manual input |
| Spec generation fails | Save partial, flag for review |
| Agent produces invalid code | Flag errors, request fixes |
| Task management update fails | Continue, retry at end |

## Approval Checkpoints

The workflow pauses for user approval at:
1. After specification generation
2. Before agent creation or modification
3. Before major file creation

Approvals prevent unintended changes and ensure alignment.
