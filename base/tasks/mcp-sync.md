---
name: mcp-sync
description: Centralized MCP interaction layer for task management and documentation synchronization
---

# MCP Sync Task

Unified interface for all MCP (Model Context Protocol) interactions. Centralizes task management and documentation operations to ensure consistent error handling, health tracking, and state management.

## Operations

### `verifyConnections`

Check health and authentication status of all MCPs.

**Steps:**
1. Test Linear MCP connection (if `projectMetadata.linear` is configured):
   - Attempt list operation
   - Verify authentication
   - Check capability schema
2. Test Atlassian MCP connection (if `projectMetadata.jira` or `projectMetadata.confluence` is configured):
   - Attempt `mcp__atlassian__atlassianUserInfo` to verify auth
   - A single Atlassian MCP covers both Jira and Confluence
3. Test Coda MCP connection (if `projectMetadata.coda` is configured):
   - Attempt list operation
   - Verify authentication
4. Test GitHub CLI (not MCP but required):
   - Run `gh auth status`
5. Return status object

**Outputs:**
```json
{
  "linear": {
    "healthy": true,
    "lastChecked": "2026-01-16T10:00:00Z",
    "error": null
  },
  "atlassian": {
    "healthy": true,
    "lastChecked": "2026-01-16T10:00:00Z",
    "coversJira": true,
    "coversConfluence": true,
    "error": null
  },
  "coda": {
    "healthy": false,
    "lastChecked": "2026-01-16T10:00:00Z",
    "error": "not configured"
  },
  "github": {
    "healthy": true,
    "authenticated": true,
    "error": null
  }
}
```

### `syncLinear`

Synchronize with task management for issue management.

**Sub-operations:**

#### `fetchIssues`
Fetch assigned issues.

**Inputs:**
- `team`: Team name or ID (optional)
- `assignee`: Filter by assignee (default: "me")
- `state`: Filter by state (default: open/active)
- `limit`: Max issues to return (default: 50)

**Steps:**
1. Call task management MCP with filters
2. Parse response into standardized format
3. Return issue list

**Outputs:**
```json
{
  "issues": [
    {
      "id": "PROJ-123",
      "title": "Issue title",
      "state": "In Progress",
      "priority": 2,
      "assignee": "User",
      "labels": ["feature"],
      "dueDate": "2026-01-20"
    }
  ],
  "syncedAt": "2026-01-16T10:00:00Z"
}
```

#### `updateIssue`
Update an issue.

**Inputs:**
- `id`: Issue ID
- `state`: New state (optional)
- `comment`: Comment to add (optional)
- `labels`: Labels to set (optional)

**Steps:**
1. Update issue if state/labels changed
2. Add comment if provided
3. Return confirmation

#### `createIssue`
Create a new issue. **Description MUST follow the Linear Issue Description Standard defined in CLAUDE.md** (Overview + Deliverables + Definition of Done sections).

