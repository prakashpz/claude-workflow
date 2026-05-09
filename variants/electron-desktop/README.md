# electron-desktop Variant

Electron desktop application development variant with React renderer, TypeScript, and electron-builder packaging.

## Project Type

Cross-platform desktop applications built with:
- **Electron** - Desktop runtime
- **React** - Renderer UI framework
- **TypeScript** - Type-safe development
- **electron-builder** - Packaging and distribution

## Components

### Agents

| Agent | Description |
|-------|-------------|
| `electron-specialist` | Senior Electron engineer covering main/renderer processes, security, builds, and performance |
| `ipc-architect` | IPC communication design, security patterns, and typed channel architecture |

### Commands

| Command | Description |
|---------|-------------|
| `/CreateComponent` | Scaffold a new React component with matching CSS in the renderer process |
| `/BuildInstaller` | Build platform-specific installer (DMG, EXE, AppImage) with validation |
| `/RunElectronTests` | Run test suites by scope (all, renderer, main, integration) |

### Tasks

| Task | Description |
|------|-------------|
| `electron-build` | Full build pipeline: pre-checks, compile, package, post-build verification |

## Expected Project Structure

```
src/
├── main/           # Electron main process
│   ├── index.ts    # App entry, window creation
│   ├── ipc-handlers.ts  # IPC channel handlers
│   └── preload.ts  # contextBridge API
├── renderer/       # React application
│   ├── components/ # React components (PascalCase.tsx + .css)
│   ├── store/      # Zustand state management
│   ├── contexts/   # React context providers
│   ├── hooks/      # Custom hooks
│   ├── themes/     # Theme definitions
│   ├── styles/     # Global styles
│   ├── types/      # TypeScript types
│   ├── utils/      # Utility functions
│   └── assets/     # Static assets
└── shared/         # Shared types between processes
```

## Requirements

- Node.js 18+
- `electron`, `react`, `react-dom`, `typescript`
- `electron-builder` for packaging

## Key Principles

- **Security first**: contextIsolation, no nodeIntegration, validated IPC
- **Native platform builds**: No cross-compilation
- **Process separation**: Clear main/renderer boundary via preload
- **Type safety**: Shared types for IPC channels

## Setup

```bash
/claude-workflow:setup
# Select "electron-desktop" variant
```
