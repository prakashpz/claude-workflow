# Electron Build Task

## Task: electron-build

Manages the build pipeline for Electron desktop applications.

## Build Stages

### 1. Pre-Build Checks
- Verify Node.js version compatibility
- Check platform matches build target
- Validate package.json configuration
- Ensure all dependencies are installed
- Check for required build assets (icons, entitlements)

### 2. Compile
- TypeScript compilation for main process (`tsconfig.main.json`)
- Webpack/Vite bundle for renderer process
- Shared types compilation
- Source map generation (dev only, disabled in production)

### 3. Package
- electron-builder packaging
- Platform-specific installer creation
- Native module rebuilding for target platform
- Asset inclusion (icons, licenses, etc.)

### 4. Post-Build
- Verify output artifacts exist and have expected sizes
- Generate build report with version, platform, file sizes
- Clean temporary build artifacts

## Platform Matrix

| Platform | Installer | Tool | Script Extension |
|----------|-----------|------|-----------------|
| macOS    | .dmg      | electron-builder | .sh |
| Windows  | .exe (NSIS) | electron-builder | .ps1 |
| Linux    | .AppImage | electron-builder | .sh |

## Build Output Structure

```
release/
  ├── {AppName}-v{version}-{Platform}-{arch}.{ext}  # Installer
  ├── {platform}-unpacked/                            # Portable
  ├── latest-{platform}.yml                           # Auto-update metadata
  └── *.blockmap                                      # Delta update data
```

## Quality Gates

- [ ] TypeScript compiles without errors
- [ ] Webpack bundle succeeds
- [ ] Installer file is created
- [ ] Installer file size is within expected range
- [ ] No devDependencies included in production bundle
- [ ] Source maps disabled in production
- [ ] DevTools disabled in production

## Environment Variables

- `NODE_ENV`: Set to `production` for release builds
- `CSC_LINK`: Code signing certificate (macOS)
- `CSC_KEY_PASSWORD`: Certificate password (macOS)
- `WIN_CSC_LINK`: Code signing certificate (Windows)

## Common Failure Modes

| Error | Cause | Fix |
|-------|-------|-----|
| native module mismatch | Wrong Electron ABI | Run `electron-rebuild` |
| icon format error | Wrong icon format for platform | Use .icns (Mac), .ico (Win) |
| NSIS not found | First Windows build | electron-builder auto-downloads |
| code sign failure | Missing certificate | Set CSC_LINK env variable |
| cross-compile failure | Building for wrong OS | Build on native platform |
