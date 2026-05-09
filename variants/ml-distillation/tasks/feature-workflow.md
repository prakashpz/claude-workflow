---
name: feature-workflow
description: Orchestrate feature implementation for ML/AI projects using specialist agents
---

# Feature Workflow Task (ML Distillation Variant)

End-to-end orchestration for feature implementation in ML projects, coordinating training pipelines, evaluation, and experiment infrastructure.

## Operations

### `implement`

Full feature implementation workflow.

**Inputs:**
- `feature`: Feature name or description
- `linearIssue`: Optional task management issue ID
- `stack`: Technology requirements (e.g., `["training", "evaluation", "infrastructure"]`)
- `skipSpec`: Skip spec generation if already exists (default: false)

**Steps:**
1. **Discovery Phase:**
   - Invoke `requirement-discovery.discover(query: feature)`
   - Invoke `context-loader.loadForFeature(featureName: feature)`
   - If issue provided, fetch full details

2. **Specification Phase (unless skipSpec):**
   - Check for existing spec in `/docs/specs/`
   - If missing, generate feature specification:
     - Model architecture decisions
     - Training pipeline design
     - Evaluation strategy
     - Experiment configuration
   - Write spec to `/docs/specs/{feature-name}.md`

3. **Approval Checkpoint:**
   - Present specification summary
   - List files to create/modify
   - Wait for user confirmation

4. **Implementation Phase:**
   - If `database` in stack:
     - Route to `schema-designer` agent for data storage design
   - If `training` in stack:
     - Route to `distillation-architect` agent with:
       - Model spec, training config, distillation strategy
   - If `evaluation` in stack:
     - Route to `eval-benchmark-specialist` agent with:
       - Metrics, benchmark suite, evaluation criteria
   - If `infrastructure` in stack:
     - Route to `reproducibility-guardian` agent with:
       - Config management, environment setup, CI integration
   - For documentation:
     - Route to `experiment-documentarian` agent
   - Collect generated code

5. **Integration Phase:**
   - Verify code aligns with spec
   - Check experiment reproducibility
   - Verify config consistency

6. **Update Phase:**
   - Update task management issue with progress via `mcp-sync`
   - Update session state with completed work
   - Generate implementation summary

**Outputs:**
```json
{
  "feature": "LoRA Fine-Tuning Pipeline",
  "status": "completed|partial|blocked",
  "specification": {
    "path": "/docs/specs/lora-pipeline.md",
    "generated": true
  },
  "implementation": {
    "filesCreated": [...],
    "filesModified": [...],
    "pipelineStages": ["data_prep", "training", "evaluation"]
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
3. Create implementation plan with ML-specific agent routing
4. Return plan without executing

**Outputs:**
```json
{
  "feature": "LoRA Pipeline",
  "plan": {
    "phases": [
      {
        "name": "Data Storage",
        "tasks": [...],
        "agent": "schema-designer"
      },
      {
        "name": "Training Pipeline",
        "tasks": [...],
        "agent": "distillation-architect"
      },
      {
        "name": "Evaluation Suite",
        "tasks": [...],
        "agent": "eval-benchmark-specialist"
      },
      {
        "name": "Reproducibility",
        "tasks": [...],
        "agent": "reproducibility-guardian"
      }
    ],
    "estimatedFiles": 10,
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
| Data storage/schema | `schema-designer` | Requirements, existing schema |
| Model architecture, training, distillation | `distillation-architect` | Model spec, training config |
| Evaluation, benchmarks, metrics | `eval-benchmark-specialist` | Eval criteria, benchmark suite |
| Reproducibility, configs, CI | `reproducibility-guardian` | Config requirements, environment |
| Documentation, model cards | `experiment-documentarian` | Experiment results, model info |
| Tests | `test-planner` | Implementation, acceptance criteria |

**This variant does NOT use the base `code-writer` agent.**

## Dependencies

- **requirement-discovery**: For requirements
- **context-loader**: For project context
- **mcp-sync**: For task management updates
- **session-management**: For state updates

## Agents Used

- **schema-designer**: Data storage design
- **distillation-architect**: Training pipeline and model code
- **eval-benchmark-specialist**: Evaluation and benchmark code
- **reproducibility-guardian**: Experiment infrastructure
- **experiment-documentarian**: Documentation

## Approval Checkpoints

The workflow pauses for user approval at:
1. After specification generation
2. Before data migrations
3. Before major training pipeline changes
