# /RunElectronTests

Run the test suite for the Electron application, including renderer tests and main process validation.

## Usage

```
/RunElectronTests [scope]
```

## Arguments

- `scope`: Optional. `all`, `renderer`, `main`, `integration`, or a specific test file path.

## Process

### Step 1: Detect Available Tests

Scan for test infrastructure:
- Check for test runner config (jest.config, vitest.config, etc.)
- Find test files in `tests/`, `src/**/*.test.*`, `src/**/*.spec.*`
- Check npm scripts for test commands
- Identify custom test runners (e.g., `test-runner.js`)

### Step 2: Run Tests by Scope

#### All Tests
Run all available test suites in order:
1. Unit tests (renderer components, utilities)
2. Main process tests (IPC handlers, file operations)
3. Integration tests (if available)
4. Custom validation tests (e.g., markdown rendering)

#### Renderer Tests
- Component tests
- Store tests
- Utility function tests
- Theme tests

#### Main Process Tests
- IPC handler tests
- File system operation tests
- Window management tests

#### Custom Tests
- Run project-specific test scripts (e.g., `npm run test:markdown`)
- Validate content rendering
- Check file format support

### Step 3: Report Results

Display:
- Pass/fail count per test suite
- Failed test details with file locations
- Test coverage summary (if available)
- Suggested fixes for common failures

## Available npm Scripts

Check and run these if they exist:
- `npm test` - Default test runner
- `npm run test:markdown` - Markdown validation tests
- `npm run test:unit` - Unit tests
- `npm run test:e2e` - End-to-end tests

## Notes

- Electron tests may require a display server on Linux CI (use xvfb)
- Main process tests should mock Electron APIs when running in Node
- Renderer tests should use testing-library for React components
