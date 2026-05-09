---
name: experiment-lifecycle
description: Orchestrate an ML experiment from planning through close-out, ensuring all phases produce required artifacts
---

# Experiment Lifecycle Task

Manages the full lifecycle of an ML experiment across four phases: planning, execution, analysis, and close-out. Each phase has defined inputs, outputs, and quality gates that must be satisfied before progressing.

## Operations

### `planExperiment`

Define the experiment hypothesis, method, success criteria, and benchmark suite.

**Inputs:**
- `experimentName`: Descriptive name for the experiment
- `hypothesis`: What we expect to observe and why
- `approach`: Distillation method (kd, sft, dpo, grpo, quant)
- `teacherModel`: Teacher model identifier
- `studentBase`: Student base model identifier

**Steps:**
1. Create experiment directory under `experiments/{experiment-id}/`
2. Generate experiment document skeleton with intent and hypothesis
3. Define success criteria with `eval-benchmark-specialist` (quality + performance thresholds)
4. Select benchmark suite appropriate for the approach
5. Create training configuration file in `configs/`
6. Validate reproducibility requirements with `reproducibility-guardian`
7. Create tracking tickets if project management integration is active

**Outputs:**
```json
{
  "experimentId": "exp-2025-001",
  "experimentDir": "experiments/exp-2025-001/",
  "documentPath": "docs/experiments/exp-2025-001.md",
  "configPath": "configs/exp-2025-001.yaml",
  "successCriteria": {},
  "benchmarkSuite": [],
  "status": "planned"
}
```

### `executeExperiment`

Track training and evaluation runs, linking to artifact stores.

**Inputs:**
- `experimentId`: Experiment identifier from planning phase
- `trainingScript`: Path to the training script
- `configPath`: Path to the training configuration

**Steps:**
1. Validate environment with `reproducibility-guardian`
2. Confirm training config matches the experiment plan
3. Track training run (W&B run ID, start time, hardware)
4. Monitor for early stopping conditions or anomalies
5. Save checkpoints with consistent naming
6. Update experiment document with training observations

**Outputs:**
```json
{
  "experimentId": "exp-2025-001",
  "runId": "wandb-run-abc123",
  "checkpointPath": "models/exp-2025-001/checkpoint-final/",
  "trainingMetrics": {
    "loss": 0.42,
    "epochs_completed": 3,
    "wall_time_hours": 12.5
  },
  "status": "trained"
}
```

### `analyzeResults`

Compare experiment results against success criteria and label the outcome.

**Inputs:**
- `experimentId`: Experiment identifier
- `checkpointPath`: Path to the model checkpoint
- `baselineId`: Baseline experiment or model to compare against

**Steps:**
1. Run benchmark suite with `eval-benchmark-specialist`
2. Compare results against success criteria thresholds
3. Check for regressions in any capability category
4. Generate comparison table (current vs. baseline vs. thresholds)
5. Label outcome: `success`, `partial`, or `failure`
6. Update experiment document with results and interpretation

**Outputs:**
```json
{
  "experimentId": "exp-2025-001",
  "outcome": "partial",
  "benchmarkResults": {},
  "regressions": [],
  "comparisonTable": "docs/experiments/exp-2025-001.md#results",
  "status": "analyzed"
}
```

### `closeIteration`

Review all artifacts, update documentation, and determine next iteration.

**Inputs:**
- `experimentId`: Experiment identifier
- `outcome`: Result from analysis phase

**Steps:**
1. Verify all required artifacts exist (config, checkpoints, results, docs)
2. Run reproducibility checklist with `reproducibility-guardian`
3. Update experiment document with interpretation and next steps
4. If outcome is `success`: trigger model publishing workflow
5. If outcome is `partial` or `failure`: propose next iteration hypothesis
6. Update project status and metrics
7. Archive or clean up intermediate artifacts

**Outputs:**
```json
{
  "experimentId": "exp-2025-001",
  "outcome": "partial",
  "artifactChecklist": {
    "config": true,
    "checkpoint": true,
    "benchmarks": true,
    "document": true,
    "reproducibility": true
  },
  "nextIteration": "exp-2025-002",
  "nextHypothesis": "Add code-specific data to improve HumanEval retention",
  "status": "closed"
}
```

## Error Handling

| Error | Action |
|-------|--------|
| Missing success criteria at execution | Block execution, return to planning phase |
| Training divergence (loss NaN/explosion) | Stop run, document failure, propose hyperparameter adjustments |
| Benchmark suite failure | Retry with debug logging, escalate if persistent |
| Missing reproducibility artifacts at close | Block close-out, list missing artifacts |
| Environment mismatch between plan and execution | Warn, document deviation, assess impact on results |

## State Machine

```
planned → trained → analyzed → closed
    ↑                              |
    └──────── (next iteration) ────┘
```

Each state transition requires the previous phase's outputs to be complete and validated.

## Dependencies

- **benchmark-suite**: For executing evaluation benchmarks during analysis
- **experiment-reproducibility**: For validating reproducibility at plan and close-out
- **model-publishing**: For triggering publication of successful experiments
- **session-management**: For tracking experiment within project sessions
