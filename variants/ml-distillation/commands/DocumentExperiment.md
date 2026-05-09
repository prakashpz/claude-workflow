---
name: DocumentExperiment
description: Generate experiment reports and model cards with hypothesis, method, results, interpretation, and artifact links
---

# /DocumentExperiment

Generate comprehensive experiment documentation including reports, model cards, or both. Ensures every experiment has a written artifact with full traceability from hypothesis to results.

## Usage

```
/DocumentExperiment <experiment-id> [options]
```

## Arguments

- `experiment-id`: Experiment identifier (required). Must match an existing experiment in `experiments/` or `docs/experiments/`.

## Options

- `--format <type>`: Output format. One of: `report`, `model-card`, `both` (default: `report`)
- `--update`: Update existing document instead of generating new (preserves manual edits)
- `--include-config`: Include full training configuration in the report
- `--include-logs`: Include training log excerpts (loss curves, learning rate schedule)
- `--wandb <run-id>`: Link to specific W&B run for artifact references

## Examples

```bash
# Generate experiment report
/DocumentExperiment exp-001

# Generate model card for HuggingFace
/DocumentExperiment exp-001 --format model-card

# Generate both report and model card
/DocumentExperiment exp-001 --format both

# Update existing report with new results
/DocumentExperiment exp-001 --update

# Full documentation with all extras
/DocumentExperiment exp-001 --format both --include-config --include-logs --wandb run-abc123
```

## Workflow

1. **Gather Experiment Data** (via `experiment-documentarian`)
   - Load experiment document from `docs/experiments/{experiment-id}.md`
   - Load training config from `configs/{experiment-id}.yaml`
   - Load benchmark results from `benchmarks/results/`
   - Load reproducibility report if available

2. **Generate Report** (if format is `report` or `both`)
   - Validate all required sections have content (intent, hypothesis, method)
   - Fill in results section from benchmark data
   - Generate interpretation guidance if results are available but interpretation is empty
   - Add artifact links (W&B, checkpoints, configs)
   - Add next steps recommendations based on outcome

3. **Generate Model Card** (if format is `model-card` or `both`)
   - Generate YAML frontmatter from experiment metadata
   - Create model description from hypothesis and method
   - Format benchmark results into model-index
   - Add training details, usage instructions, and limitations
   - Write to model directory as README.md

4. **Validate Completeness**
   - Check all required sections are filled
   - Verify artifact links are valid (paths exist, URLs are formatted)
   - Flag any sections still marked as "to be filled"
   - Report documentation completeness percentage

5. **Write Output**
   - Save or update experiment document
   - Save model card if requested
   - Print completeness summary

## Generated Report Structure

```markdown
# Experiment: {experiment-id}

**Status:** {status}
**Created:** {date}
**Closed:** {date or "In Progress"}
**Approach:** {approach}
**Outcome:** {success|partial|failure or "Pending"}

## Intent
Why this experiment exists and what question it addresses.

## Hypothesis
What we expected to observe and why.

## Method

### Training Approach
- **Type:** {sft|dpo|grpo|kd|quant}
- **Teacher:** {teacher model}
- **Student:** {student model}
- **Dataset:** {dataset}

### Configuration
- **Learning Rate:** {lr}
- **Epochs:** {epochs}
- **Batch Size:** {batch_size}
- **Hardware:** {gpu_type} x {gpu_count}
- **Training Time:** {hours}

## Results

### Quality Metrics
| Benchmark | Baseline | Result | Delta | Threshold | Status |
|-----------|----------|--------|-------|-----------|--------|

### Performance Metrics
| Metric | Baseline | Result | Delta | Target | Status |
|--------|----------|--------|-------|--------|--------|

## Interpretation
What the results mean in context of the hypothesis.

## Next Steps
What should be investigated next based on these findings.

## Artifacts
- **Training Config:** `configs/{experiment-id}.yaml`
- **Checkpoint:** `models/{experiment-id}/`
- **Benchmark Results:** `benchmarks/results/{label}/`
- **W&B Run:** {link}
- **HuggingFace Repo:** {link if published}

## Reproducibility
- **Environment:** Python {version}, CUDA {version}, PyTorch {version}
- **Seed:** {seed}
- **Dependencies:** `experiments/{experiment-id}/requirements.txt`
```

## Completeness Scoring

```
Documentation Completeness: 85%

Sections:
  ✓ Intent (complete)
  ✓ Hypothesis (complete)
  ✓ Method (complete)
  ✓ Results (complete)
  ✗ Interpretation (empty - needs human input)
  ✗ Next Steps (empty - needs human input)
  ✓ Artifacts (4/5 linked)
  ✓ Reproducibility (complete)
```

## Related Commands

- `/PlanExperiment` - Create the experiment that this documents
- `/RunBenchmarks` - Generate benchmark results for the report
- `/PublishModel` - Publish model with the generated model card
