---
name: PlanExperiment
description: Plan a new ML experiment with hypothesis, success criteria, benchmark suite, and experiment document skeleton
---

# /PlanExperiment

Plan and set up a new ML experiment with structured hypothesis, success criteria, benchmark selection, and documentation skeleton. Ensures every experiment starts with clear objectives and measurable outcomes.

## Usage

```
/PlanExperiment <experiment-name> [options]
```

## Arguments

- `experiment-name`: Descriptive name for the experiment (required). Used as the basis for the experiment ID.

## Options

- `--approach <type>`: Distillation/training approach. One of: `kd`, `sft`, `dpo`, `grpo`, `quant`, `lora`, `custom` (default: `sft`)
- `--teacher <model>`: Teacher model identifier (e.g., `meta-llama/Llama-3-70B`)
- `--student <model>`: Student base model identifier (e.g., `meta-llama/Llama-3-8B`)
- `--dataset <name>`: Training dataset identifier
- `--domain <type>`: Target domain for success criteria. One of: `general`, `code`, `math`, `medical`, `legal`, `custom`

## Examples

```bash
# Basic distillation experiment
/PlanExperiment kl-distill-llama70b-to-8b --approach kd --teacher meta-llama/Llama-3-70B --student meta-llama/Llama-3-8B

# SFT with domain focus
/PlanExperiment sft-code-specialist --approach sft --teacher gpt-4-outputs --student meta-llama/Llama-3-8B --domain code

# DPO alignment experiment
/PlanExperiment dpo-alignment-v2 --approach dpo --dataset custom-preferences --domain general

# Quantization experiment
/PlanExperiment quant-int4-llama8b --approach quant --student meta-llama/Llama-3-8B
```

## Workflow

1. **Validate Input**
   - Verify experiment name follows naming convention (lowercase, hyphenated)
   - Check for existing experiments with the same name
   - Validate model identifiers if provided

2. **Gather Hypothesis** (via `distillation-architect`)
   - Define the core question the experiment addresses
   - State expected outcome and reasoning
   - Identify key risks and assumptions

3. **Define Success Criteria** (via `eval-benchmark-specialist`)
   - Set quality thresholds (benchmark scores with acceptable degradation ranges)
   - Set performance targets (throughput, latency, memory)
   - Set cost targets if applicable
   - Reference baseline measurements

4. **Select Benchmark Suite** (via `eval-benchmark-specialist`)
   - Choose standard benchmarks based on approach and domain
   - Add domain-specific benchmarks if applicable
   - Configure evaluation parameters

5. **Create Experiment Artifacts**
   - Create experiment directory: `experiments/{experiment-id}/`
   - Generate experiment document skeleton: `docs/experiments/{experiment-id}.md`
   - Create training config template: `configs/{experiment-id}.yaml`
   - Initialize reproducibility checklist

6. **Set Up Tracking**
   - Create experiment entry in project state
   - Link to W&B project if configured
   - Create project management tickets if integration is active

## Output Structure

```
experiments/{experiment-id}/
├── README.md                 # Quick reference
└── notes/                    # Working notes during experiment

configs/{experiment-id}.yaml  # Training configuration

docs/experiments/{experiment-id}.md  # Full experiment document
```

## Generated Experiment Document

```markdown
# Experiment: {experiment-id}

**Status:** Planned
**Created:** {date}
**Approach:** {approach}
**Author:** {author}

## Intent
{Why this experiment exists}

## Hypothesis
{Expected outcome and reasoning}

## Success Criteria

### Quality Metrics
| Benchmark | Baseline | Minimum | Target |
|-----------|----------|---------|--------|
| {benchmark} | {score} | {min} | {target} |

### Performance Metrics
| Metric | Baseline | Minimum | Target |
|--------|----------|---------|--------|
| Tokens/sec | {baseline} | {min} | {target} |

## Method
- **Approach:** {approach}
- **Teacher:** {teacher}
- **Student:** {student}
- **Dataset:** {dataset}
- **Key hyperparameters:** (to be filled during setup)

## Results
(to be filled after evaluation)

## Interpretation
(to be filled at close)

## Next Steps
(to be filled at close)

## Artifacts
- Config: `configs/{experiment-id}.yaml`
- Checkpoint: (to be filled)
- Benchmarks: (to be filled)
- W&B Run: (to be filled)
```

## Related Commands

- `/RunBenchmarks` - Execute benchmarks after training
- `/DocumentExperiment` - Generate full experiment report
- `/PublishModel` - Publish successful experiment results
