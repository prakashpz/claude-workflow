---
description: Diagnose and fix bugs in ML pipelines using specialist agents
---

# FixBug

Structured bug investigation and resolution workflow for ML/AI projects.

## Purpose

Guides bug fixing in ML projects using specialist agents for diagnosis across training, evaluation, data processing, and experiment infrastructure.

## Arguments

- `description`: Bug description (required)
- `linearIssue`: Task management issue ID (optional)
- `affectedFiles`: Known affected files (optional)
- `severity`: Initial severity assessment (optional: `critical` | `high` | `medium` | `low`)

## Execution

1. Invoke `bug-workflow` task with action: `investigate`
   - Triage: Categorize severity and impact
   - Investigation: Analyze code paths across ML pipeline
   - Root Cause: Identify source of issue
   - Approval: Present findings before fix
   - Fix: Generate fix via specialist agents
   - Verification: Outline test cases and validation

## Example

```
/FixBug description="Training loss diverges after epoch 5" affectedFiles=["scripts/train.py", "configs/lora.yaml"]
```

## Workflow Phases

### 1. Triage
- Categorize: Critical / High / Medium / Low
- Identify pipeline stage (data, training, evaluation, inference)
- Assess impact on experiments in progress

### 2. Investigation
- Reproduce the issue (check configs, seeds, data versions)
- Check for common ML pitfalls (gradient issues, data leakage, dtype mismatches)
- Analyze suspected code paths
- Review experiment logs and metrics

### 3. Root Cause Analysis
- Trace issue to source
- Classify: numerical instability, data corruption, config error, OOM, etc.
- Assess reproducibility of the issue

### 4. Approval Checkpoint
**STOP** - Present findings for review

### 5. Fix Implementation
- Route to appropriate specialist agent

### 6. Verification
- Define validation criteria (metrics, loss curves, memory usage)

## Agent Routing

| Root Cause Area | Agent | Purpose |
|----------------|-------|---------|
| Model architecture, training logic, distillation | `distillation-architect` | Training pipeline fixes |
| Evaluation metrics, benchmark code | `eval-benchmark-specialist` | Evaluation fixes |
| Experiment configs, environment, reproducibility | `reproducibility-guardian` | Infrastructure fixes |
| Documentation, experiment records | `experiment-documentarian` | Documentation fixes |
| Data storage/schema | `schema-designer` | Storage fixes |
| Test cases | `test-planner` | Test generation |

**Do NOT route to `code-writer`** — this variant uses specialized ML agents for all fix work.
