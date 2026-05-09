---
description: Plan and execute code refactoring in Electron applications using specialist agents
---

# RefactorCode

Structured code refactoring with Electron architecture awareness and safety checks.

## Purpose

Guides refactoring using Electron specialist agents, respecting main/renderer process boundaries and security constraints.

## Arguments

- `target`: File, module, or pattern to refactor (required)
- `goal`: Refactoring goal (optional)
  - `simplify` - Reduce complexity
  - `extract` - Extract reusable modules
  - `consolidate` - Merge duplicate code
  - `modernize` - Update to current Electron patterns
- `linearIssue`: Task management issue ID (optional)

## Execution

1. Invoke `feature-workflow` task with action: `plan` (refactor mode)
   - Analysis: Assess current code structure with process boundary awareness
   - Plan: Generate refactoring plan
   - Approval: Present plan for confirmation
   - Implementation: Execute via specialist agents
   - Verification: Ensure no regressions

## Refactoring Types

| Goal | Description | Risk Level |
|------|-------------|------------|
| `simplify` | Reduce complexity | Low |
| `extract` | Extract shared logic to shared/ module | Medium |
| `consolidate` | Merge duplicate implementations across processes | Medium |
| `modernize` | Update to current Electron patterns and security best practices | High |

## Safety Checks

Before refactoring:
- Identify main/renderer process boundaries
- Check context isolation compliance
- Verify IPC channel contracts
- Check for test coverage

After refactoring:
- Verify IPC still works correctly
- Run existing tests
- Platform-specific verification

## Agent Routing

| Target Type | Agent | Purpose |
|-------------|-------|---------|
| Main process code | `electron-specialist` | Main process refactoring |
| IPC channels, preload scripts | `ipc-architect` | IPC refactoring |
| Renderer components | `electron-specialist` | Renderer refactoring |
| Database/storage | `schema-designer` | Schema refactoring |

**Do NOT route to `code-writer`** — this variant uses specialized agents for all refactoring work.

## Approval Checkpoint

The workflow pauses for approval after the refactoring plan is generated, before any code changes.
