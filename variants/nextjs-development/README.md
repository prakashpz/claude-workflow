# Next.js Development Variant

A specialized variant of the Claude Workflow System for full-stack Next.js development with React, TypeScript, and modern tooling.

## Overview

This variant extends the base Claude Workflow System with Next.js-specific agents, commands, and configurations optimized for App Router development.

## Features

- **Next.js Specialist Agent**: Expert guidance on App Router patterns, server components, and data fetching strategies
- **React Component Writer**: Generate accessible, well-typed React components with tests
- **API Route Designer**: Create robust API endpoints with validation and error handling
- **Next.js-specific Commands**: `/CreateComponent`, `/CreateAPIRoute` for rapid development
- **Build Task Integration**: TypeScript, ESLint, and bundle analysis

## Installation

### For New Projects

```bash
# From the workflow repository
python scripts/init-project.py /path/to/your/nextjs-project --variant nextjs-development
```

### For Existing Projects

```bash
# Sync workflow system to existing project
python scripts/sync-workflow.py /path/to/your/nextjs-project --variant nextjs-development
```

## Included Components

### Agents

| Agent | Description |
|-------|-------------|
| `nextjs-specialist` | Expert in App Router, server components, and Next.js patterns |
| `react-component-writer` | Creates accessible React components with proper TypeScript |
| `api-route-designer` | Designs RESTful API routes with validation |

### Commands

| Command | Description |
|---------|-------------|
| `/CreateComponent` | Create a new React component with tests and optional Storybook story |
| `/CreateAPIRoute` | Create a new API route with validation and error handling |

### Tasks

| Task | Description |
|------|-------------|
| `nextjs-build` | Handle type checking, linting, and production builds |

## Project Structure

This variant expects and creates the following structure:

```
your-project/
├── .claude/
│   ├── commands/         # All workflow commands
│   ├── agents/           # All workflow agents
│   └── tasks/            # All workflow tasks
├── .github/
│   └── workflows/        # CI/CD workflows
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── api/          # API routes
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── ui/           # Base components
│   │   ├── features/     # Feature components
│   │   └── layouts/      # Layout components
│   ├── lib/              # Utilities
│   ├── hooks/            # Custom hooks
│   └── types/            # TypeScript types
├── docs/
│   ├── planning/         # Session management
│   └── specs/            # Technical specs
├── knowledge/
│   ├── prd/              # Requirements
│   └── architecture/     # Architecture docs
├── CLAUDE.md             # Project guidance
└── package.json
```

## Configuration

The manifest configures:

```json
{
  "projectStructure": {
    "components": "src/components",
    "pages": "src/app",
    "api": "src/app/api",
    "lib": "src/lib",
    "hooks": "src/hooks",
    "types": "src/types"
  },
  "requiredDependencies": [
    "next",
    "react",
    "react-dom",
    "typescript"
  ]
}
```

## Usage Examples

### Creating Components

```bash
# Create a UI button component
/CreateComponent Button --type ui --props "variant:string,size:string"

# Create a feature component with tests and story
/CreateComponent UserProfile --type feature --with-story --client
```

### Creating API Routes

```bash
# Create a CRUD API for items
/CreateAPIRoute items --methods GET,POST --with-id --prisma --auth

# Create a simple endpoint
/CreateAPIRoute health --methods GET
```

### Development Workflow

```bash
# Start a session
/StartSession

# Work on a feature
/ImplementFeature "Add user authentication"

# Create necessary components
/CreateComponent LoginForm --type feature --client

# Create API routes
/CreateAPIRoute auth --methods POST --with-id

# Review code before commit
/ReviewCode

# End session
/EndSession --trigger-ci
```

## Compatibility

- **Base Version**: 2.0.0+
- **Next.js**: 14+ (App Router)
- **React**: 18+
- **TypeScript**: 5+
- **Node.js**: 18+

## Customization

To customize this variant for your project:

1. Fork or copy the variant directory
2. Modify `manifest.json` to adjust paths or add components
3. Edit agent files to match your team's patterns
4. Add custom commands as needed

## Contributing

See the main Claude Workflow System repository for contribution guidelines.
