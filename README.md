***

**CLIENT REPOSITORY NOTICE**

**Prepared for: AGData**

This repository is provided as a starter project for your team to own, manage,
and modify based on your training. Going forward, your team is fully responsible
for all maintenance, customization, and support of this codebase.

| | |
|---|---|
| **Version** | Workflow System v2.2.1 |
| **Support Contact** | Jared Munn (Jared.Munn@agdata.com) |
| **Original Creator** | Johann Beukes (johann@red-blue.ai) — Attribution only, not for support |
| **License** | Apache 2.0 — See LICENSE and NOTICE files |

**DISCLAIMER**: This software is provided "AS IS" without warranties of any kind,
express or implied. There are no guarantees of fitness for any particular purpose.
Your team is solely responsible for determining its appropriateness for your use.
See the LICENSE file for complete terms.

***

# Claude Workflow System

![Workflow System](https://img.shields.io/badge/Workflow_System-2.2.1-blue) ![Plugin](https://img.shields.io/badge/Plugin-1.1.0-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

A modular, extensible workflow system for Claude Code that provides structured development workflows, CI/CD integration, and project-type-specific variants.

## Overview

The Claude Workflow System gives you:

- **Structured Development Workflows**: Commands for session management, feature implementation, bug fixing, and code review
- **Intelligent Agents**: AI specialists for code writing, testing, documentation, and review
- **CI/CD Integration**: GitHub Actions for automated code and security reviews
- **Project Variants**: Specialized configurations for different project types (Next.js, Python, etc.)

### What's New in v2.2.1

- **Linear Issue Description Standard** — All issues created through the workflow system now follow a consistent format: `## Overview`, `## Deliverables`, `## Definition of Done`. Enforced in `/LogNewFeature`, `/Breakdown`, and `mcp-sync.createIssue`.
- **EndSession Linear Project Updates** — `/EndSession` now automatically posts a project update document to Linear when issues are completed during a session, and updates epic status when all sub-tasks are done.
- **Richer Issue Descriptions** — `/LogNewFeature` now generates full descriptions with acceptance criteria instead of optional single-line text.

---

## Installation Methods

Choose the method that works best for you:

| Method | Best For | Requirements |
|--------|----------|--------------|
| **Claude Code Plugin** | Most users - simple 3-step setup | Claude Code CLI, Git |
| **Python Scripts** | Automation, CI/CD pipelines | Python 3.8+, Git |

---

## Method 1: Claude Code Plugin (Recommended)

The plugin provides an interactive setup experience directly within Claude Code.

### Step 1: Add the Marketplace and Install the Plugin

In Claude Code, first add the RedBlue workflows marketplace:

```
/plugin marketplace add https://github.com/agdata-corp/claude-workflow-plugin.git
```

Then install the plugin:

```
/plugin install claude-workflow@agdata-corp-workflows
```

**Alternative: Test locally** (for plugin development):
```bash
git clone https://github.com/agdata-corp/claude-workflow-plugin.git
claude --plugin-dir /path/to/claude-workflow-plugin
```

### Step 2: Set Up a New Project

Navigate to your project directory (new or existing) and run:

```
/claude-workflow:setup
```

The plugin will:
1. Fetch the latest workflow system from GitHub
2. Detect if it's a new project or existing setup
3. Ask you to select a variant (base, nextjs-development, etc.)
4. Copy all necessary files to your project
5. Generate customized CLAUDE.md and configuration

### Step 3: Start Using Workflows

After setup, you have access to all workflow commands:

```
/StartSession          # Begin a development session
/ImplementFeature      # Start feature implementation
/FixBug               # Investigate and fix bugs
/ReviewCode           # Request code review
/EndSession           # End session, optionally trigger CI
```

### Plugin Commands Reference

| Command | Description |
|---------|-------------|
| `/claude-workflow:setup` | Set up workflow system in current directory |
| `/claude-workflow:update` | Update existing installation to latest version |
| `/claude-workflow:variants` | List available project variants |
| `/claude-workflow:status` | Check current installation status |

> **Note**: The plugin itself is NOT installed into your project. It's the "installer" that fetches and sets up the workflow components.

For detailed plugin documentation, see the [Plugin Repository](https://github.com/agdata-corp/claude-workflow-plugin).

---

## Method 2: Python Scripts

Use Python scripts for automated or scripted installations.

### Prerequisites

- Python 3.8 or later
- Git

### Initialize a New Project

```bash
# Clone this repository (one-time)
git clone https://github.com/agdata-corp/claude-workflow.git

# Initialize your project
python claude-workflow/scripts/init-project.py /path/to/your/project \
  --variant nextjs-development \
  --name "My Project" \
  --description "Project description"
```

### Update an Existing Project

```bash
python claude-workflow/scripts/sync-workflow.py /path/to/your/project \
  --variant nextjs-development
```

### List Available Variants

```bash
python claude-workflow/scripts/init-project.py --list-variants
```

### Script Options

**init-project.py**:
```
--variant, -v     Variant to use (e.g., nextjs-development)
--name, -n        Project name (defaults to directory name)
--description, -d Project description
--force, -f       Overwrite existing files
--list-variants   List available variants and exit
```

**sync-workflow.py**:
```
--variant, -v      Variant to sync
--components, -c   Components to sync (commands, agents, tasks, workflows)
--strategy, -s     Sync strategy (overlay, replace, merge)
--base-only        Only sync base layer
--variant-only     Only sync variant layer
--dry-run, -n      Preview changes without applying
```

---

## What Gets Installed

When you set up a project, the following structure is created:

```
your-project/
├── .claude/
│   ├── commands/           # 29 workflow commands
│   │   ├── StartSession.md
│   │   ├── EndSession.md
│   │   ├── ImplementFeature.md
│   │   └── ...
│   ├── agents/             # 10+ AI agents
│   │   ├── code-writer.md
│   │   ├── reviewer.md
│   │   └── ...
│   └── tasks/              # 20 orchestration tasks
│       ├── session-management.md
│       ├── ci-integration.md
│       └── ...
├── .github/
│   └── workflows/
│       ├── code-review.yml     # AI code review on PRs
│       └── security-review.yml # Security analysis on PRs
├── docs/
│   ├── planning/           # Session state and plans
│   └── specs/              # Technical specifications
├── knowledge/
│   ├── prd/                # Product requirements
│   └── architecture/       # Architecture documentation
└── CLAUDE.md               # Project guidance for Claude
```

---

## Available Variants

| Variant | Type | Description |
|---------|------|-------------|
| `base` | Generic | Core workflow system for any project |
| `nextjs-development` | Next.js | Full-stack Next.js with App Router, React, TypeScript |
| `electron-desktop` | Electron | Electron desktop app development with React renderer, TypeScript, and electron-builder |
| `ml-distillation` | Python | ML/AI R&D for model distillation, evaluation, benchmarking, and experiment workflows |

### Base Variant

Includes all core components - suitable for any project type:
- 29 commands for development workflows
- 10 agents for code, docs, testing, review, planning
- 20 tasks for orchestration
- GitHub Actions for CI/CD

### Next.js Variant

Extends base with Next.js specializations:
- **Additional Agents**: nextjs-specialist, react-component-writer, api-route-designer
- **Additional Commands**: /CreateComponent, /CreateAPIRoute
- **Additional Tasks**: nextjs-build
- **Templates**: Next.js-specific CLAUDE.md

### Electron Desktop Variant

Extends base with Electron specializations:
- **Additional Agents**: electron-specialist, ipc-architect
- **Additional Commands**: /CreateComponent, /BuildInstaller, /RunElectronTests
- **Additional Tasks**: electron-build
- **Templates**: Electron-specific CLAUDE.md

### ML Distillation Variant

Extends base with ML/AI R&D specializations:
- **Additional Agents**: distillation-architect, eval-benchmark-specialist, experiment-documentarian
- **Additional Commands**: /RunExperiment, /EvalModel, /PublishModel, /SyncExperiments
- **Additional Tasks**: experiment-tracking, model-evaluation
- **Templates**: ML-specific CLAUDE.md

### Create Your Own Variant

Don't see a variant for your project type? Create one during setup:

```bash
# During /SetupWorkflow, select "Create New Variant"
# Or run directly:
/CreateVariant swift-ios
```

After creating, submit to the community:
```bash
/SubmitVariant swift-ios
```

All contributions go through branches and pull requests - never direct push to main.

---

## Core Commands

| Command | Description |
|---------|-------------|
| `/StartSession` | Initialize development session with context loading |
| `/EndSession` | Close session, persist state, optionally trigger CI |
| `/SessionStatus` | View current session state and progress |
| `/SetupProjectMeta` | Reconfigure Linear, Coda, and GitHub integrations |
| `/CreateVariant` | Create a new variant for unsupported project types |
| `/SubmitVariant` | Submit variant to community via branch and PR |
| `/ImplementFeature` | Guided feature implementation workflow |
| `/FixBug` | Bug investigation and fix workflow |
| `/ReviewCode` | AI-powered code review |
| `/GenerateTests` | Generate test specifications |
| `/RefactorCode` | Code refactoring workflow |
| `/RunSecurityAudit` | Security-focused code analysis |
| `/UpdateDocs` | Documentation management |
| `/PRDIntake` | Import PRD from Coda, Confluence, or local file |
| `/PRDValidate` | Validate PRD completeness with scoring |
| `/PRDEnrich` | Add technical context to PRD |
| `/PRDFeasibility` | Assess feasibility with resource estimates |
| `/PRDSequence` | Sequence multiple initiatives |
| `/Breakdown` | Convert PRD to sized work items |
| `/CyclePlan` | Plan capacity-aware development cycle |
| `/CycleCommit` | Commit cycle plan to Linear |
| `/CycleStatus` | Get cycle progress and blockers |
| `/CycleSummary` | Generate end-of-cycle summary |
| `/CycleRetro` | Retrospective analysis |

---

## Core Agents

| Agent | Description |
|-------|-------------|
| `code-writer` | Full-stack engineer for production-ready code |
| `reviewer` | Code review specialist with security awareness |
| `test-planner` | Test specification and strategy expert |
| `doc-writer` | Technical documentation specialist |
| `schema-designer` | Database architecture expert |
| `researcher` | Standards and compliance researcher |
| `prd-validator` | PRD structure validation and completeness scoring |
| `technical-analyst` | Codebase analysis for PRD enrichment and feasibility |
| `cycle-planner` | Capacity planning and cycle management |
| `status-aggregator` | Status reporting and retrospective analysis |

---

## Post-Installation Setup

### 1. Configure CLAUDE.md

Review and customize the generated `CLAUDE.md` with:
- Your project description
- Repository structure
- Development guidelines
- Environment setup instructions

### 2. Project Integrations (Configured During Setup)

During setup, you'll be prompted to configure:
- **Linear**: Select team and project for issue tracking
- **Coda**: Choose document and page for product requirements
- **GitHub**: Verify repository access (auto-detected from git remote)

To reconfigure later, run `/SetupProjectMeta`.

### 3. Set Up GitHub Actions

Add your Anthropic API key to GitHub secrets:

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your Anthropic API key

### 4. Start Your First Session

```
/StartSession
```

The session will verify your project integrations are configured and ready.

---

## Repository Structure

```
claude-workflow/                     # This repository
├── base/                           # Core workflow system
│   ├── commands/                   # Base commands (29 files)
│   ├── agents/                     # Base agents (10 files)
│   ├── tasks/                      # Base tasks (20 files)
│   ├── github-workflows/           # CI/CD templates
│   ├── templates/                  # Project templates
│   ├── schema/                     # JSON schemas
│   └── VERSION                     # Base version
├── variants/                       # Project-type extensions
│   ├── nextjs-development/         # Next.js variant
│   ├── electron-desktop/           # Electron desktop variant
│   └── ml-distillation/            # ML/AI R&D variant
│       ├── manifest.json
│       ├── agents/
│       ├── commands/
│       ├── tasks/
│       └── templates/
├── scripts/                        # Python installation scripts
│   ├── init-project.py
│   ├── sync-workflow.py
│   ├── validate-variant.py
│   └── merge-layers.py
└── docs/                          # Repository documentation
    ├── getting-started.md
    ├── architecture.md
    └── creating-variants.md
```

**Plugin**: The Claude Code plugin lives in a separate repository: [claude-workflow-plugin](https://github.com/agdata-corp/claude-workflow-plugin)

**Installed in your project**: `base/` and selected `variants/` content

**NOT installed**: `scripts/`, `docs/` (these are tools, not project content)

---

## Documentation

- [Getting Started Guide](docs/getting-started.md) - Detailed setup walkthrough
- [Architecture](docs/architecture.md) - System design and concepts
- [Creating Variants](docs/creating-variants.md) - Build custom variants
- [Plugin Documentation](https://github.com/agdata-corp/claude-workflow-plugin) - Plugin installation and usage (separate repo)

---

## Requirements

| Component | Requirement |
|-----------|-------------|
| Claude Code | Required |
| Git | Required (for fetching from GitHub) |
| Python | 3.8+ (only for scripts method) |
| GitHub | For CI/CD workflows |
| Node.js | 18+ (for Next.js variant) |

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- [GitHub Issues](https://github.com/agdata-corp/claude-workflow/issues)
- [Documentation](docs/)
