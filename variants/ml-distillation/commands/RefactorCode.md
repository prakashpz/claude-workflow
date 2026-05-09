---
description: Plan and execute code refactoring in ML projects using specialist agents
---

# RefactorCode

Structured code refactoring for ML/AI projects with experiment safety and reproducibility awareness.

## Purpose

Guides refactoring using ML specialist agents, ensuring experiment reproducibility is maintained and training pipelines remain functional.

## Arguments

- `target`: File, module, or pattern to refactor (required)
- `goal`: Refactoring goal (optional)
  - `simplify` - Reduce complexity
  - `extract` - Extract reusable components
  - `consolidate` - Merge duplicate code
  - `modernize` - Update to current ML patterns and libraries
- `linearIssue`: Task management issue ID (optional)

## Execution

1. Invoke `feature-workflow` task with action: `plan` (refactor mode)
   - Analysis: Assess current code structure
   - Plan: Generate refactoring plan
   - Approval: Present plan for confirmation
   - Implementation: Execute via specialist agents
   - Verification: Ensure reproducibility maintained

## Refactoring Types

| Goal | Description | Risk Level |
|------|-------------|------------|
| `simplify` | Reduce complexity in training scripts | Low |
| `extract` | Extract reusable training/eval utilities | Medium |
| `consolidate` | Merge duplicate model/pipeline implementations | Medium |
| `modernize` | Update to latest transformers/torch patterns | High |

## Safety Checks

Before refactoring:
- Verify experiment reproducibility baseline
- Check for active experiments using target code
- Note config dependencies

After refactoring:
- Re-run baseline experiment to verify reproducibility
- Verify metrics match pre-refactor baseline
- Run existing tests

## Agent Routing

| Target Type | Agent | Purpose |
|-------------|-------|---------|
| Model architecture, training loops | `distillation-architect` | Training code refactoring |
| Evaluation/benchmark code | `eval-benchmark-specialist` | Evaluation refactoring |
| Experiment configs, CI/CD | `reproducibility-guardian` | Infrastructure refactoring |
| Documentation | `experiment-documentarian` | Documentation refactoring |

**Do NOT route to `code-writer`** — this variant uses specialized ML agents for all refactoring work.

## Approval Checkpoint

The workflow pauses for approval after the refactoring plan is generated, before any code changes.
