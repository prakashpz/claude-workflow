---
name: feature-workflow
description: Orchestrate feature implementation for Electron desktop applications using specialist agents
---

# Feature Workflow Task (Electron Variant)

End-to-end orchestration for feature implementation in Electron applications, coordinating across main process, renderer, and IPC layers.

## Operations

### `implement`

Full feature implementation workflow.

**Inputs:**
- `feature`: Feature name or description
- `linearIssue`: Optional task management issue ID
- `stack`: Technology requirements (e.g., `["native", "ui", "database"]`)
- `skipSpec`: Skip spec generation if already exists (default: false)

**Steps:**
1. **Discovery Phase:**
   - Invoke `requirement-discovery.discover(query: feature)`
   - Invoke `context-loader.loadForFeature(featureName: feature)`
   - If issue provided, fetch full details

2. **Specification Phase (unless skipSpec):**
   - Check for existing spec in `/docs/specs/`
   - If missing, generate feature specification:
     - Process architecture (main vs renderer responsibilities)
     - IPC channel design (if cross-process communication needed)
     - File structure plan
     - Native API requirements
   - Write spec to `/docs/specs/{feature-name}.md`

3. **Approval Checkpoint:**
   - Present specification summary
   - List files to create/modify (organized by process)
   - Wait for user confirmation

4. **Implementation Phase:**
   - If `database` in stack:
     - Route to `schema-designer` agent for storage design
   - If IPC communication needed:
     - Route to `ipc-architect` agent for channel design and preload scripts
   - Route to `electron-specialist` agent for:
     - Main process logic (window management, native APIs, app lifecycle)
     - Renderer components (React UI, state management, theming)
   - Collect generated code

5. **Integration Phase:**
   - Verify IPC contracts between main and renderer
   - Check security (context isolation, no exposed Node APIs)
   - Verify code aligns with spec

6. **Update Phase:**
   - Update task management issue with progress via `mcp-sync`
   - Update session state with completed work
   - Generate implementation summary

**Outputs:**
```json
{
  "feature": "File Drag-and-Drop Import",
  "status": "completed|partial|blocked",
  "specification": {
    "path": "/docs/specs/file-import.md",
    "generated": true
  },
  "implementation": {
    "filesCreated": [...],
    "filesModified": [...],
    "processes": ["main", "renderer"],
    "ipcChannels": ["file:import", "file:import-result"]
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
3. Create implementation plan with Electron-specific routing
4. Return plan without executing

**Outputs:**
```json
{
  "feature": "File Import",
  "plan": {
    "phases": [
      {
        "name": "Storage",
        "tasks": [...],
        "agent": "schema-designer"
      },
      {
        "name": "IPC Channels",
        "tasks": [...],
        "agent": "ipc-architect"
      },
      {
        "name": "Main Process",
        "tasks": [...],
        "agent": "electron-specialist"
      },
      {
        "name": "Renderer UI",
        "tasks": [...],
        "agent": "electron-specialist"
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

## Agent Routing

| Requirement Type | Agent | Input |
|------------------|-------|-------|
| Database/storage | `schema-designer` | Requirements, existing schema |
| IPC channels, preload scripts | `ipc-architect` | Channel spec, security requirements |
| Main process, native OS, windows | `electron-specialist` | Architecture requirements |
| Renderer UI, React components | `electron-specialist` | Component spec, design system |
| Tests | `test-planner` | Implementation, acceptance criteria |

**This variant does NOT use the base `code-writer` agent.**

## Dependencies

- **requirement-discovery**: For requirements
- **context-loader**: For project context
- **mcp-sync**: For task management updates
- **session-management**: For state updates

## Agents Used

- **schema-designer**: Database/storage design
- **ipc-architect**: IPC communication design
- **electron-specialist**: Main process and renderer implementation

## Approval Checkpoints

The workflow pauses for user approval at:
1. After specification generation
2. Before storage migrations
3. Before major file creation
