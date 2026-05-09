---
name: agentuity-build
description: Build, typecheck, and deploy Agentuity projects with verification
---

# Agentuity Build Task

Build, verification, and deployment workflow for Agentuity projects.

## Operations

### `build`

Full build and verification.

**Steps:**
1. **Typecheck:**
   ```bash
   cd agents && bun run typecheck
   ```
   - Report any TypeScript errors
   - Check schema type inference is correct

2. **Build:**
   ```bash
   cd agents && bun run build
   ```
   - Produces `.agentuity/app.js` (server bundle)
   - Produces `.agentuity/client/` (Vite-built SPA)
   - Auto-generates `src/generated/registry.ts` and `src/generated/routes.ts`

3. **Verify:**
   - Check `.agentuity/app.js` exists
   - Check `.agentuity/client/` directory exists (if SPA present)
   - Check `src/generated/registry.ts` includes all agents
   - Check `src/generated/routes.ts` includes all routes

**Outputs:**
```json
{
  "status": "success|failed",
  "typecheck": { "errors": 0, "warnings": 0 },
  "build": {
    "serverBundle": ".agentuity/app.js",
    "clientBundle": ".agentuity/client/",
    "agents": ["Financial-Analyst"],
    "routes": ["chat", "upload", "analyze/variance", ...]
  }
}
```

### `dev`

Start development server.

**Steps:**
1. Ensure in `agents/` directory
2. Run `bun run dev` (starts on port 3500)
3. Report:
   - Server URL: `http://localhost:3500`
   - Workbench URL: `http://localhost:3500/workbench`
   - SPA URL: `http://localhost:3500/dashboard`
   - Health check: `http://localhost:3500/_agentuity/health`

### `deploy`

Deploy to Agentuity cloud.

**Steps:**
1. Run `build` operation first
2. If build succeeds:
   ```bash
   cd agents && bun run deploy
   ```
3. Report deployment URL and status

**Outputs:**
```json
{
  "status": "deployed",
  "url": "https://{project}.agentuity.cloud",
  "agents": [...],
  "routes": [...]
}
```

### `verify`

Verify project structure without building.

**Steps:**
1. Check `agentuity.json` exists and is valid
2. Check `app.ts` entry point exists
3. Scan `src/agent/*/` for agent files
4. Scan `src/api/` for route files
5. Check `src/web/` for SPA (if applicable)
6. Verify `package.json` dependencies
7. Report findings

**Outputs:**
```json
{
  "valid": true,
  "agents": [
    { "name": "Financial-Analyst", "path": "src/agent/Financial-Analyst/index.ts", "hasSchema": false }
  ],
  "routes": [
    { "path": "src/api/chat.ts", "methods": ["POST", "GET"] }
  ],
  "spa": { "exists": true, "entry": "src/web/index.html" },
  "issues": []
}
```

## Common Build Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Module not found `@agent/*` | Agent path alias not resolving | Check agent directory naming matches import |
| Type error in generated files | Stale generated code | Delete `src/generated/` and rebuild |
| Vite build error | `@/*` alias used in `src/web/` | Use relative imports only |
| Port 3500 in use | Previous dev server running | Kill process on port 3500 |
| Missing `AGENTUITY_SDK_KEY` | Not logged in to Agentuity | Run `agentuity auth login` |

## Dependencies

- **Bun**: Runtime and package manager
- **@agentuity/cli**: Build and dev tooling
- **TypeScript**: Type checking

## Directory Context

All build commands must run from the `agents/` directory, not the repository root. Root `package.json` scripts use `cd agents &&` prefix to handle this.
