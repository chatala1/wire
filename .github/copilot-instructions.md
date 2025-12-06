# Copilot Instructions for Wire Repository

## Overview

This repository contains the Wire project. When working on this repository, please follow these guidelines to ensure high-quality contributions.

## Development Guidelines

### General Principles

1. **Make Minimal Changes**: Always make the smallest possible changes to accomplish the task. Avoid unnecessary refactoring or modifications to working code.

2. **Preserve Existing Functionality**: Do not delete or modify working files unless absolutely necessary for the task at hand.

3. **Follow Existing Patterns**: Study the existing codebase and follow established patterns, conventions, and coding styles.

4. **Test Your Changes**: Ensure all changes are properly tested before committing. Run existing tests and add new tests when adding new functionality.

## Code Quality

### Best Practices

- Write clear, self-documenting code with descriptive variable and function names
- Keep functions small and focused on a single responsibility
- Add comments only when necessary to explain complex logic or non-obvious decisions
- Ensure all code is properly formatted and follows the project's style guide

### Security

- Never commit secrets, API keys, or sensitive credentials to the repository
- Validate and sanitize all user inputs
- Follow secure coding practices and be aware of common vulnerabilities
- Run security scans before finalizing changes

## Git Workflow

### Commits

- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Use conventional commit format when applicable (e.g., `feat:`, `fix:`, `docs:`, `chore:`)

### Pull Requests

- Provide clear descriptions of what was changed and why
- Reference related issues in PR descriptions
- Ensure CI/CD checks pass before requesting review
- Respond to review feedback promptly and professionally

## Testing

- Run all existing tests before committing changes
- Add tests for new functionality
- Ensure tests are meaningful and test actual behavior, not implementation details
- Maintain or improve code coverage with each change

## Documentation

- Update documentation when making changes that affect user-facing features
- Keep README.md up to date
- Document any new configuration options or environment variables
- Include examples in documentation when appropriate

## Issue Resolution

When working on issues:

1. Read the entire issue description carefully
2. Understand the problem before proposing a solution
3. Ask clarifying questions if requirements are unclear
4. Propose a solution before implementing, if the approach is complex
5. Test the solution thoroughly against the issue requirements

## Communication

- Be clear and concise in all communications
- Provide context when asking questions
- Share your reasoning when making significant decisions
- Be respectful and professional in all interactions

## Resources

- README.md: Project overview and setup instructions
- LICENSE: Project license information

---

Remember: Quality over speed. Take the time to understand the problem and implement a robust, maintainable solution.
