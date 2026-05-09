# Getting Started

This guide walks you through setting up the Claude Workflow System for your project.

## Prerequisites

- Python 3.8 or later
- Claude Code CLI installed and configured
- Git
- GitHub account (for CI features)

## Installation Options

### Option 1: Initialize a New Project

Best for starting fresh or adding workflows to a clean project:

```bash
# Clone the workflow repository
git clone https://github.com/agdata-corp/claude-workflow.git

# Initialize your project
python claude-workflow/scripts/init-project.py /path/to/your/project \
  --variant nextjs-development \
  --name "My Project" \
  --description "Description of my project"
```

**Don't see a variant for your project type?** During setup, select "Create New Variant" or run `/CreateVariant` to build one for your technology stack.

### Option 2: Add to Existing Project

Best for adding workflows to an established codebase:

```bash
# Clone the workflow repository
git clone https://github.com/agdata-corp/claude-workflow.git

# Sync workflows to your project
python claude-workflow/scripts/sync-workflow.py /path/to/your/project \
  --variant nextjs-development
```

## Post-Installation Setup

### 1. Configure CLAUDE.md

Open `CLAUDE.md` in your project and customize:

- Project description and overview
- Repository structure documentation
- Development guidelines specific to your project
- Environment setup instructions

### 2. Project Integrations (Configured During Setup)

During `/SetupWorkflow` or `/claude-workflow:setup`, you'll be prompted to configure:

1. **Linear Integration**: Select your team and project for issue tracking
2. **Coda Integration**: Choose a document and page for product requirements
3. **GitHub Integration**: Verify repository access (auto-detected from git remote)

The configuration is stored in `.claude/settings.json` under `projectMetadata`:

```json
{
  "projectMetadata": {
    "linear": {
      "teamId": "team-uuid",
      "teamName": "Engineering",
      "projectId": "project-uuid",
      "projectName": "My Project"
    },
    "coda": {
      "docId": "document-id",
      "docName": "Project Documentation",
      "pageId": "page-id",
      "pageName": "My Project Requirements"
    },
    "github": {
      "repo": "org/repo-name",
      "owner": "org",
      "name": "repo-name"
    }
  }
}
```

To reconfigure integrations later, run `/SetupProjectMeta`.

### 3. Set Up GitHub Actions

Add your Anthropic API key to GitHub secrets:

1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your Anthropic API key

### 4. Configure Task Management (Optional)

For additional task management options, edit `.claude/settings.json`:

```json
{
  "workflow": {
    "taskManagement": {
      "provider": "linear",
      "projectKey": "YOUR-PROJECT",
      "autoSync": true
    }
  }
}
```

## Your First Session

Start a development session:

```bash
# In your project directory with Claude Code
/StartSession
```

This will:
1. Load project context from CLAUDE.md
2. Check for existing session state
3. Sync with task management (if configured)
4. Report current status

### Session Commands

```bash
# Check session status
/SessionStatus

# Work on a feature
/ImplementFeature "Add user authentication"

# Fix a bug
/FixBug "Login fails on mobile devices"

# Request code review
/ReviewCode

# End session
/EndSession
```

## Directory Structure

After setup, your project will have:

```
your-project/
├── .claude/
│   ├── commands/           # 29 workflow commands
│   ├── agents/             # 10+ AI agents
│   ├── tasks/              # 20 orchestration tasks
│   └── settings.json       # Configuration
├── .github/
│   └── workflows/
│       ├── code-review.yml
│       └── security-review.yml
├── docs/
│   ├── planning/
│   │   ├── CURRENT-STATE.md
│   │   └── session-state.json
│   ├── specs/
│   └── reports/
├── knowledge/
│   ├── prd/
│   └── architecture/
└── CLAUDE.md
```

## Common Workflows

### Feature Development

```bash
# Start session
/StartSession

# Begin feature work
/ImplementFeature "Add search functionality"

# Claude will:
# 1. Discover requirements
# 2. Create implementation plan
# 3. Generate code with code-writer agent
# 4. Run quality checks
# 5. Update documentation

# Review changes
/ReviewCode

# End session
/EndSession --trigger-ci
```

### Bug Fixing

```bash
# Start session
/StartSession

# Investigate and fix bug
/FixBug "Search results not sorted correctly"

# Claude will:
# 1. Analyze bug description
# 2. Locate relevant code
# 3. Investigate root cause
# 4. Implement fix
# 5. Generate tests

# End session
/EndSession
```

### Code Review

```bash
# Review specific files
/ReviewCode --files "src/components/Search.tsx"

# Review all changes
/ReviewCode

# Review with security focus
/RunSecurityAudit
```

### Planning Workflow (v2.0)

```bash
# Import a PRD from Coda
/PRDIntake url="https://coda.io/d/..."

# Validate and enrich the PRD
/PRDValidate prd="feature-name"
/PRDEnrich prd="feature-name"

# Assess feasibility
/PRDFeasibility prd="feature-name"

# Break down into work items
/Breakdown prd="feature-name"

# Plan and commit a cycle
/CyclePlan duration="2w" team="Engineering"
/CycleCommit cycle="cycle-2026-02-04"

# Track progress
/CycleStatus
/CycleSummary
/CycleRetro
```

## Updating the Workflow System

To update to the latest version:

```bash
# Pull latest changes
cd claude-workflow
git pull

# Sync updates to your project
python scripts/sync-workflow.py /path/to/your/project
```

## Troubleshooting

### Session State Issues

If session state becomes corrupted:

```bash
# Check current state
/SessionStatus

# Reset session (end without saving)
/EndSession --discard
```

### MCP Connection Problems

Check MCP status:

```bash
/CheckMCPStatus
```

### CI Workflow Not Running

1. Verify `ANTHROPIC_API_KEY` is set in GitHub secrets
2. Check workflow permissions in repository settings
3. Review workflow file in `.github/workflows/`

## Contributing Variants

Created a variant for your project type? Share it with the community:

```bash
# Submit your variant via pull request
/SubmitVariant your-variant-name
```

This creates a branch and PR - all contributions go through review before merging to main.

See [Creating Variants](creating-variants.md) for the full guide.

## Next Steps

- Read the [Architecture Guide](architecture.md) to understand the system design
- Learn about [Creating Variants](creating-variants.md) for custom project types
- Explore the [Command Reference](command-reference.md) for all available commands
- Check the [Agent Reference](agent-reference.md) for agent capabilities
