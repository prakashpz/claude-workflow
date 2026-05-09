---
name: CreateRoute
description: Create a new Hono API route with validation, agent integration, and error handling
---

# /CreateRoute

Create a new Hono-based API route within the Agentuity platform with proper validation, error handling, and optional agent integration.

## Usage

```
/CreateRoute <path> [options]
```

## Arguments

- `path`: Route path in kebab-case (required), e.g., `analyze/variance` or `users`

## Options

- `--methods <methods>`: HTTP methods to implement (default: GET,POST)
- `--agent <name>`: Wire to an existing agent (import and call `.run()`)
- `--validator`: Add agent `.validator()` middleware (requires --agent)
- `--cron <schedule>`: Make it a cron-triggered route (e.g., `"0 9 * * *"`)
- `--storage <types>`: Storage to use in route: `kv`, `vector`, `stream`
- `--shared`: Also create a shared data loader in `_shared/`
- `--no-tests`: Skip test considerations

## Examples

```bash
# Create an analysis route that calls an agent
/CreateRoute analyze/variance --methods POST --agent VarianceAnalyzer --validator

# Create a data retrieval route with KV caching
/CreateRoute get-data --methods GET --storage kv

# Create a cron job route
/CreateRoute daily-report --cron "0 9 * * *" --agent ReportGenerator

# Create a file upload route
/CreateRoute upload --methods POST

# Create a route with a shared data loader
/CreateRoute analyze/cash-flow --methods POST --shared --agent CashFlowProjector
```

## Output Structure

```
src/api/
├── {path}.ts                    # Route file
└── _shared/
    └── load-{resource}.ts       # Shared loader (if --shared)
```

## Workflow

1. **Validate Input**
   - Check path is valid kebab-case
   - Verify target file doesn't exist
   - If --agent, verify agent exists

2. **Generate Route**
   - Use `agentuity-route-designer` agent
   - Create `src/api/{path}.ts`
   - Implement requested HTTP methods
   - Add agent wiring if specified
   - Add storage access patterns if specified
   - Include error handling

3. **Generate Shared Loader** (if --shared)
   - Create `src/api/_shared/load-{resource}.ts`
   - Include typed interface and loading logic

4. **Report**
   - List created files
   - Show endpoint paths
   - Note testing approach

## Generated Route Template

```typescript
import { createRouter } from '@agentuity/runtime';

const router = createRouter();

router.get('/api/{path}', async (c) => {
  try {
    // TODO: Implement handler
    return c.json({ data: [] });
  } catch (error) {
    c.var.logger.error('Request failed', { error });
    return c.json({ error: 'Internal server error' }, { status: 500 });
  }
});

router.post('/api/{path}', async (c) => {
  try {
    const body = await c.req.json();
    // TODO: Implement handler
    return c.json({ success: true, data: body }, { status: 201 });
  } catch (error) {
    c.var.logger.error('Request failed', { error });
    return c.json({ error: 'Internal server error' }, { status: 500 });
  }
});

export default router;
```

## Generated Route with Agent Template

```typescript
import { createRouter } from '@agentuity/runtime';
import myAgent from '@agent/my-agent';

const router = createRouter();

router.post('/api/{path}', myAgent.validator(), async (c) => {
  try {
    const input = c.req.valid('json');
    const result = await myAgent.run(input);
    return c.json(result);
  } catch (error) {
    c.var.logger.error('Agent call failed', { error });
    return c.json({ error: 'Processing failed' }, { status: 500 });
  }
});

export default router;
```

## Related Commands

- `/CreateAgent` - For creating agents that this route calls
- `/ImplementFeature` - For implementing complete features
- `/GenerateTests` - For generating API test coverage
