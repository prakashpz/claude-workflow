# Contributing to Claude Workflow System

Thank you for your interest in contributing to the Claude Workflow System! This document provides guidelines for contributing.

## Ways to Contribute

- **Bug Reports**: Report issues you encounter
- **Feature Requests**: Suggest new features or improvements
- **Documentation**: Improve or add documentation
- **Code**: Submit bug fixes or new features
- **Variants**: Create new project-type variants

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/claude-workflow.git
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Validate your changes:
   ```bash
   # Validate a variant
   python scripts/validate-variant.py variants/your-variant

   # Test initialization
   python scripts/init-project.py /tmp/test-project --variant nextjs-development
   ```

## Coding Standards

### Markdown Files (Commands, Agents, Tasks)

- Use consistent frontmatter format
- Include all required sections
- Follow existing formatting conventions
- Add usage examples

### Python Scripts

- Follow PEP 8 style guidelines
- Include docstrings for functions
- Add type hints where appropriate
- Handle errors gracefully

### JSON Files

- Use 2-space indentation
- Validate against schemas
- Include comments via description fields

## Commit Messages

Follow conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(nextjs): add CreateComponent command
fix(session): handle missing state file gracefully
docs(readme): add installation instructions
```

## Pull Request Process

1. Update documentation for any new features
2. Add or update tests as appropriate
3. Ensure all validation passes
4. Update CHANGELOG.md if applicable
5. Submit PR with clear description

### PR Description Template

```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
How were these changes tested?

## Checklist
- [ ] Documentation updated
- [ ] Validation passes
- [ ] Follows coding standards
```

## Creating Variants

See [Creating Variants](docs/creating-variants.md) for detailed instructions.

Key points:
1. Follow the manifest schema
2. Include comprehensive documentation
3. Test with the init-project script
4. Validate with validate-variant script

## Reporting Issues

When reporting issues, include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: How to reproduce the problem
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, etc.

## Feature Requests

When requesting features:

1. **Use Case**: Describe the problem you're trying to solve
2. **Proposed Solution**: Your idea for addressing it
3. **Alternatives**: Other approaches you've considered
4. **Additional Context**: Any other relevant information

## Code Review

All submissions require review. Reviewers will check:

- Code quality and style
- Documentation completeness
- Test coverage
- Compatibility with existing components

## Community

- Be respectful and constructive
- Help others when you can
- Follow the code of conduct

## Questions?

- Open an issue for questions about contributing
- Check existing issues and documentation first

Thank you for contributing!
