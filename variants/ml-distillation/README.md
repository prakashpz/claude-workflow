# ML Distillation Variant

A Claude Workflow System variant for ML/AI R&D teams focused on model distillation, evaluation, benchmarking, experiment reproducibility, and documentation.

## Overview

This variant provides structured workflows for ML experiment lifecycles, covering the full pipeline from hypothesis definition through model publication. It is **tool-agnostic** - it defines workflow patterns and guidance without requiring specific MCP servers (W&B, HuggingFace, etc.) to be configured.

## Focus Areas

The variant covers 5 core ML R&D practices:

| # | Focus Area | Components |
|---|-----------|------------|
| 1 | **Success Measures & Evaluation** | `eval-benchmark-specialist`, `benchmark-suite` |
| 2 | **Distillation & Architecture** | `distillation-architect`, `experiment-lifecycle` |
| 3 | **Benchmarking & Comparison** | `eval-benchmark-specialist`, `benchmark-suite`, `/RunBenchmarks` |
| 4 | **Testing & Reproducibility** | `reproducibility-guardian`, `experiment-reproducibility` |
| 5 | **Documentation & Artifacts** | `experiment-documentarian`, `model-publishing`, `/DocumentExperiment` |

## Components

### Agents (4)

| Agent | Purpose |
|-------|---------|
| `distillation-architect` | Guide distillation strategy, architecture decisions, and compression methods |
| `eval-benchmark-specialist` | Define success criteria, select benchmarks, validate evaluation claims |
| `experiment-documentarian` | Produce experiment reports, model cards, and integration notes |
| `reproducibility-guardian` | Validate reproducibility, enforce shared frameworks, CI/CD for ML |

### Tasks (4)

| Task | Purpose |
|------|---------|
| `experiment-lifecycle` | Orchestrate experiments from planning through close-out |
| `benchmark-suite` | Manage benchmark execution, result storage, and cross-run comparison |
| `model-publishing` | Guide model publication to HuggingFace with naming and metadata |
| `experiment-reproducibility` | Validate environment, configs, baselines, and script promotion |

### Commands (4)

| Command | Purpose |
|---------|---------|
| `/PlanExperiment` | Plan a new experiment with hypothesis, success criteria, and benchmarks |
| `/RunBenchmarks` | Execute benchmark suite against a model, compare against baselines |
| `/PublishModel` | Publish model to HuggingFace with proper naming and model card |
| `/DocumentExperiment` | Generate experiment report or model card |

### Template (1)

| Template | Purpose |
|----------|---------|
| `CLAUDE.md.ml-distillation` | Project guidance for ML R&D with experiment workflows, conventions, and commands |

## Project Structure

The variant expects the following project structure:

```
project/
├── experiments/              # Per-experiment working directories
├── models/                   # Model checkpoints
├── datasets/                 # Dataset configs and processing
├── benchmarks/               # Evaluation suites, results, comparisons
│   ├── suites/
│   ├── results/
│   └── comparisons/
├── configs/                  # Version-controlled training configs
├── scripts/                  # Shared training and eval scripts
├── docs/                     # Documentation and experiment reports
│   └── experiments/
└── tests/                    # Tests for shared scripts
```

## Usage

### Setting Up a New Project

```bash
# Initialize with the ml-distillation variant
python scripts/init-project.py --variant ml-distillation /path/to/project
```

### Experiment Workflow

```bash
# 1. Plan an experiment
/PlanExperiment kl-distill-llama70b-to-8b --approach kd --teacher meta-llama/Llama-3-70B --student meta-llama/Llama-3-8B

# 2. Run training (manual step with generated configs)

# 3. Evaluate results
/RunBenchmarks ./models/exp-001-final --compare teacher-70b-baseline

# 4. Document findings
/DocumentExperiment exp-001 --format both

# 5. Publish if successful
/PublishModel ./models/exp-001-final --name agdata-corp/llama3-8b-llama3-70b-sft-general
```

## Dependencies

### Required

- `torch` - PyTorch for model training and inference
- `transformers` - HuggingFace Transformers for model loading and training
- `datasets` - HuggingFace Datasets for data loading
- `accelerate` - HuggingFace Accelerate for distributed training

### Optional

- `wandb` - Weights & Biases experiment tracking
- `lm-eval` - Language Model Evaluation Harness
- `vllm` - Fast inference for benchmarking throughput
- `bitsandbytes` - Quantization support
- `peft` - Parameter-efficient fine-tuning (LoRA, QLoRA)
- `trl` - Transformer Reinforcement Learning (DPO, GRPO, SFT trainers)

## Compatibility

- **Base version:** 2.0.0
- **Python:** 3.9+
- **PyTorch:** 2.0+
- **Transformers:** 4.36+
- **CUDA:** 11.8+ (for GPU workflows)

## Key Conventions

- **Every experiment produces a written artifact** - No verbal-only findings
- **Documentation during iteration, not after** - Update docs as you work
- **Benchmark claims require artifacts** - Reference specific result files
- **Default to private** - Models are private until release review
- **Pin all dependencies** - No unpinned versions in requirements
- **Config over code** - Hyperparameters in YAML, not hardcoded
- **Seeds everywhere** - Reproducibility starts with deterministic seeds
- **HuggingFace naming** - `{Org}/{Student}-{Teacher}-{TrainingType}-{DatasetType}`
