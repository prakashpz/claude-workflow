# How We Work — Workflow Automation Companion

This document explains how the `ml-distillation` workflow variant translates our "How We Work" practices into an automated, enforceable system inside the developer's editor. It is intended to be read alongside the original How We Work PDF.

## What This Is

The How We Work document defines *what* our ML R&D team does and *why*. This workflow variant makes those practices the default path for every engineer using Claude Code. Instead of relying on memory, discipline, or post-hoc review to follow our SOPs, the workflow encodes them directly into the tools people use every day.

It does not replace the How We Work document. It operationalizes it.

## What It Actually Does

When an engineer starts an experiment, the workflow walks them through a structured process that matches our SOPs. It is not a CI pipeline or a platform tool — it is guidance and enforcement built into the coding assistant, ensuring the right steps happen in the right order and the right artifacts are produced.

Here is what changes in practice across each of our five focus areas.

### 1. Success Measures and Evaluation

**The SOP says:** Every iteration begins with written success criteria — quality thresholds, performance targets, and acceptable degradation ranges — defined before work starts.

**The workflow enforces this by:**
- Requiring success criteria as part of experiment planning. When an engineer runs `/PlanExperiment`, the system asks for measurable quality and performance targets before anything else.
- Structuring criteria as tables with baseline, minimum, and target columns so there is no ambiguity about what "good enough" means.
- Carrying these criteria forward into benchmarking and close-out, so results are always compared against what was agreed at the start.

**What this prevents:** Experiments that drift without clear goals. Post-hoc rationalization of results. "We think it's better" without numbers.

### 2. Distillation and Architecture

**The SOP says:** Distillation approach selection should be deliberate, documented, and justified. Architecture changes require rationale. No accidental model invention.

**The workflow enforces this by:**
- Providing a distillation architect agent that guides strategy selection based on the trade-off triangle: quality preservation, performance gains, and training cost.
- Requiring that architecture decisions are proposed as discrete tasks with documented rationale, not buried in code changes.
- Covering the full range of our approaches (KL divergence, SFT, DPO, GRPO, quantization, LoRA) so engineers have structured guidance regardless of method.

**What this prevents:** Ad-hoc architecture changes without review. Engineers choosing approaches based on familiarity rather than fit. Undocumented compression decisions that are hard to explain to clients.

### 3. Benchmarking and Comparison

**The SOP says:** Benchmark results must be stored, comparable across runs, and referenced by any improvement claim. No cherry-picked metrics. Client-specific workloads supplement but never replace the standard suite.

**The workflow enforces this by:**
- Defining a standard benchmark suite (MMLU, HumanEval, HellaSwag, etc.) as the default for every experiment. Engineers can add client-specific benchmarks on top but cannot skip the standard set.
- Storing all results in a consistent directory structure (`benchmarks/results/{run-label}/`) so any two runs can be compared directly.
- Flagging regressions automatically when comparing against a baseline, with configurable thresholds per metric.
- Requiring multiple runs for stochastic metrics (code generation benchmarks need at least 3 runs).

**What this prevents:** Results that exist only in a notebook or Slack message. Claims that reference a single cherry-picked benchmark. Inability to compare this week's experiment to last month's baseline.

### 4. Testing and Reproducibility

**The SOP says:** Every experiment must be reproducible by any team member on any compatible hardware. Dependencies are pinned. Configs are version-controlled. Seeds are set. Local-only scripts are promoted to shared pipelines.

**The workflow enforces this by:**
- Blocking experiment completion when reproducibility artifacts are missing: pinned dependencies, version-controlled configs, documented seeds, hardware specs.
- Scanning training scripts for local-only patterns (hardcoded paths, personal environment variables, untracked imports) and flagging them.
- Running baseline tests (model loading, inference sanity, regression checks) before an experiment is considered complete.
- Providing a promotion workflow that moves local experiment scripts into shared team pipelines with proper argument parsing, config loading, and tests.

**What this prevents:** "It works on my machine" experiments. Training configs that exist only in someone's command history. Scripts that break when another team member tries to run them. Silent regressions caught weeks later.

### 5. Documentation and Artifacts

**The SOP says:** Every experiment produces a written artifact. Documentation happens during the iteration, not after. Verbal-only findings are incomplete. Models are published with proper naming, model cards, and metadata.

**The workflow enforces this by:**
- Creating an experiment document skeleton at the start of every experiment, with sections for intent, hypothesis, method, results, interpretation, and next steps. The document exists from day one, not as an afterthought.
- Tracking documentation completeness and flagging sections that are still empty at close-out.
- Enforcing HuggingFace naming conventions (`Student-Teacher-TrainingType-DatasetType`) so published models are consistently identifiable.
- Generating model cards with proper YAML metadata (language, license, tags, base model, benchmark results) so models are published with full context.
- Defaulting all model visibility to private, requiring explicit review for public publication.

**What this prevents:** Experiments that conclude with "I'll write it up later" and never get documented. Models published without model cards. Inconsistent naming that makes the model registry hard to navigate. Accidental public publication of in-progress work.

## The Iteration Cycle

The workflow codifies our iteration cycle as five steps, each backed by a command:

```
Plan  -->  Experiment  -->  Benchmark  -->  Document  -->  Publish
  |                                                          |
  +------ next iteration informed by previous results -------+
```

| Step | Command | What happens |
|------|---------|-------------|
| Plan | `/PlanExperiment` | Define hypothesis, success criteria, select benchmark suite, create experiment document |
| Experiment | *(manual training)* | Run training with generated configs, track in W&B |
| Benchmark | `/RunBenchmarks` | Evaluate against success criteria, compare to baseline, flag regressions |
| Document | `/DocumentExperiment` | Generate experiment report and/or model card with full traceability |
| Publish | `/PublishModel` | Publish to HuggingFace with naming validation, model card, and branch strategy |

Each step produces artifacts that feed the next. Failed experiments inform the next iteration's hypothesis. The cycle is the same whether the experiment takes a day or a month.

## What This Does Not Do

This workflow is guidance and enforcement at the developer's workstation. It is not:

- **A training platform.** It does not run training jobs. It structures the work around them.
- **A CI/CD pipeline.** It defines what CI should check, but does not replace GitHub Actions or similar systems.
- **A model registry.** It guides publication to HuggingFace but does not replace HuggingFace as the registry.
- **An experiment tracker.** It integrates with W&B or MLflow but does not replace them.

It sits in the gap between "we have SOPs" and "engineers consistently follow them." The tools still matter. The workflow makes sure the process around them is followed.

## What Changes for the Team

| Before | After |
|--------|-------|
| SOPs exist in a document people reference occasionally | SOPs are embedded in the tools people use every day |
| Experiment documentation depends on individual discipline | The system creates document skeletons and tracks completeness |
| Benchmark results live in notebooks and Slack threads | Results are stored in a consistent, comparable format |
| Reproducibility is checked at review time, if at all | Reproducibility is validated before an experiment can close |
| Model naming and publishing is manual and inconsistent | Naming conventions and model cards are enforced at publish time |
| Success criteria are discussed verbally at kickoff | Success criteria are written, structured, and carried through to evaluation |

## Summary

The How We Work document describes the practices that make our ML R&D team effective. This workflow variant makes those practices the path of least resistance. Engineers do not need to remember every convention or checklist item — the workflow guides them through it. When something is missing, the system says so before the work is considered done.

The goal is not to add process. It is to make the process we already agreed on actually happen, consistently, every time.
