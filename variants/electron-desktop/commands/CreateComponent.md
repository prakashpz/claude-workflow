# /CreateComponent

Create a new React component for the Electron renderer process with matching CSS file.

## Usage

```
/CreateComponent <ComponentName>
```

## Process

### Step 1: Gather Component Information

Use AskUserQuestion to ask:
- **Component name**: PascalCase name (e.g., `StatusBar`, `SearchPanel`)
- **Component type**: UI component, container, modal, panel, or sidebar widget
- **Props**: Key props the component needs
- **State**: Whether it needs local state or connects to a Zustand store

### Step 2: Check Existing Components

Before creating, check `src/renderer/components/` for:
- Existing components with similar names or functionality
- Related components that this one should integrate with
- Shared patterns (CSS conventions, import style, prop patterns)

### Step 3: Create Component Files

Create two files in `src/renderer/components/`:

#### `{ComponentName}.tsx`
- Functional React component with TypeScript
- Props interface exported
- Follow existing component patterns in the project
- Include appropriate imports (React, CSS, store hooks)
- Use CSS class names matching existing conventions

#### `{ComponentName}.css`
- Matching CSS file with component-scoped classes
- Follow existing theme variable usage (CSS custom properties)
- Support dark/light theme variants
- Responsive sizing where appropriate

### Step 4: Integration Guidance

After creating files, provide:
- Where to import and render the new component
- Any store updates needed
- Any IPC channels to add (if component needs main process data)

## Example Output

```
Created component: StatusBar

Files created:
  src/renderer/components/StatusBar.tsx
  src/renderer/components/StatusBar.css

Integration:
  Import in App.tsx and add below the main content area.
  No store changes needed - uses props from parent.
```
