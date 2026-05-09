---
name: bug-workflow
description: Orchestrate bug investigation and fix delivery for ML/AI projects
---

# Bug Workflow Task (ML Distillation Variant)

Structured workflow for bug investigation and resolution in ML projects, with awareness of training pipelines, evaluation, and experiment infrastructure.

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
   - Identify pipeline stage (data, training, evaluation, inference, infrastructure)
   - Assess impact on active experiments
   - Check for workarounds
   - If issue provided, fetch full details via `mcp-sync`

2. **Investigation Phase:**
   - Invoke `context-loader.loadForBug` to gather context
   - Analyze suspected code paths
   - Check for common ML issues:
     - Gradient explosion/vanishing
     - Data leakage between train/eval splits
     - Dtype mismatches (fp16/bf16/fp32)
     - OOM errors (GPU memory)
     - Non-deterministic behavior (seeds, data loading)
     - Config inconsistencies
   - Review experiment logs, metrics, and wandb runs
   - Document minimal reproduction steps (including config and seed)

3. **Root Cause Analysis:**
   - Trace issue to source
   - Classify issue type:
     - Numerical instability (gradient, loss, activation)
     - Data corruption (preprocessing, tokenization, collation)
     - Config error (hyperparameters, paths, device mapping)
     - Memory issue (OOM, memory leak, fragmentation)
     - Reproducibility failure (seeds, non-determinism, environment)
     - Integration failure (API, model hub, tracking service)
   - Assess if systematic or edge case

4. **Approval Checkpoint:**
   - Present findings summary
   - Proposed fix approach
   - Risk to active experiments
   - Wait for user confirmation

5. **Fix Phase (after approval):**
   - Route to appropriate specialist agent:
     - Training/model bugs → `distillation-architect`
     - Evaluation/metric bugs → `eval-benchmark-specialist`
     - Config/reproducibility bugs → `reproducibility-guardian`
     - Documentation bugs → `experiment-documentarian`
   - Generate fix code
   - Include defensive improvements

6. **Verification Phase:**
   - Define validation criteria (metrics comparison, loss curves)
   - Check for regression risks
   - Verify experiment reproducibility maintained

7. **Delivery Phase:**
   - Update task management issue via `mcp-sync`
   - Update session state
   - Generate fix summary

**Outputs:**
```json
{
  "bug": {
    "description": "Training loss diverges after epoch 5",
    "severity": "High",
    "pipelineStage": "training"
  },
  "investigation": {
    "rootCause": "Learning rate warmup steps misconfigured causing gradient explosion",
    "issueType": "numerical_instability",
    "affectedFiles": [...],
    "experimentId": "exp-042"
  },
  "fix": {
    "approach": "Fix warmup scheduler config, add gradient clipping safeguard",
    "filesModified": [...],
    "agent": "distillation-architect"
  },
  "verification": {
    "validationCriteria": "Loss should decrease monotonically for first 10 epochs",
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
2. Identify pipeline stage
3. Assess impact on active experiments
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

## Issue Type Classification (ML Specific)

| Type | Description | Typical Agent |
|------|-------------|---------------|
| `numerical_instability` | Gradient/loss/activation issues | `distillation-architect` |
| `data_corruption` | Data pipeline issues | `distillation-architect` |
| `config_error` | Hyperparameter/path/device errors | `reproducibility-guardian` |
| `memory_issue` | OOM, memory leak, fragmentation | `distillation-architect` |
| `reproducibility_failure` | Non-deterministic results | `reproducibility-guardian` |
| `evaluation_error` | Wrong metrics, benchmark failures | `eval-benchmark-specialist` |
| `integration_failure` | API/hub/tracking service issues | `reproducibility-guardian` |

## Agent Routing

| Root Cause Area | Agent | Purpose |
|----------------|-------|---------|
| Model architecture, training, distillation | `distillation-architect` | Training fixes |
| Evaluation, benchmarks, metrics | `eval-benchmark-specialist` | Evaluation fixes |
| Configs, reproducibility, CI | `reproducibility-guardian` | Infrastructure fixes |
| Documentation, reports | `experiment-documentarian` | Documentation fixes |
| Data storage/schema | `schema-designer` | Storage fixes |
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
