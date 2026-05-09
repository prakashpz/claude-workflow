---
name: experiment-reproducibility
description: Validate and enforce experiment reproducibility through environment checks, config versioning, baseline tests, and script promotion
---

# Experiment Reproducibility Task

Validates that ML experiments can be reproduced by any team member on any compatible hardware. Enforces shared frameworks and blocks experiment completion when reproducibility requirements are not met.

## Operations

### `validateEnvironment`

Check that Python dependencies are pinned and hardware environment is documented.

**Inputs:**
- `experimentDir`: Path to the experiment directory
- `requirementsPath`: Path to requirements file (requirements.txt, pyproject.toml, or environment.yml)

**Steps:**
1. Check that a dependency file exists and is not empty
2. Verify all dependencies have pinned versions (no `>=`, `~=`, or missing versions)
3. Check Python version is documented
4. Check CUDA version is documented (if GPU experiment)
5. Verify no local-only paths in requirements (no `file://` or `-e .` for team deps)
6. Generate environment report

**Outputs:**
```json
{
  "status": "pass",
  "pythonVersion": "3.10.12",
  "cudaVersion": "12.1",
  "totalDependencies": 45,
  "pinnedDependencies": 45,
  "unpinnedDependencies": [],
  "warnings": [],
  "reportPath": "experiments/exp-001/environment-report.json"
}
```

**Failure Conditions:**
- Any unpinned dependency → `fail`
- Missing Python version → `warn`
- Missing CUDA version for GPU experiment → `warn`
- Local paths in requirements → `fail`

### `validateConfig`

Ensure training configurations are version-controlled and complete.

**Inputs:**
- `configPath`: Path to the training configuration file
- `experimentId`: Experiment identifier for cross-referencing

**Steps:**
1. Validate config file exists and is valid YAML/JSON
2. Check all required fields are present (model, training params, data, seed)
3. Verify config is tracked by git (not in .gitignore)
4. Check for hardcoded absolute paths
5. Validate hyperparameter ranges are reasonable
6. Cross-reference with experiment document

**Outputs:**
```json
{
  "status": "pass",
  "configPath": "configs/exp-001.yaml",
  "isTracked": true,
  "requiredFields": {
    "model": true,
    "training": true,
    "data": true,
    "seed": true
  },
  "hardcodedPaths": [],
  "warnings": []
}
```

**Required Config Fields:**
```yaml
# Minimum required fields
experiment:
  name: string       # Experiment identifier
  seed: integer      # Random seed

model:
  name: string       # Model identifier or path
  # Additional model-specific fields

training:
  learning_rate: float
  num_epochs: integer
  batch_size: integer

data:
  dataset: string    # Dataset identifier or path
```

### `runBaselineTests`

Execute model loading, inference sanity, and regression checks.

**Inputs:**
- `checkpointPath`: Path to the model checkpoint
- `baselineResults`: Optional path to baseline benchmark results for regression check
- `testConfig`: Optional custom test configuration

**Steps:**
1. **Model loading test**: Load model from checkpoint, verify all weights loaded
2. **Tokenizer test**: Load tokenizer, verify encode/decode roundtrip
3. **Inference sanity test**: Generate output for 5 standard prompts, verify non-degenerate output
4. **Memory footprint**: Measure GPU memory usage
5. **Regression check**: If baseline provided, compare key metrics
6. Generate test report

**Outputs:**
```json
{
  "status": "pass",
  "tests": {
    "modelLoading": {"status": "pass", "loadTimeSeconds": 12.5},
    "tokenizerRoundtrip": {"status": "pass"},
    "inferenceSanity": {"status": "pass", "samplesGenerated": 5, "allNonDegenerate": true},
    "memoryFootprint": {"status": "pass", "peakMemoryGB": 7.2},
    "regressionCheck": {"status": "pass", "regressedMetrics": []}
  },
  "reportPath": "experiments/exp-001/baseline-test-report.json"
}
```

**Sanity Check Criteria:**
- Output is not empty
- Output is not a single repeated token
- Output length is within expected range
- Output does not contain degenerate patterns (all punctuation, all whitespace)

### `promoteToShared`

Move local experiment scripts to shared repository pipelines.

**Inputs:**
- `scriptPaths`: List of local scripts to promote
- `targetDir`: Target directory in shared pipeline (e.g., `scripts/training/`, `scripts/eval/`)
- `experimentId`: Source experiment for attribution

**Steps:**
1. Scan scripts for local-only patterns (hardcoded paths, personal references, untracked imports)
2. Report issues found and required changes
3. Validate scripts use config files instead of hardcoded parameters
4. Check CLI argument parsing or config file loading is present
5. Verify type hints on public functions
6. Create or update minimal test for each script
7. Move scripts to shared location
8. Update imports and references

**Outputs:**
```json
{
  "status": "pass",
  "promotedScripts": [
    {
      "source": "experiments/exp-001/train.py",
      "destination": "scripts/training/kl_distillation.py",
      "issuesFixed": ["hardcoded_path", "missing_cli_args"],
      "testCreated": "tests/test_kl_distillation.py"
    }
  ],
  "blockers": [],
  "warnings": []
}
```

**Promotion Checklist:**
- [ ] No hardcoded absolute paths
- [ ] No personal environment variable names
- [ ] All imports available in requirements.txt
- [ ] Config loaded from file or CLI arguments
- [ ] Public functions have type hints
- [ ] Minimal test exists
- [ ] Script runs with `--help` flag

## Error Handling

| Error | Action |
|-------|--------|
| Unpinned dependencies | List unpinned deps with current installed versions for easy pinning |
| Missing config fields | List missing fields with expected types |
| Model fails to load | Report error details, check checkpoint completeness |
| Degenerate inference output | Flag with examples, suggest investigation steps |
| Hardcoded paths in scripts | Report locations with suggested replacements |
| Untracked config file | Add to git tracking, warn about gitignore patterns |

## Quality Gates

This task enforces the following quality gates:

1. **Pre-execution gate**: Environment and config must validate before training starts
2. **Post-training gate**: Baseline tests must pass before benchmarking
3. **Pre-publication gate**: All reproducibility checks must pass before model publishing
4. **Promotion gate**: Scripts must pass all checklist items before moving to shared pipelines

## Dependencies

- **experiment-lifecycle**: Triggers reproducibility checks at planning and close-out phases
- **benchmark-suite**: Baseline tests feed into benchmark execution
- **model-publishing**: Blocks publication when reproducibility requirements are unmet
- **ci-integration**: Promoted scripts are added to CI pipelines
