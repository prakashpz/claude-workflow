---
name: CreateAgent
description: Create a new Agentuity agent with handler, schema, evaluations, and optional route wiring
---

# /CreateAgent

Create a new Agentuity agent with proper structure, typed schemas, and optional API route integration.

## Usage

```
/CreateAgent <AgentName> [options]
```

## Arguments

- `AgentName`: PascalCase name for the agent (required)

## Options

- `--description <desc>`: Agent description
- `--schema <type>`: Schema style: `typed` (with input/output schema, default), `raw` (no schema)
- `--storage <types>`: Comma-separated storage types to use: `kv`, `vector`, `stream`, `thread`
- `--ai`: Include AI Gateway boilerplate (generateText/generateObject)
- `--route`: Also create an API route that invokes this agent
- `--calls <agents>`: Comma-separated agent names this agent calls
- `--eval`: Include evaluation file
- `--no-eval`: Skip evaluation file

## Examples

```bash
# Create a typed agent with AI integration
/CreateAgent CashFlowProjector --description "Projects cash flow for 8 weeks" --schema typed --ai --storage kv,thread

# Create a raw agent that orchestrates others
/CreateAgent FinancialOrchestrator --schema raw --calls "VarianceAnalyzer,AnomalyDetector,CashFlowProjector"

# Create an agent with a corresponding API route
/CreateAgent DuplicateScanner --description "Scans transactions for duplicates" --ai --route --eval

# Create a simple data processing agent
/CreateAgent DataValidator --schema typed --storage kv
```

## Output Structure

```
src/agent/{AgentName}/
├── index.ts          # createAgent() with handler
└── eval.ts           # Agent evaluations (if --eval)

src/api/{agent-name}.ts   # API route (if --route)
```

## Workflow

1. **Validate Input**
   - Check AgentName is PascalCase
   - Verify target directory doesn't exist
   - Validate storage types

2. **Generate Agent**
   - Use `agentuity-agent-architect` agent
   - Create `src/agent/{AgentName}/index.ts`
   - Include schema definitions
   - Add storage API usage patterns
   - Wire agent-to-agent calls if specified

3. **Generate Evaluations** (if requested)
   - Create `src/agent/{AgentName}/eval.ts`
   - Include basic response eval
   - Include schema validation eval

4. **Generate Route** (if requested)
   - Use `agentuity-route-designer` agent
   - Create `src/api/{agent-name}.ts`
   - Wire agent import and `.run()` call
   - Add `.validator()` middleware

5. **Report**
   - List created files
   - Show next steps (implement handler logic)

## Generated Agent Template

```typescript
import { createAgent } from '@agentuity/runtime';
import { s } from '@agentuity/schema';

const agent = createAgent('{AgentName}', {
  description: '{description}',
  schema: {
    input: s.object({
      // TODO: Define input schema
    }),
    output: s.object({
      // TODO: Define output schema
    }),
  },
  handler: async (ctx, input) => {
    ctx.logger.info('{AgentName} processing', { input });

    // TODO: Implement agent logic

    return {
      // TODO: Return matching output schema
    };
  },
});

export default agent;
```

## Related Commands

- `/ImplementFeature` - For implementing complete features
- `/CreateRoute` - For creating standalone API routes
- `/GenerateTests` - For generating additional test coverage
