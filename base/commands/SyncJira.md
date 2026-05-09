---
description: Manually sync with Jira for issue management via the Atlassian MCP
---

# SyncJira

Manual synchronization with Jira for issue fetching, updates, and creation via the Atlassian MCP.

## Purpose

Provides direct access to Jira operations outside of session management, useful for quick updates or when not in an active session.

## Arguments

- `action`: Sync action (required)
  - `fetch` - Fetch open issues for the configured project
  - `update` - Update an issue status and/or add a comment
  - `create` - Create a new issue
  - `transition` - Transition an issue to a new status
- `projectKey`: Jira project key (for fetch/create; defaults to configured project)
- `issueId`: Issue key (for update/transition, e.g., PROJ-123)
- `status`: New status name (for update/transition)
- `comment`: Comment to add (for update/create)
- `title`: Issue summary (for create)
- `description`: Issue description (for create)
- `issueType`: Issue type (for create; default: "Story")

## Execution

1. Invoke `mcp-sync` task with appropriate action
   - For `fetch`: Call `mcp-sync.syncJira.fetchIssues`
   - For `update`: Call `mcp-sync.syncJira.updateIssue`
   - For `create`: Call `mcp-sync.syncJira.createIssue`
   - For `transition`: Call `mcp-sync.syncJira.transitionIssue`

2. Display:
   - Action result
   - Issue details
   - Confirmation

## Prerequisites

- Atlassian MCP configured and authenticated
- Jira integration configured in `.claude/settings.json` (via `/SetupProjectMeta --jira-only`)

## Examples

### Fetch Issues
```
/SyncJira action="fetch"
/SyncJira action="fetch" projectKey="PROJ"
```

### Update Issue
```
/SyncJira action="update" issueId="PROJ-211" status="In Review" comment="Ready for code review"
```

### Create Issue
```
/SyncJira action="create" projectKey="PROJ" title="Fix timeout bug" description="Handle timeout errors gracefully" issueType="Bug"
```

### Transition Issue
```
/SyncJira action="transition" issueId="PROJ-211" status="Done"
```

## Output Format

### Fetch
```
### Jira Issues (Project: PROJ)
| Key | Summary | Status | Priority |
|-----|---------|--------|----------|
| PROJ-211 | Feature implementation | In Progress | High |
| PROJ-212 | Bug fix | To Do | Medium |
```

### Update
```
### Issue Updated
- Key: PROJ-211
- New Status: In Review
- Comment Added: Yes
```

### Create
```
### Issue Created
- Key: PROJ-213
- URL: https://your-org.atlassian.net/browse/PROJ-213
```

## Related

- `/StartSession` - Full session with sync
- `/EndSession` - Session end with updates
- `/CheckMCPStatus` - Verify Atlassian MCP connection
- `/SyncLinear` - Sync with Linear instead

## Tasks Invoked

- `mcp-sync.syncJira.fetchIssues`
- `mcp-sync.syncJira.updateIssue`
- `mcp-sync.syncJira.createIssue`
- `mcp-sync.syncJira.transitionIssue`