**Inputs:**
- `title`: Issue title
- `description`: Issue description (**must include ## Overview, ## Deliverables, ## Definition of Done**)
- `team`: Team name or ID
- `assignee`: Assignee (optional)
- `labels`: Labels (optional)
- `priority`: Priority level (optional)
- `project`: Project name or ID (optional)
- `parentId`: Parent issue ID for sub-tasks (optional)
- `estimate`: Story point estimate (optional)

**Steps:**
1. Validate description contains required sections (Overview, Deliverables, Definition of Done)
2. Create issue via MCP with proper markdown formatting (real newlines, not escaped)
3. Return created issue details

#### `searchIssues`
Search issues by text query against titles and descriptions.

**Inputs:**
- `query`: Search text to match against issue titles and descriptions
- `team`: Team name or ID (optional, loaded from `project-metadata.getLinearContext` if not provided)
- `project`: Project name or ID (optional, loaded from `project-metadata.getLinearContext` if not provided)
- `limit`: Max issues to return (default: 10)
- `includeCompleted`: Include completed/done issues (default: false)

**Steps:**
1. Load project context from `project-metadata.getLinearContext` if team/project not provided
2. Call task management MCP to list issues within the team/project scope
3. Filter results by matching `query` text against issue titles and descriptions
4. Score results by relevance:
   - Title exact match: highest weight
   - Title partial/word match: high weight
   - Description match: moderate weight
5. Sort results by relevance score (descending)
6. Truncate to `limit` results
7. Return ranked issue list

**Outputs:**
```json
{
  "query": "dark mode",
  "totalMatches": 3,
  "issues": [
    {
      "id": "PROJ-456",
      "title": "Add dark mode support",
      "state": "Backlog",
      "priority": 2,
      "labels": ["feature"],
      "relevanceScore": 0.95,
      "matchedIn": ["title"]
    },
    {
      "id": "PROJ-389",
      "title": "CSS variable refactor",
      "state": "In Progress",
      "priority": 1,
      "labels": ["ui", "feature"],
      "relevanceScore": 0.62,
      "matchedIn": ["description"]
    }
  ],
  "searchedAt": "2026-01-27T10:00:00Z"
}
```

### `syncCoda`

Synchronize with documentation system.

**Sub-operations:**

#### `fetchPRD`
Fetch PRD content from documentation system.

**Inputs:**
- `docId`: Document ID
- `pageId`: Page ID or name

**Steps:**
1. Fetch page content via MCP
2. Parse markdown content
3. Return PRD object

**Outputs:**
```json
{
  "title": "PRD Title",
  "content": "Markdown content...",
  "lastUpdated": "2026-01-15",
  "source": "documentation"
}
```

#### `updatePage`
Update a documentation page.

**Inputs:**
- `docId`: Document ID
- `pageId`: Page ID or name
- `content`: New markdown content

**Steps:**
1. Update page via MCP
2. Return confirmation

#### `appendToPage`
Append content to a page.

**Inputs:**
- `docId`: Document ID
- `pageId`: Page ID or name
- `content`: Content to append

**Steps:**
1. Append content via MCP
2. Return confirmation

### `syncJira`

Synchronize with Jira for issue management via the Atlassian MCP.

**Sub-operations:**

#### `fetchIssues`
Fetch issues from the configured Jira project.

**Inputs:**
- `projectKey`: Jira project key (optional, loaded from `project-metadata.getJiraContext`)
- `assignee`: Filter by assignee (default: "currentUser()")
- `status`: Filter by status (default: open/active)
- `limit`: Max issues to return (default: 50)

**Steps:**
1. Load project context from `project-metadata.getJiraContext` if projectKey not provided
2. Call `mcp__atlassian__searchJiraIssuesUsingJql` with JQL: `project = {projectKey} AND assignee = {assignee} AND status != Done ORDER BY priority ASC`
3. Parse response into standardized format
4. Return issue list

**Outputs:**
```json
{
  "issues": [
    {
      "id": "PROJ-123",
      "title": "Issue title",
      "status": "In Progress",
      "priority": "High",
      "assignee": "User",
      "labels": ["feature"],
      "url": "https://your-org.atlassian.net/browse/PROJ-123"
    }
  ],
  "syncedAt": "2026-01-16T10:00:00Z"
}
```

#### `updateIssue`
Update a Jira issue status and/or add a comment.

**Inputs:**
- `id`: Issue key (e.g., PROJ-123)
- `status`: New status to transition to (optional)
- `comment`: Comment to add (optional)
- `labels`: Labels to set (optional)

**Steps:**
1. If `status` provided: fetch available transitions via `mcp__atlassian__getTransitionsForJiraIssue`, then call `mcp__atlassian__transitionJiraIssue`
2. If `comment` provided: call `mcp__atlassian__addCommentToJiraIssue`
3. If `labels` provided: call `mcp__atlassian__editJiraIssue` with updated labels
4. Return confirmation

#### `createIssue`
Create a new Jira issue.

**Inputs:**
- `title`: Issue summary
- `description`: Issue description (ADF or plain text)
- `projectKey`: Jira project key
- `issueType`: Issue type (default: "Story")
- `assignee`: Assignee account ID (optional)
- `labels`: Labels (optional)
- `priority`: Priority name (optional)
- `parentId`: Parent issue key for sub-tasks (optional)

**Steps:**
1. Fetch issue type metadata via `mcp__atlassian__getJiraIssueTypeMetaWithFields`
2. Create issue via `mcp__atlassian__createJiraIssue`
3. Return created issue key and URL

**Outputs:**
```json
{
  "id": "PROJ-124",
  "url": "https://your-org.atlassian.net/browse/PROJ-124"
}
```

#### `searchIssues`
Search Jira issues by text query using JQL.

**Inputs:**
- `query`: Search text
- `projectKey`: Jira project key (optional, loaded from context)
- `limit`: Max issues to return (default: 10)
- `includeResolved`: Include resolved issues (default: false)

**Steps:**
1. Load project context if projectKey not provided
2. Build JQL: `project = {projectKey} AND text ~ "{query}"` (append `AND resolution = Unresolved` unless `includeResolved`)
3. Call `mcp__atlassian__searchJiraIssuesUsingJql`
4. Return ranked issue list

#### `transitionIssue`
Transition a Jira issue to a new status.

**Inputs:**
- `id`: Issue key
- `status`: Target status name (e.g., "In Progress", "Done", "In Review")

**Steps:**
1. Fetch available transitions via `mcp__atlassian__getTransitionsForJiraIssue`
2. Match target status name to a transition ID
3. Execute transition via `mcp__atlassian__transitionJiraIssue`
4. Return confirmation

### `syncConfluence`

Synchronize with Confluence for documentation via the Atlassian MCP.

**Sub-operations:**

#### `fetchPage`
Fetch content from a Confluence page.

**Inputs:**
- `pageId`: Confluence page ID (optional, loaded from `project-metadata.getConfluenceContext`)
- `spaceKey`: Space key (optional)

**Steps:**
1. Load context from `project-metadata.getConfluenceContext` if pageId not provided
2. Call `mcp__atlassian__getConfluencePage` with pageId
3. Parse and return page content as markdown

**Outputs:**
```json
{
  "title": "Page Title",
  "content": "Markdown content...",
  "lastUpdated": "2026-01-15",
  "url": "https://your-org.atlassian.net/wiki/spaces/SPACE/pages/12345",
  "source": "confluence"
}
```

#### `updatePage`
Update a Confluence page with new content.

**Inputs:**
- `pageId`: Confluence page ID
- `title`: Page title
- `content`: New page content (markdown or storage format)
- `version`: Current page version (required for updates)

**Steps:**
1. Fetch current page version via `mcp__atlassian__getConfluencePage` if version not provided
2. Call `mcp__atlassian__updateConfluencePage` with incremented version
3. Return confirmation and updated page URL

#### `appendToPage`
Append content to an existing Confluence page.

**Inputs:**
- `pageId`: Confluence page ID
- `content`: Content to append (markdown)

**Steps:**
1. Fetch current page content and version via `mcp__atlassian__getConfluencePage`
2. Append new content to existing body
3. Call `mcp__atlassian__updateConfluencePage` with combined content
4. Return confirmation

#### `searchPages`
Search Confluence pages using CQL.

**Inputs:**
- `query`: Search text
- `spaceKey`: Space key to scope search (optional, loaded from context)
- `limit`: Max results (default: 10)

**Steps:**
1. Load context if spaceKey not provided
2. Call `mcp__atlassian__searchConfluenceUsingCql` with CQL: `space = "{spaceKey}" AND text ~ "{query}"`
3. Return list of matching pages with titles and URLs

### `createInitiative`

Create an Initiative in Linear from PRD data.

**Inputs:**
- `title`: Initiative title
- `description`: Initiative description (from PRD)
- `targetDate`: Target completion date (optional)

**Steps:**
1. Create Initiative via Linear MCP
2. Return Initiative ID and URL

**Outputs:**
```json
{ "initiativeId": "init-123", "url": "https://linear.app/..." }
```

### `createWorkItems`

Batch create Work Items from breakdown.

**Inputs:**
- `items`: Array of work item specs (title, description, team, labels, priority, estimate)
- `projectId`: Linear project ID

**Steps:**
1. Iterate over items
2. Create each issue via Linear MCP
3. Set dependency relationships between items
4. Return created issue IDs

**Outputs:**
```json
{ "created": [{ "id": "PROJ-101", "title": "..." }], "count": 12 }
```

### `createCycle`

Create a Cycle in Linear.

**Inputs:**
- `teamId`: Team ID
- `name`: Cycle name
- `startDate`: Start date
- `endDate`: End date

**Steps:**
1. Create Cycle via Linear MCP
2. Return Cycle ID

**Outputs:**
```json
{ "cycleId": "cycle-123", "url": "https://linear.app/..." }
```

### `assignToCycle`

Assign Work Items to a Cycle.

**Inputs:**
- `cycleId`: Cycle ID
- `issueIds`: Array of issue IDs to assign

**Steps:**
1. Update each issue to assign to cycle
2. Return confirmation

**Outputs:**
```json
{ "assigned": 12, "cycleId": "cycle-123" }
```

### `getCycleProgress`

Fetch Cycle status from Linear.

**Inputs:**
- `cycleId`: Cycle ID (optional, defaults to current cycle)
- `teamId`: Team ID

**Steps:**
1. Fetch cycle details from Linear MCP
2. Fetch all issues in cycle
3. Calculate progress metrics
4. Return progress object

**Outputs:**
```json
{ "cycleId": "cycle-123", "total": 12, "completed": 5, "inProgress": 4, "blocked": 1, "remaining": 2 }
```

### `getBacklog`

Fetch prioritized backlog for planning.

**Inputs:**
- `teamId`: Team ID (optional)
- `projectId`: Project ID (optional)
- `state`: Filter by state (default: "backlog")
- `limit`: Max items (default: 100)

**Steps:**
1. Fetch backlog issues from Linear MCP sorted by priority
2. Return prioritized list

**Outputs:**
```json
{ "items": [{ "id": "PROJ-50", "title": "...", "priority": 1, "estimate": 8 }], "total": 45 }
```

## Configuration

The task works with any configured MCP servers for:
- Task management: Linear MCP (`syncLinear`) or Atlassian MCP (`syncJira`)
- Documentation: Coda MCP (`syncCoda`) or Atlassian MCP (`syncConfluence`)

**Project Scoping:** When `project-metadata` is configured, operations are automatically scoped:
- Linear operations use the configured team and project (`project-metadata.getLinearContext`)
- Jira operations use the configured project key and base URL (`project-metadata.getJiraContext`)
- Coda operations use the configured document and page (`project-metadata.getCodaContext`)
- Confluence operations use the configured space key and page ID (`project-metadata.getConfluenceContext`)

**Atlassian MCP Note:** Jira and Confluence both use the same Atlassian MCP connection. A single authentication covers both services.

## Error Handling

| Error Type | Action |
|------------|--------|
| Authentication failure | Return `healthy: false` with error details |
| Rate limit | Retry with exponential backoff (max 3 attempts) |
| Network error | Mark unhealthy, allow offline mode |
| Invalid response | Log error, return partial data if possible |

## Health Tracking

Health status is stored in `session-state.json`:
```json
{
  "mcpState": {
    "linearLastSync": "2026-01-16T10:05:00Z",
    "linearHealthy": true,
    "jiraLastSync": "2026-01-16T10:05:00Z",
    "jiraHealthy": true,
    "codaLastSync": "2026-01-16T10:05:00Z",
    "codaHealthy": false,
    "confluenceLastSync": "2026-01-16T10:05:00Z",
    "confluenceHealthy": true
  }
}
```

Note: `jiraHealthy` and `confluenceHealthy` both reflect the Atlassian MCP connection status since they share the same MCP.

## Dependencies

- **project-metadata** (optional): For getting configured team/project/document context

## Usage Examples

```
// Verify all connections
invoke mcp-sync.verifyConnections

// --- Linear ---
// Fetch my open issues
invoke mcp-sync.syncLinear.fetchIssues(assignee="me", state="open")

// Update issue status
invoke mcp-sync.syncLinear.updateIssue(id="PROJ-123", state="Done", comment="Completed in session")

// Search for issues by keyword
invoke mcp-sync.syncLinear.searchIssues(query="dark mode", limit=10)

// --- Jira ---
// Fetch my open Jira issues
invoke mcp-sync.syncJira.fetchIssues(assignee="currentUser()")

// Update Jira issue status
invoke mcp-sync.syncJira.updateIssue(id="PROJ-123", status="In Review", comment="Ready for review")

// Create a Jira issue
invoke mcp-sync.syncJira.createIssue(title="Fix timeout bug", projectKey="PROJ", issueType="Bug")

// Search Jira issues
invoke mcp-sync.syncJira.searchIssues(query="dark mode", limit=10)

// Transition a Jira issue
invoke mcp-sync.syncJira.transitionIssue(id="PROJ-123", status="Done")

// --- Coda ---
// Fetch PRD from Coda
invoke mcp-sync.syncCoda.fetchPRD(docId="doc123", pageId="PRD Page")

// --- Confluence ---
// Fetch requirements page from Confluence
invoke mcp-sync.syncConfluence.fetchPage(pageId="12345678")

// Append session notes to a Confluence page
invoke mcp-sync.syncConfluence.appendToPage(pageId="12345678", content="## Session Notes\n...")

// Search Confluence pages
invoke mcp-sync.syncConfluence.searchPages(query="authentication design", spaceKey="ENG")
```
