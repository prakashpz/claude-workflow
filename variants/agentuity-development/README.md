# Agentuity Development Variant

A Claude Workflow System variant for building AI agent applications on the [Agentuity platform](https://agentuity.dev/).

## Overview

This variant provides specialized agents, commands, and tasks for developing Agentuity-based projects with:
- **AI Agents** using `@agentuity/runtime` (`createAgent`, schemas, storage APIs, AI Gateway)
- **Hono API Routes** using `createRouter` (middleware, cron, validators)
- **React SPA Frontend** (React 19, React Router v7, Tailwind CSS, Radix UI)

## Design Philosophy

The variant enforces **separation of concerns** across three layers:

| Layer | Agent | Platform-Specific? | Replaceable? |
|-------|-------|---------------------|--------------|
| Agents | `agentuity-agent-architect` | Yes (Agentuity SDK) | No |
| API Routes | `agentuity-route-designer` | Yes (Hono via Agentuity) | Partially |
| Frontend | `react-spa-writer` | No (generic React) | Yes |

The frontend layer is intentionally generic React -- if you swap to Vue, Svelte, or a separate Next.js app, only `react-spa-writer` needs to change. Agent and route logic remain untouched.

## Components

### Specialized Agents (replace base `code-writer`)

| Agent | Purpose |
|-------|---------|
| `agentuity-agent-architect` | Creates Agentuity agents with `createAgent()`, schemas, storage APIs, AI Gateway, agent-to-agent communication, evaluations |
| `agentuity-route-designer` | Designs Hono-based API routes with `createRouter()`, middleware, cron jobs, validators, `c.var.*` storage access |
| `react-spa-writer` | Builds React 19 SPA with React Router v7, Tailwind CSS, Radix UI components, client-side API integration |

### Variant Commands (replace base versions)

| Command | Purpose |
|---------|---------|
| `/ImplementFeature` | Agentuity-aware feature implementation with agent/route/UI routing |
| `/FixBug` | Bug diagnosis with Agentuity-specific pitfall checklist |
| `/RefactorCode` | Refactoring with layer separation awareness |

### New Commands

| Command | Purpose |
|---------|---------|
| `/CreateAgent` | Scaffold a new Agentuity agent with handler, schema, evaluations |
| `/CreateRoute` | Scaffold a new Hono API route with agent integration |

### Variant Tasks (replace base versions)

| Task | Purpose |
|------|---------|
| `feature-workflow` | Feature orchestration routing to layer-specific agents |
| `bug-workflow` | Bug investigation with Agentuity-specific issue classification |

### New Tasks

| Task | Purpose |
|------|---------|
| `agentuity-build` | Build, typecheck, deploy, and verify Agentuity projects |

## Agentuity Project Structure

```
project/
├── app.ts                    # createApp() entry point
├── agentuity.json            # Platform config
├── src/
│   ├── agent/                # AI agents (auto-discovered)
│   │   └── {Name}/
│   │       ├── index.ts      # createAgent() with handler
│   │       └── eval.ts       # Agent evaluations
│   ├── api/                  # Hono routes (auto-discovered)
│   │   ├── _shared/          # Shared utilities
│   │   └── {route}.ts        # createRouter() exports
│   ├── web/                  # React SPA (Vite-built)
│   │   ├── components/
│   │   ├── routes/
│   │   └── lib/
│   └── generated/            # Auto-generated (do not edit)
└── data/                     # Data files
```

## Requirements

- Bun runtime
- `@agentuity/runtime` and `@agentuity/workbench`
- Vercel AI SDK v6 (`ai`, `@ai-sdk/openai`)
- TypeScript 5+

## Getting Started

```bash
# Setup with this variant
/claude-workflow:setup
# Select "agentuity-development" when prompted

# Or during project creation
agentuity init
/claude-workflow:setup
```
