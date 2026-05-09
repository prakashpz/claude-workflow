---
name: RunBenchmarks
description: Execute benchmark suite against a model checkpoint, store results, and compare against baselines
---

# /RunBenchmarks

Execute an evaluation benchmark suite against a model, store results in a comparable format, and optionally compare against a baseline. Ensures all evaluation claims are backed by reproducible artifacts.

## Usage

```
/RunBenchmarks <model-path> [options]
```

## Arguments

- `model-path`: Path to model checkpoint directory or HuggingFace model ID (required)

## Options

- `--suite <name>`: Benchmark suite to execute. One of: `default`, `client`, `full`, or a custom suite name (default: `default`)
- `--compare <baseline>`: Baseline run label or model path to compare against
- `--label <name>`: Human-readable label for this run (default: auto-generated from model path and timestamp)
- `--device <ids>`: GPU device IDs to use (default: `auto`)
- `--batch-size <n>`: Override batch size for evaluation (default: from suite config)
- `--num-runs <n>`: Number of evaluation runs for stochastic metrics (default: `1`, minimum `3` for code generation)

## Examples

```bash
# Run default benchmarks
/RunBenchmarks ./models/exp-001-final

# Run with baseline comparison
/RunBenchmarks ./models/exp-001-final --compare teacher-70b-baseline --label exp-001-final

# Run client-specific suite
/RunBenchmarks ./models/exp-001-final --suite client --compare exp-001-baseline

# Run full suite with multiple runs for code metrics
/RunBenchmarks ./models/exp-001-final --suite full --num-runs 3 --label exp-001-full-eval

# Run against HuggingFace model
/RunBenchmarks agdata-corp/llama3-8b-llama3-70b-sft-general --suite default --compare meta-llama/Llama-3-8B
```

## Workflow

1. **Validate Input** (via `eval-benchmark-specialist`)
   - Verify model can be loaded from the specified path
   - Load benchmark suite configuration
   - Validate device availability and memory for model size

2. **Execute Benchmarks**
   - Run each benchmark in the suite sequentially
   - Collect per-task and aggregate results
   - For stochastic metrics (pass@k), run multiple times if `--num-runs > 1`
   - Track execution time per benchmark

3. **Store Results**
   - Save results to `benchmarks/results/{label}/`
   - Generate `summary.json` with aggregate scores
   - Generate `detailed.json` with per-sample results
   - Save per-task breakdowns to `per-task/` directory

4. **Compare Against Baseline** (if `--compare` specified)
   - Load baseline results
   - Compute deltas and percentage changes per benchmark
   - Flag regressions exceeding configured thresholds
   - Generate comparison markdown report

5. **Generate Summary**
   - Print results table to console
   - Highlight regressions in red, improvements in green
   - Output comparison report path if baseline was provided

## Output Structure

```
benchmarks/results/{label}/
├── summary.json              # Aggregate scores
├── detailed.json             # Per-sample results
├── per-task/                 # Per-benchmark breakdowns
│   ├── mmlu.json
│   ├── humaneval.json
│   └── ...
└── metadata.json             # Run metadata (model, suite, device, timestamp)
```

## Console Output Example

```
Benchmark Results: exp-001-final
Suite: default-causal-lm | Device: cuda:0,1 | Date: 2025-01-15

┌──────────────────┬──────────┬──────────┬────────┬────────┐
│ Benchmark        │ Baseline │ Current  │ Delta  │ Status │
├──────────────────┼──────────┼──────────┼────────┼────────┤
│ MMLU (5-shot)    │ 0.720    │ 0.690    │ -0.030 │ PASS   │
│ HellaSwag        │ 0.840    │ 0.810    │ -0.030 │ PASS   │
│ ARC-Challenge    │ 0.580    │ 0.550    │ -0.030 │ PASS   │
│ TruthfulQA       │ 0.490    │ 0.470    │ -0.020 │ PASS   │
│ HumanEval (p@1)  │ 0.450    │ 0.420    │ -0.030 │ WARN   │
│ GSM8K            │ 0.380    │ 0.350    │ -0.030 │ PASS   │
├──────────────────┼──────────┼──────────┼────────┼────────┤
│ Tokens/sec       │ 45       │ 180      │ +135   │ PASS   │
│ Memory (GB)      │ 40.0     │ 7.2      │ -32.8  │ PASS   │
└──────────────────┴──────────┴──────────┴────────┴────────┘

Overall: PASS (1 warning)
Results: benchmarks/results/exp-001-final/
Comparison: benchmarks/comparisons/exp-001-final-vs-teacher-70b-baseline.md
```

## Related Commands

- `/PlanExperiment` - Plan experiment with benchmark suite selection
- `/DocumentExperiment` - Include benchmark results in experiment report
- `/PublishModel` - Publish model with benchmark results in model card
