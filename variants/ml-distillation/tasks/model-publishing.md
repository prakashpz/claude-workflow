---
name: model-publishing
description: Guide model publication to HuggingFace with proper naming, metadata, model cards, and branch strategy
---

# Model Publishing Task

Manages the publication of trained models to HuggingFace Hub with enforced naming conventions, proper metadata, model cards, and branch strategy. Ensures models are published with complete documentation and appropriate visibility settings.

## Operations

### `validateNaming`

Enforce the tokenized naming convention for HuggingFace model repositories.

**Inputs:**
- `studentModel`: Student model architecture name
- `teacherModel`: Teacher model name
- `trainingType`: Training approach used (sft, dpo, grpo, kd, quant)
- `datasetType`: Domain descriptor (general, code, math, medical, legal)
- `organization`: HuggingFace organization name

**Steps:**
1. Validate each token follows naming rules (lowercase, hyphenated)
2. Compose full name: `{org}/{student}-{teacher}-{trainingType}-{datasetType}`
3. Check for naming conflicts with existing repos
4. Return validated name

**Outputs:**
```json
{
  "validatedName": "agdata-corp/llama3-8b-llama3-70b-sft-general",
  "organization": "agdata-corp",
  "student": "llama3-8b",
  "teacher": "llama3-70b",
  "trainingType": "sft",
  "datasetType": "general",
  "isValid": true,
  "conflicts": []
}
```

**Naming Rules:**
- All tokens lowercase with hyphens
- Student model listed first
- Teacher model listed second
- Training type uses standard abbreviations: `sft`, `dpo`, `grpo`, `kd`, `quant`
- Dataset type is a single descriptor word or hyphenated compound

### `generateModelCard`

Create a HuggingFace README.md with YAML metadata following the model card specification.

**Inputs:**
- `modelName`: Validated HuggingFace model name
- `experimentId`: Source experiment identifier
- `benchmarkResults`: Benchmark results from evaluation
- `trainingConfig`: Training configuration used
- `modelDescription`: Human-readable description

**Steps:**
1. Generate YAML frontmatter with required fields (language, license, tags, base_model, datasets, pipeline_tag)
2. Add model-index with benchmark results
3. Generate markdown body sections (description, training, evaluation, usage, limitations)
4. Validate YAML frontmatter against HuggingFace schema
5. Write to model directory as README.md

**Outputs:**
```json
{
  "modelCardPath": "models/exp-001-final/README.md",
  "metadata": {
    "language": ["en"],
    "license": "apache-2.0",
    "tags": ["distillation", "llama"],
    "base_model": "meta-llama/Llama-3-8B",
    "pipeline_tag": "text-generation"
  },
  "sections": ["description", "training", "evaluation", "usage", "limitations"],
  "isValid": true
}
```

**Required YAML Fields:**
```yaml
---
language:
  - en
license: apache-2.0
tags:
  - distillation
  - {model-family}
base_model: {base-model-id}
datasets:
  - {dataset-name}
pipeline_tag: text-generation
model-index:
  - name: {model-name}
    results:
      - task:
          type: text-generation
        dataset:
          name: {benchmark-name}
          type: {benchmark-type}
        metrics:
          - name: {metric-name}
            type: {metric-type}
            value: {metric-value}
---
```

### `publishCheckpoint`

Validate branch strategy and publish model checkpoint to HuggingFace.

**Inputs:**
- `modelName`: Validated HuggingFace model name
- `checkpointPath`: Local path to model checkpoint
- `branch`: Target branch (main or experiment/)
- `visibility`: Repository visibility (private or public)
- `releaseTag`: Optional release tag

**Steps:**
1. Validate branch naming (never push directly to main without release review)
2. Validate model card exists and is complete
3. Validate checkpoint contains all required files (config.json, model weights, tokenizer)
4. Set repository visibility (default: private)
5. Push to HuggingFace with appropriate branch
6. Tag release if specified

**Outputs:**
```json
{
  "repoUrl": "https://huggingface.co/agdata-corp/llama3-8b-llama3-70b-sft-general",
  "branch": "experiment/exp-001",
  "visibility": "private",
  "releaseTag": null,
  "filesUploaded": ["config.json", "model.safetensors", "tokenizer.json", "README.md"],
  "status": "published"
}
```

**Branch Strategy:**
- `experiment/{experiment-id}` - For in-progress experiments (default)
- `main` - Only after release review and approval
- Never force-push to main

**Visibility Rules:**
- Default visibility is **private**
- Public visibility requires explicit release review
- Document visibility change in experiment log

### `updateCollection`

Add published model to a HuggingFace collection (Gold Standard or Project Collection).

**Inputs:**
- `modelName`: Published model identifier
- `collectionName`: Target collection (gold-standard, project-specific)
- `collectionNote`: Note explaining why this model is in the collection

**Steps:**
1. Validate model is published and has a complete model card
2. Validate model has passing benchmark results
3. Add to specified collection with note
4. Update collection description if needed

**Outputs:**
```json
{
  "collectionName": "gold-standard",
  "modelAdded": "agdata-corp/llama3-8b-llama3-70b-sft-general",
  "note": "Production-ready distillation with <5% quality degradation",
  "status": "added"
}
```

**Collection Types:**
- **Gold Standard**: Models validated for production use with full benchmark coverage
- **Project Collection**: All models from a specific project, including experimental

## Error Handling

| Error | Action |
|-------|--------|
| Naming convention violation | Reject and provide corrected name suggestion |
| Missing model card | Block publication, generate card template |
| Push to main without review | Block and require branch-based workflow |
| Missing checkpoint files | List required files, block publication |
| HuggingFace auth failure | Check HF_TOKEN, provide setup instructions |
| Public visibility without review | Block and require explicit approval |

## Key Rules

1. **Default visibility is private** - Public only after explicit release review
2. **Never push to main directly** - Use experiment branches, merge after review
3. **Model card is mandatory** - No publication without complete documentation
4. **Naming is enforced** - All models follow Student-Teacher-TrainingType-DatasetType convention
5. **Benchmark results required** - No publication without evaluation data in model card

## Dependencies

- **experiment-lifecycle**: Triggers publication after successful experiment close-out
- **benchmark-suite**: Provides benchmark results for model card
- **experiment-reproducibility**: Validates checkpoint completeness
- **documentation-sync**: Keeps project docs in sync with published models
