---
name: benchmark-suite
description: Manage benchmark definition, execution, result storage, and cross-run comparison for ML experiments
---

# Benchmark Suite Task

Manages the complete benchmark lifecycle: defining standard and custom evaluation suites, executing benchmarks, storing results in a comparable format, and diffing results across experiments. Enforces the rule that improvement claims must reference benchmark artifacts.

## Operations

### `defineDefaultBenchmarks`

Set the standard evaluation suite used across all experiments.

**Inputs:**
- `modelType`: Type of model being evaluated (causal-lm, seq2seq, embedding)
- `capabilities`: Target capabilities to evaluate (general, code, math, reasoning, domain-specific)

**Steps:**
1. Select standard benchmarks based on model type and capabilities
2. Define evaluation parameters (few-shot count, batch size, metrics)
3. Create benchmark suite configuration file
4. Validate that all required benchmark datasets are accessible

**Outputs:**
```json
{
  "suiteId": "default-causal-lm",
  "benchmarks": [
    {"name": "mmlu", "type": "multiple_choice", "fewshot": 5, "metric": "accuracy"},
    {"name": "hellaswag", "type": "multiple_choice", "fewshot": 10, "metric": "accuracy"},
    {"name": "arc_challenge", "type": "multiple_choice", "fewshot": 25, "metric": "accuracy"},
    {"name": "truthfulqa_mc2", "type": "multiple_choice", "fewshot": 0, "metric": "accuracy"},
    {"name": "humaneval", "type": "code_generation", "fewshot": 0, "metric": "pass@1"},
    {"name": "gsm8k", "type": "math", "fewshot": 5, "metric": "exact_match"}
  ],
  "configPath": "benchmarks/suites/default-causal-lm.yaml"
}
```

### `addClientBenchmark`

Extend the default suite with client-specific workloads.

**Inputs:**
- `suiteId`: Base suite to extend
- `clientName`: Client identifier
- `workloadDescription`: Description of the client-specific evaluation
- `evalDataPath`: Path to custom evaluation dataset
- `metric`: Evaluation metric for the custom benchmark

**Steps:**
1. Validate custom evaluation dataset format
2. Create evaluation script or LM-Eval task definition for the custom workload
3. Add to suite configuration with client tag
4. Run a sanity check on the custom benchmark with a known model

**Outputs:**
```json
{
  "suiteId": "default-causal-lm-clientA",
  "addedBenchmark": {
    "name": "clientA-support-tickets",
    "type": "custom",
    "evalDataPath": "benchmarks/data/clientA/support-tickets.jsonl",
    "metric": "f1",
    "baselinScore": 0.85
  },
  "configPath": "benchmarks/suites/default-causal-lm-clientA.yaml"
}
```

### `runBenchmarks`

Execute the evaluation suite against a model checkpoint.

**Inputs:**
- `modelPath`: Path to model checkpoint or HuggingFace model ID
- `suiteId`: Benchmark suite to execute
- `runLabel`: Human-readable label for this run
- `deviceMap`: GPU allocation (auto, specific device IDs)

**Steps:**
1. Load benchmark suite configuration
2. Validate model can be loaded
3. Execute each benchmark in the suite
4. Collect and format results
5. Store results in `benchmarks/results/{run-label}/`
6. Generate summary table

**Outputs:**
```json
{
  "runLabel": "exp-001-final",
  "suiteId": "default-causal-lm",
  "resultsDir": "benchmarks/results/exp-001-final/",
  "summary": {
    "mmlu": 0.69,
    "hellaswag": 0.78,
    "arc_challenge": 0.55,
    "truthfulqa_mc2": 0.48,
    "humaneval": 0.42,
    "gsm8k": 0.35
  },
  "detailedResults": "benchmarks/results/exp-001-final/detailed.json",
  "timestamp": "2025-01-15T14:30:00Z"
}
```

### `compareRuns`

Diff benchmark results across experiments to identify improvements and regressions.

**Inputs:**
- `currentRun`: Run label for the current experiment
- `baselineRun`: Run label for the baseline comparison
- `thresholds`: Acceptable degradation thresholds per metric

**Steps:**
1. Load results for both runs
2. Align benchmarks (handle cases where suites differ)
3. Compute deltas and percentage changes
4. Flag regressions that exceed thresholds
5. Generate comparison report

**Outputs:**
```json
{
  "comparison": {
    "current": "exp-001-final",
    "baseline": "teacher-70b-baseline",
    "benchmarks": {
      "mmlu": {"baseline": 0.72, "current": 0.69, "delta": -0.03, "pct": -4.2, "status": "pass"},
      "humaneval": {"baseline": 0.45, "current": 0.42, "delta": -0.03, "pct": -6.7, "status": "warn"},
      "tokens_per_sec": {"baseline": 45, "current": 180, "delta": 135, "pct": 300, "status": "pass"}
    },
    "regressions": ["humaneval"],
    "improvements": ["tokens_per_sec"],
    "overallStatus": "pass_with_warnings"
  },
  "reportPath": "benchmarks/comparisons/exp-001-vs-teacher.md"
}
```

## Result Storage Convention

All benchmark results follow a consistent directory structure:

```
benchmarks/
├── suites/                    # Suite definitions
│   ├── default-causal-lm.yaml
│   └── default-causal-lm-clientA.yaml
├── results/                   # Per-run results
│   ├── teacher-70b-baseline/
│   │   ├── summary.json
│   │   ├── detailed.json
│   │   └── per-task/
│   └── exp-001-final/
│       ├── summary.json
│       ├── detailed.json
│       └── per-task/
└── comparisons/               # Cross-run comparisons
    └── exp-001-vs-teacher.md
```

## Error Handling

| Error | Action |
|-------|--------|
| Model fails to load | Report error with model path and device info, do not proceed |
| Benchmark dataset not found | Skip benchmark, log warning, report incomplete suite |
| OOM during evaluation | Reduce batch size, retry; if persistent, document hardware limitation |
| Mismatched suite between runs | Compare only overlapping benchmarks, note missing comparisons |
| Stale baseline results | Warn if baseline is older than configurable threshold (default 30 days) |

## Key Rules

1. **Benchmark outputs are stored and comparable across runs** - Results must be saved in the standard format, never discarded
2. **Improvement claims must reference artifacts** - No claim without a `benchmarks/results/` path and run label
3. **Multiple runs for stochastic metrics** - Code generation benchmarks (HumanEval, MBPP) require minimum 3 runs
4. **Client benchmarks are additive** - Custom benchmarks extend the default suite, never replace it

## Dependencies

- **experiment-lifecycle**: Triggers benchmark runs during the analysis phase
- **experiment-reproducibility**: Ensures benchmark environment is reproducible
- **quality-gates**: Uses benchmark results as quality gate criteria
