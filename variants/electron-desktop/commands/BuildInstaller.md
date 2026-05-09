# /BuildInstaller

Build a platform-specific installer for the Electron application.

## Usage

```
/BuildInstaller [platform]
```

## Arguments

- `platform`: Optional. `mac`, `win`, or `linux`. Defaults to current platform.

## Process

### Step 1: Detect Environment

1. Determine current OS platform
2. Verify the target platform matches the current OS (no cross-compilation)
3. Check Node.js version (18+ required)
4. Verify npm dependencies are installed

### Step 2: Pre-Build Validation

1. Check for uncommitted changes (warn if present)
2. Verify `package.json` version is correct
3. Check that required build assets exist (icons, etc.)
4. Validate electron-builder configuration in `package.json`

### Step 3: Build Process

1. Clean previous build artifacts (`dist/`, `release/`)
2. Run `npm run build` to compile TypeScript and bundle renderer
3. Run `npm run dist:{platform}` to create installer
4. Verify output files exist in `release/`

### Step 4: Report Results

Display:
- Build output location and file sizes
- Installer filename and type (.dmg, .exe, .AppImage)
- Version number included in build
- Any warnings encountered

## Platform Rules

- **macOS builds**: Must run on macOS. Creates .dmg installer.
- **Windows builds**: Must run on Windows (native PowerShell, not WSL). Creates NSIS .exe installer.
- **Linux builds**: Must run on Linux. Creates .AppImage.

If the user requests a cross-platform build, explain why it's not supported and suggest building on the target platform.

## Build Scripts

If build scripts exist in `/builds/`, prefer using them over raw npm commands, as they include version management and validation.

## Troubleshooting

Common issues to check:
- Icon format errors (use proper .icns for Mac, .ico for Windows)
- Native module compilation failures (rebuild with `electron-rebuild`)
- Code signing configuration (required for macOS distribution)
- NSIS not found (auto-installed by electron-builder on Windows)
