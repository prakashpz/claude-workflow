---
description: Diagnose and fix bugs in Electron applications using specialist agents
---

# FixBug

Structured bug investigation and resolution workflow for Electron desktop applications.

## Purpose

Guides the bug fixing process using Electron specialist agents for diagnosis and fix generation, with awareness of main/renderer process architecture.

## Arguments

- `description`: Bug description (required)
- `linearIssue`: Task management issue ID (optional)
- `affectedFiles`: Known affected files (optional)
- `severity`: Initial severity assessment (optional: `critical` | `high` | `medium` | `low`)

## Execution

1. Invoke `bug-workflow` task with action: `investigate`
   - Triage: Categorize severity and impact
   - Investigation: Analyze code paths across main/renderer processes
   - Root Cause: Identify source of issue
   - Approval: Present findings before fix
   - Fix: Generate fix via specialist agents
   - Verification: Outline test cases

2. Display:
   - Severity and impact assessment
   - Root cause analysis (with process identification)
   - Fix approach
   - Test verification plan

## Prerequisites

- Bug description or task management issue

## Example

```
/FixBug description="Window state not restored on restart" affectedFiles=["src/main/window-manager.ts"]
```

## Workflow Phases

### 1. Triage
- Categorize: Critical / High / Medium / Low
- Identify affected process (main, renderer, or IPC)
- Assess platform specificity (macOS, Windows, Linux)

### 2. Investigation
- Reproduce the issue
- Check for common Electron pitfalls (IPC race conditions, context isolation, memory leaks)
- Analyze suspected code paths in both processes
- Review recent changes (git blame)

### 3. Root Cause Analysis
- Trace issue to source process and module
- Classify: IPC failure, memory leak, native API misuse, renderer crash, etc.
- Assess security implications (context isolation, node integration)

### 4. Approval Checkpoint
**STOP** - Present findings for review before proceeding

### 5. Fix Implementation
- Route to appropriate specialist agent based on root cause

### 6. Verification
- Define regression tests
- Outline manual verification (per-platform if needed)

## Tasks Invoked

- `bug-workflow.investigate`
- `context-loader.loadForBug`
- `mcp-sync.syncLinear`

## Agent Routing

| Root Cause Area | Agent | Purpose |
|----------------|-------|---------|
| Main process, native OS, window management | `electron-specialist` | Main process fixes |
| IPC communication, preload scripts | `ipc-architect` | IPC and channel fixes |
| Renderer UI, React components | `electron-specialist` | Renderer fixes |
| Database/storage | `schema-designer` | Storage fixes |
| Test cases | `test-planner` | Test generation |

**Do NOT route to `code-writer`** — this variant uses specialized agents for all fix work.
