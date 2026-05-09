---
name: PublishModel
description: Publish a trained model to HuggingFace with validated naming, model card, and proper branch strategy
---

# /PublishModel

Publish a model checkpoint to HuggingFace Hub with enforced naming conventions, complete model card, and appropriate branch strategy. Ensures models are published with full documentation and proper visibility settings.

## Usage

```
/PublishModel <model-path> [options]
```

## Arguments

- `model-path`: Path to the model checkpoint directory (required)

## Options

- `--name <hf-name>`: HuggingFace repository name following naming convention. If not provided, will be constructed interactively.
- `--collection <name>`: Add to a HuggingFace collection after publishing. One of: `gold-standard`, or a project-specific collection name.
- `--branch <name>`: Target branch (default: `experiment/{experiment-id}`)
- `--visibility <level>`: Repository visibility. One of: `private`, `public` (default: `private`)
- `--experiment <id>`: Source experiment ID for linking artifacts
- `--skip-validation`: Skip pre-publication checks (not recommended)

## Examples

```bash
# Publish to experiment branch (default, private)
/PublishModel ./models/exp-001-final --experiment exp-001

# Publish with explicit naming
/PublishModel ./models/exp-001-final --name agdata-corp/llama3-8b-llama3-70b-sft-general

# Publish to gold standard collection
/PublishModel ./models/exp-001-final --name agdata-corp/llama3-8b-llama3-70b-sft-general --collection gold-standard

# Publish to main branch (requires review)
/PublishModel ./models/exp-001-final --branch main --visibility public
```

## Workflow

1. **Validate Naming** (via `experiment-documentarian`)
   - If `--name` provided: validate against naming convention
   - If not provided: construct name interactively (student, teacher, training type, dataset type)
   - Check for naming conflicts with existing repositories

2. **Validate Checkpoint**
   - Verify checkpoint directory contains required files:
     - `config.json` - Model configuration
     - Model weights (`.safetensors` or `.bin`)
     - `tokenizer.json` or `tokenizer_config.json`
     - `special_tokens_map.json`
   - Verify model can be loaded successfully

3. **Generate Model Card** (via `experiment-documentarian`)
   - Create YAML frontmatter with metadata (language, license, tags, base_model, datasets, pipeline_tag)
   - Add benchmark results from experiment if `--experiment` specified
   - Generate markdown body (description, training details, evaluation, usage, limitations)
   - Write README.md to model directory

4. **Validate Branch Strategy**
   - If `--branch main`: require explicit confirmation and review
   - If `--branch experiment/*`: proceed with standard checks
   - Block force-pushes to any branch

5. **Publish to HuggingFace**
   - Create or update repository
   - Set visibility (default: private)
   - Push checkpoint and model card to target branch
   - Tag release if publishing to main

6. **Update Collection** (if `--collection` specified)
   - Verify model meets collection criteria
   - For `gold-standard`: require passing benchmarks and full documentation
   - Add model to collection with descriptive note

7. **Update Project State**
   - Record publication in experiment document
   - Update project status with published model reference

## Pre-Publication Checklist

```
[ ] Model loads successfully
[ ] Model card (README.md) is complete with YAML metadata
[ ] Naming follows convention: {org}/{student}-{teacher}-{type}-{domain}
[ ] Benchmark results included in model card
[ ] Branch is not main (or explicit approval given)
[ ] Visibility is private (or explicit approval for public)
[ ] Training config referenced in model card
[ ] Reproducibility artifacts available
```

## Output

```
Publishing: agdata-corp/llama3-8b-llama3-70b-sft-general
Branch: experiment/exp-001
Visibility: private

Pre-publication checks:
  ✓ Checkpoint valid (config.json, model.safetensors, tokenizer.json)
  ✓ Model card generated with YAML metadata
  ✓ Naming convention validated
  ✓ Benchmark results included (6 benchmarks)
  ✓ Branch strategy validated

Uploading files...
  → config.json
  → model.safetensors (14.5 GB)
  → tokenizer.json
  → special_tokens_map.json
  → README.md

Published: https://huggingface.co/agdata-corp/llama3-8b-llama3-70b-sft-general/tree/experiment/exp-001
```

## Related Commands

- `/PlanExperiment` - Plan the experiment that produced this model
- `/RunBenchmarks` - Generate benchmark results for the model card
- `/DocumentExperiment` - Generate detailed experiment documentation
