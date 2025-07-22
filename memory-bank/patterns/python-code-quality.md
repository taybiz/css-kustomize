# Python Code Quality Patterns

## Overview

Project-specific guidelines for Python code quality, emphasizing consistent formatting, proper exception handling, and compliance with Ruff linting rules across the CSS Kustomize project.

## Code Formatting Standards

### Ruff Formatting Requirements

**Mandatory Process**: Always run `poetry run ruff format .` after any Python code modifications

- Apply formatting before committing changes to maintain consistent code style
- Use Ruff as the primary formatting tool for all Python files in the project
- Format Python code immediately after making changes, not just before commits
- Include formatting step in any Python-related development tasks
- Ensure formatting is applied to entire project directory using `.` argument

### Development Workflow Integration

- Treat code formatting as mandatory step in development process
- Maintain consistency with project's existing Ruff configuration
- Apply formatting to all Python files including:
  - Pipeline modules in `dagger_pipeline/`
  - Configuration scripts
  - Test files
  - Utility scripts

### Quality Assurance Process

- Run formatting validation as part of pre-commit hooks
- Include formatting checks in CI/CD pipeline
- Validate formatting consistency during code review
- Maintain project-wide formatting standards

## Exception Handling Patterns

### Exception Chaining Requirements

**Ruff B904 Compliance**: Always use proper exception chaining to maintain error context

#### Required Patterns

**When re-raising with additional context:**

```python
try:
    risky_operation()
except OriginalException as e:
    raise CustomException("Operation failed with additional context") from e
```

**When catching subprocess errors:**

```python
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    raise Exception(f"Command failed: {e}") from e
```

**When suppressing original context (use sparingly):**

```python
try:
    operation()
except OriginalException as e:
    raise CustomException("User-friendly message") from None
```

#### Anti-Patterns to Avoid

**❌ Bare re-raising without chaining:**

```python
try:
    operation()
except Exception as e:
    raise Exception("Something went wrong")  # Missing 'from e'
```

**❌ Losing exception context:**

```python
try:
    operation()
except Exception:
    raise Exception("Generic error")  # No context preserved
```

### Exception Handling Best Practices

#### Maintain Debugging Information

- Always preserve original exception chain for debugging
- Use `raise ... from e` to maintain stack trace context
- Only use `raise ... from None` when explicitly suppressing context
- Include relevant context in exception messages

#### Specific Exception Types

- Use specific exception types rather than generic `Exception`
- Create custom exception classes for domain-specific errors
- Include actionable information in exception messages
- Maintain consistent exception handling patterns across codebase

#### Error Context Preservation

```python
# Good: Preserves full error context
try:
    result = complex_operation()
except NetworkError as e:
    raise ProcessingError(f"Failed to process due to network issue: {e}") from e
except ValidationError as e:
    raise ProcessingError(f"Invalid data provided: {e}") from e
```

## Code Quality Compliance

### Ruff Integration

#### Linting Commands

```bash
# Check for all issues including B904
poetry run ruff check .

# Check specifically for exception handling issues
poetry run ruff check . --select B904

# Auto-fix issues where possible
poetry run ruff check . --fix

# Format code
poetry run ruff format .
```

#### Configuration Management

- Centralize Ruff configuration in `pyproject.toml`
- Maintain consistent rules across development team
- Document any rule exceptions or customizations
- Regular review and update of linting rules

### Development Workflow

#### Pre-commit Validation

- Exception handling validation as part of pre-commit hooks
- Automated formatting checks before commits
- Consistent application of code quality standards
- Fast feedback on code quality issues

#### Code Review Process

- Check exception handling during code review
- Validate proper exception chaining patterns
- Ensure consistent formatting application
- Verify compliance with project standards

#### Continuous Integration

- Run full Ruff checks in CI pipeline
- Fail builds on code quality violations
- Provide clear feedback on quality issues
- Maintain quality gates for all code changes

## Project-Specific Patterns

### Dagger Pipeline Context

Exception handling is particularly important in the Dagger pipeline modules:

```python
async def pipeline_task(client: dagger.Client) -> bool:
    """Pipeline task with proper exception handling"""
    try:
        result = await client.container().from_("python:3.11").sync()
        return True
    except dagger.DaggerError as e:
        raise PipelineError(f"Dagger operation failed: {e}") from e
    except Exception as e:
        raise PipelineError(f"Unexpected error in pipeline: {e}") from e
```

### Release Management Context

Proper exception handling supports robust automation workflows:

```python
def release_operation():
    """Release operation with comprehensive error handling"""
    try:
        validate_release_conditions()
        execute_release_steps()
    except ValidationError as e:
        raise ReleaseError(f"Release validation failed: {e}") from e
    except ExecutionError as e:
        raise ReleaseError(f"Release execution failed: {e}") from e
```

## Tool Configuration

### Ruff Configuration Example

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "B",   # flake8-bugbear
    "B904", # Exception handling
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Integration with Poetry

```toml
[tool.poetry.group.dev.dependencies]
ruff = "^0.1.0"

[tool.poetry.scripts]
lint = "ruff check ."
format = "ruff format ."
```

## Measuring Code Quality

### Quality Metrics

- Zero Ruff B904 violations in codebase
- Consistent formatting across all Python files
- Proper exception chaining in all error handling
- Fast feedback on code quality issues

### Maintenance Practices

- Regular updates to Ruff version and rules
- Periodic review of exception handling patterns
- Team training on code quality standards
- Documentation updates as standards evolve

## Troubleshooting

### Common Issues

**Ruff B904 violations:**

- Add proper exception chaining with `from e`
- Review exception handling patterns
- Use `from None` only when context suppression is intentional

**Formatting inconsistencies:**

- Run `poetry run ruff format .` to fix
- Check for configuration conflicts
- Ensure consistent tool versions across team

### Resolution Strategies

- Use automated fixing where possible
- Maintain clear documentation of standards
- Provide examples of correct patterns
- Regular team review of quality practices

## Cross-References

- See `.clinerules/python-formatting.md` and `.clinerules/python-exception-handling.md` for original rule specifications
- Related: [`dagger-automation.md`](dagger-automation.md) for pipeline-specific patterns
- Related: [`../troubleshooting/common-issues.md`](../troubleshooting/common-issues.md) for troubleshooting formatting and linting issues
- Related: [`../workflows/development-workflow.md`](../workflows/development-workflow.md) for workflow integration

______________________________________________________________________

*This pattern supports the project's emphasis on robust automation workflows and maintainable Python code through consistent quality standards.*
