# Wire Project - AI Agent Context

## Project Overview

Wire is a project repository that serves as a foundation for development. This document provides context and guidelines for AI agents working on this codebase.

## Project Structure

```
wire/
├── .github/              # GitHub configuration and workflows
│   └── copilot-instructions.md
├── LICENSE               # Project license
├── README.md            # Project documentation
└── AGENTS.md            # This file - AI agent context
```

## Technology Stack

This is a minimal repository that can be extended with various technologies. When adding new components:

- Choose appropriate, well-maintained libraries and frameworks
- Follow industry best practices for the chosen technology
- Document any new dependencies or setup requirements
- Ensure compatibility with the existing project structure

## Coding Standards

### General Guidelines

1. **Clarity Over Cleverness**: Write code that is easy to understand and maintain
2. **Consistency**: Follow existing patterns and conventions in the codebase
3. **Documentation**: Document complex logic and public APIs
4. **Testing**: Write tests that verify behavior, not implementation

### File Organization

- Keep related files organized in appropriate directories
- Use clear, descriptive file names
- Maintain a logical project structure as the codebase grows

### Naming Conventions

- Use descriptive names that clearly indicate purpose
- Follow language-specific conventions (camelCase, snake_case, PascalCase, etc.)
- Avoid abbreviations unless they are widely understood
- Use consistent terminology throughout the codebase

## Development Workflow

### Before Starting Work

1. Read the issue or task description thoroughly
2. Understand the current state of the codebase
3. Identify the minimal changes needed
4. Consider the impact on existing functionality

### During Development

1. Make small, incremental changes
2. Test frequently
3. Commit logical units of work
4. Keep track of dependencies and requirements

### Before Completing Work

1. Run all tests and ensure they pass
2. Check for security vulnerabilities
3. Update documentation as needed
4. Review changes for quality and completeness
5. Ensure the solution actually solves the stated problem

## Testing Strategy

- Write tests that are reliable and maintainable
- Test edge cases and error conditions
- Ensure tests are fast and can be run frequently
- Mock external dependencies appropriately
- Keep test code clean and well-organized

## Security Considerations

- Never commit secrets or credentials
- Validate all inputs
- Use secure communication protocols
- Follow OWASP guidelines for web applications
- Keep dependencies up to date
- Run security scans regularly

## Documentation Standards

- Keep README.md current with setup and usage instructions
- Document configuration options
- Provide examples for complex features
- Explain the "why" behind non-obvious decisions
- Use clear, concise language

## Common Tasks

### Adding New Features

1. Plan the feature and its integration points
2. Consider backward compatibility
3. Implement with minimal disruption to existing code
4. Add comprehensive tests
5. Update documentation

### Fixing Bugs

1. Reproduce the bug reliably
2. Identify the root cause
3. Fix the underlying issue, not just the symptom
4. Add tests to prevent regression
5. Verify the fix solves the original problem

### Refactoring

1. Ensure you have good test coverage first
2. Make small, safe refactoring steps
3. Run tests after each step
4. Don't mix refactoring with feature changes
5. Maintain or improve code quality

## Quality Checklist

Before marking work as complete, verify:

- [ ] All tests pass
- [ ] No security vulnerabilities introduced
- [ ] Documentation is up to date
- [ ] Code follows project conventions
- [ ] Changes are minimal and focused
- [ ] No unnecessary dependencies added
- [ ] Commits are clear and well-organized
- [ ] The solution solves the stated problem

## AI Agent Best Practices

1. **Understand Before Acting**: Read all context before making changes
2. **Minimize Changes**: Make the smallest changes necessary
3. **Verify Your Work**: Test and validate all changes
4. **Ask When Uncertain**: Better to clarify than to guess
5. **Learn from Feedback**: Incorporate review comments and improve

## Success Metrics

- Code quality remains high or improves
- Test coverage is maintained or increases
- No regressions in functionality
- Clear, understandable changes
- Positive feedback from reviewers

---

This document should be updated as the project evolves and new patterns emerge.
