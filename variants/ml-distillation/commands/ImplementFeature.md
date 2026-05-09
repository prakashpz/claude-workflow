---
description: Implement a feature end-to-end using ML specialist agents for experiment and model code
---

# ImplementFeature

Full feature implementation workflow for ML/AI projects, routing to distillation and experiment specialist agents.

## Purpose

Orchestrates feature implementation for ML projects: training pipelines, model architectures, evaluation harnesses, data processing, and experiment infrastructure.

## Arguments

- `feature`: Feature name or description (required)
- `linearIssue`: Task management issue ID (optional, for linking)
- `stack`: Technology requirements array (optional)
  - `database` - Requires data storage changes
  - `training` - Requires training pipeline work
  - `evaluation` - Requires benchmark/evaluation work
  - `infrastructure` - Requires experiment infrastructure
- `skipSpec`: Skip specification generation (default: false)

## Execution

1. Invoke `feature-workflow` task with action: `implement`
   - Discovery: Finds requirements from experiment plans, PRDs, documentation
   - Specification: Generates or loads feature spec
   - Approval: Presents plan for confirmation
   - Implementation: Routes to specialist agents (see Agent Routing)
   - Update: Syncs task management with progress

2. Display:
   - Requirements summary
   - Implementation plan
   - Generated code locations
   - Next steps

## Example

```
/ImplementFeature feature="LoRA fine-tuning pipeline" linearIssue="PROJ-401" stack=["training", "evaluation"]
```

## Tasks Invoked

- `feature-workflow.implement`
- `requirement-discovery.discover`
- `context-loader.loadForFeature`
- `mcp-sync.syncLinear`

## Agent Routing

| Requirement Type | Agent | When to Use |
|------------------|-------|-------------|
| Data storage/schema | `schema-designer` | Dataset metadata, experiment database |
| Model architecture, training pipelines, distillation | `distillation-architect` | Core ML implementation |
| Evaluation harnesses, benchmarks, metrics | `eval-benchmark-specialist` | Evaluation and benchmark code |
| Experiment configs, reproducibility, CI | `reproducibility-guardian` | Infrastructure and reproducibility |
| Documentation, model cards, reports | `experiment-documentarian` | Documentation generation |
| Tests | `test-planner` | Test specifications |

**Do NOT route to `code-writer`** — this variant uses specialized ML agents for all implementation work.

## Approval Checkpoints

The workflow pauses for approval:
1. After specification generation
2. Before data migrations
3. Before major training pipeline changes
