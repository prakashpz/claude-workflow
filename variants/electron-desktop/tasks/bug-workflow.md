---
name: bug-workflow
description: Orchestrate bug investigation and fix delivery for Electron desktop applications
---

# Bug Workflow Task (Electron Variant)

Structured workflow for bug investigation and resolution in Electron applications, with awareness of main/renderer process architecture.

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
   - Identify affected process (main, renderer, or IPC)
   - Assess platform specificity (macOS, Windows, Linux)
   - Check for workarounds
   - If issue provided, fetch full details via `mcp-sync`

2. **Investigation Phase:**
   - Invoke `context-loader.loadForBug` to gather context
   - Analyze suspected code paths in affected process
   - Check for common Electron issues:
     - IPC race conditions or dropped messages
     - Context isolation violations
     - Memory leaks (renderer or main)
     - Native API errors (platform-specific)
     - Window state management issues
     - Auto-update failures
   - Review recent changes (git blame/log)
   - Document minimal reproduction steps

3. **Root Cause Analysis:**
   - Trace issue to source process and module
   - Classify issue type:
     - IPC failure (dropped/malformed messages)
     - Memory leak (renderer or main process)
     - Native API misuse (platform-specific)
     - Renderer crash (React error, state corruption)
     - Security issue (context isolation, node integration)
     - Build/packaging issue
   - Assess security implications

4. **Approval Checkpoint:**
   - Present findings summary
   - Proposed fix approach with process identification
   - Risk assessment
   - Wait for user confirmation

5. **Fix Phase (after approval):**
   - Route to appropriate specialist agent:
     - IPC issues -> `ipc-architect`
     - Main process / native / window issues -> `electron-specialist`
     - Renderer UI issues -> `electron-specialist`
   - Generate fix code
   - Include defensive improvements

6. **Verification Phase:**
   - Outline test cases for the fix
   - Check for regression risks
   - Note platform-specific verification needs

7. **Delivery Phase:**
   - Update task management issue via `mcp-sync`
   - Update session state
   - Generate fix summary

**Outputs:**
```json
{
  "bug": {
    "description": "Window state not restored on restart",
    "severity": "Medium",
    "process": "main"
  },
  "investigation": {
    "rootCause": "electron-store not persisting window bounds on close",
    "issueType": "native_api_misuse",
    "affectedFiles": [...],
    "platforms": ["all"]
  },
  "fix": {
    "approach": "Save window bounds in 'before-quit' event instead of 'close'",
    "filesModified": [...],
    "agent": "electron-specialist"
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
2. Identify affected process
3. Assess platform specificity
4. Recommend priority

### `analyzeOnly`

Root cause analysis without fix generation.

**Inputs:**
- `description`: Bug description
- `affectedFiles`: Files to analyze

**Steps:**
1. Run investigation phase
2. Run root cause analysis
3. Return analysis without fix

## Issue Type Classification (Electron Specific)

| Type | Description | Typical Agent |
|------|-------------|---------------|
| `ipc_failure` | IPC message handling issue | `ipc-architect` |
| `memory_leak` | Process memory growth | `electron-specialist` |
| `native_api_misuse` | Wrong native API usage | `electron-specialist` |
| `renderer_crash` | React/renderer error | `electron-specialist` |
| `security_issue` | Context isolation violation | `electron-specialist` |
| `build_issue` | Packaging/installer problem | `electron-specialist` |
| `platform_specific` | OS-specific behavior | `electron-specialist` |

## Agent Routing

| Root Cause Area | Agent | Purpose |
|----------------|-------|---------|
| IPC communication, preload scripts | `ipc-architect` | IPC fixes |
| Main process, native OS, windows | `electron-specialist` | Main process fixes |
| Renderer UI, React components | `electron-specialist` | Renderer fixes |
| Database/storage | `schema-designer` | Storage fixes |
| Test cases | `test-planner` | Test generation |

**This variant does NOT use the base `code-writer` agent.**

## Dependencies

- **context-loader**: For bug context
- **mcp-sync**: For task management updates
- **session-management**: For state updates

## Git Integration

Bug fixes follow this branch convention:
- Branch: `fix/{issue-id}-{short-description}`
- Commit: `fix({scope}): {description}`
- PR title: `Fix: {description} (#{issue-id})`
