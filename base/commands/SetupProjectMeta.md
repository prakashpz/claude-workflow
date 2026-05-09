---
name: SetupProjectMeta
description: Reconfigure project integration metadata for Linear or Jira (task management), Coda or Confluence (documentation), and GitHub
user_invocable: true
---

# /SetupProjectMeta

Reconfigure the project's integration metadata for Linear or Jira (task management), Coda or Confluence (documentation), and GitHub (source control). Use this command to change integrations after initial setup or to configure integrations that were skipped.

## Purpose

Project integrations are normally configured during `/SetupWorkflow`. Use this command when you need to:
- Change the Linear team or project
- Switch your task management tool from Linear to Jira (or vice versa)
- Switch to a different Coda document or page
- Switch your documentation tool from Coda to Confluence (or vice versa)
- Update the GitHub repository association
- Configure integrations that were skipped during initial setup

The workflow system uses this metadata to:
- Create and query issues in the correct Linear or Jira project
- Read and update product requirements in the correct Coda page or Confluence space
- Verify GitHub repository access

## Usage

```
/SetupProjectMeta [options]
```

## Arguments

- `--force`: Overwrite existing metadata configuration
- `--verify-only`: Only verify existing configuration without prompting for changes
- `--linear-only`: Only configure Linear integration
- `--jira-only`: Only configure Jira integration
- `--coda-only`: Only configure Coda integration
- `--confluence-only`: Only configure Confluence integration
- `--github-only`: Only configure GitHub integration

## Interactive Setup Process

When invoked, this command will:

### 1. Check Current Configuration

- Load `.claude/settings.json`
- Display current metadata status
- If already configured, ask: Update or Keep existing

### 2. Configure Task Management Integration

Ask the user which task management tool they use:
- **Linear** — set up Linear team and project
- **Jira** — set up Jira project via Atlassian MCP
- **Skip** — configure later

#### If Linear:

1. Verify Linear MCP connection
2. List available teams via `mcp__linear__list_teams`
3. Prompt user to select team
4. List projects in selected team via `mcp__linear__list_projects`
5. Prompt user to select or create project
6. If creating new project, prompt for project name and details
7. Store team and project IDs in settings under `linear`

#### If Jira:

1. Verify Atlassian MCP connection
2. List available projects via `mcp__atlassian__getVisibleJiraProjects`
3. Prompt user to select project
4. Ask for Jira base URL (e.g., `https://your-org.atlassian.net`)
5. Store project key, project name, and base URL in settings under `jira`

### 3. Configure Documentation Integration

Ask the user which documentation tool they use:
- **Coda** — set up Coda document and page
- **Confluence** — set up Confluence space and page via Atlassian MCP
- **Skip** — configure later

#### If Coda:

1. Verify Coda MCP connection
2. List available documents via `mcp__coda__coda_list_documents`
3. Prompt user to select document
4. List pages in selected document via `mcp__coda__coda_list_pages`
5. Prompt user to select or create project requirements page
6. If creating new page, use PRD template
7. Store document and page IDs in settings under `coda`

#### If Confluence:

1. Verify Atlassian MCP connection
2. List available spaces via `mcp__atlassian__getConfluenceSpaces`
3. Prompt user to select space
4. List pages in space via `mcp__atlassian__getPagesInConfluenceSpace`
5. Prompt user to select or identify requirements page
6. Ask for Confluence base URL (e.g., `https://your-org.atlassian.net/wiki`)
7. Store space key, page ID, page name, and base URL in settings under `confluence`

### 4. Configure GitHub Integration

1. Attempt auto-detection from git remote
2. If detected, confirm with user
3. If not detected or user wants different repo, prompt for repo URL
4. Verify access via `gh repo view`
5. Store repository details in settings

### 5. Finalize

- Save updated settings to `.claude/settings.json`
- Display summary of configured integrations
- Provide next steps guidance

## Prerequisites

- Linear MCP server configured and authenticated (if using Linear)
- Atlassian MCP server configured and authenticated (if using Jira or Confluence)
- Coda MCP server configured and authenticated (if using Coda)
- GitHub CLI (`gh`) authenticated
- `.claude/settings.json` exists (created by `/SetupWorkflow`)

## Output

Updates `.claude/settings.json` with the configured integrations:

```json
{
  "projectMetadata": {
    "linear": {
      "teamId": "team-uuid",
      "teamName": "Engineering",
      "projectId": "project-uuid",
      "projectName": "My Project"
    },
    "jira": {
      "baseUrl": "https://your-org.atlassian.net",
      "projectKey": "PROJ",
      "projectName": "My Project"
    },
    "coda": {
      "docId": "document-id",
      "docName": "Project Documentation",
      "pageId": "page-id",
      "pageName": "My Project Requirements"
    },
    "confluence": {
      "baseUrl": "https://your-org.atlassian.net/wiki",
      "spaceKey": "SPACE",
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

Only the keys for configured integrations are written; unconfigured integrations are omitted or left as empty objects.

## Examples

```bash
# Full interactive setup
/SetupProjectMeta

# Verify existing configuration
/SetupProjectMeta --verify-only

# Only set up Linear integration
/SetupProjectMeta --linear-only

# Only set up Jira integration
/SetupProjectMeta --jira-only

# Only set up Confluence integration
/SetupProjectMeta --confluence-only

# Force reconfigure all integrations
/SetupProjectMeta --force
```

## Execution Steps

1. Load current settings from `.claude/settings.json`
2. Check MCP connection status via `mcp-sync.verifyConnections`
3. For each integration (Linear or Jira, Coda or Confluence, GitHub):
   - Check if already configured
   - If not configured or `--force`, run interactive setup
   - Verify configuration is valid
4. Save updated settings
5. Display configuration summary

## Error Handling

| Error | Action |
|-------|--------|
| Settings file missing | Create default settings file first |
| Linear MCP not connected | Skip Linear setup, warn user |
| Atlassian MCP not connected | Skip Jira and Confluence setup, warn user |
| Coda MCP not connected | Skip Coda setup, warn user |
| GitHub CLI not authenticated | Skip GitHub setup, warn user |
| Team/project not found | Clear invalid config, re-prompt |
| Jira project key invalid | Re-prompt for correct project key |
| Confluence space key invalid | Re-prompt for correct space key |

## Related Commands

- `/StartSession` - Verifies metadata before starting a session
- `/CheckMCPStatus` - View connection status for all MCPs
- `/SyncLinear` - Manually sync with Linear (uses configured project)
- `/SyncJira` - Manually sync with Jira (uses configured project)
- `/SetupWorkflow` - Initial workflow system setup

## Tasks Invoked

- `project-metadata.setup`
- `project-metadata.verify`
- `mcp-sync.verifyConnections`

## Notes

- This command should be run once when setting up a new project
- Re-run with `--force` if you need to change project associations
- Task management (Linear or Jira) and documentation (Coda or Confluence) configurations are optional but recommended
- Jira and Confluence both use the Atlassian MCP — a single MCP connection covers both
- GitHub is auto-detected but can be overridden
