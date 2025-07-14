# Dagger Automation Patterns

## Pipeline Architecture

The project uses Dagger Python SDK for automation, replacing traditional CI/CD tools with code-based pipelines.

### Core Components

- `dagger_pipeline/main.py`: Entry point and CLI interface
- `dagger_pipeline/pipeline.py`: Pipeline logic and container operations
- `pyproject.toml`: Tool configuration and dependencies

### Pipeline Structure

```python
async def lint_pipeline(client: dagger.Client) -> bool:
    """Main linting pipeline with multiple validation steps"""
    # 1. YAML linting with yamllint
    # 2. Python linting with ruff
    # 3. Security scanning
    # 4. Manifest generation validation
```

## Best Practices

### Container Management

- Use specific base images (python:3.11-slim)
- Cache dependencies between pipeline runs
- Mount source code as directories, not files
- Use with_workdir() for consistent working directories

### Error Handling

- Implement comprehensive error catching
- Provide clear, actionable error messages
- Use colored output for better UX
- Return boolean success indicators

### Configuration Management

- Centralize tool configurations in pyproject.toml
- Use separate dependency groups for different concerns
- Make configurations permissive for real-world usage
- Document all configuration options

## Modular Design Patterns

### Task Isolation

```python
async def yaml_lint_task(client: dagger.Client) -> bool:
    """Isolated YAML linting task"""
    # Single responsibility
    # Clear input/output contract
    # Reusable across pipelines
```

### Dependency Injection

- Pass Dagger client as parameter
- Use async/await for all operations
- Avoid global state
- Make functions testable

### Cross-Platform Support

- Create both .sh and .ps1 wrapper scripts
- Use Poetry for consistent dependency management
- Handle path separators correctly
- Test on multiple platforms

## Performance Optimization

- Use container caching effectively
- Parallelize independent tasks when possible
- Minimize container rebuilds
- Cache tool installations
