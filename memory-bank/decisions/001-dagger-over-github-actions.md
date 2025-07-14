# ADR-001: Use Dagger Python SDK over GitHub Actions

## Status

Accepted

## Date

2025-01-13

## Context

The project needed a robust CI/CD pipeline for linting and validation of Kubernetes manifests and Python code. Traditional options included:

1. GitHub Actions with YAML workflows
1. Bash/PowerShell scripts
1. Dagger for code-based pipelines
1. Jenkins or other CI/CD platforms

## Decision

We chose to implement the automation pipeline using Dagger Python SDK instead of traditional CI/CD tools.

## Rationale

### Advantages of Dagger

- **Code-based pipelines**: Python code is more maintainable than YAML
- **Local development**: Can run the same pipeline locally and in CI
- **Container isolation**: Each step runs in isolated containers
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Type safety**: Python provides better error checking than shell scripts
- **Testability**: Pipeline logic can be unit tested
- **Dependency management**: Uses Poetry for consistent environments

### Disadvantages Considered

- **Learning curve**: Team needs to learn Dagger concepts
- **Newer technology**: Less mature than GitHub Actions
- **Container overhead**: Requires Docker/container runtime
- **Complexity**: More complex than simple shell scripts

## Implementation Details

### Pipeline Structure

```python
async def lint_pipeline(client: dagger.Client) -> bool:
    """Main linting pipeline with multiple validation steps"""
    tasks = [
        yaml_lint_task(client),
        python_lint_task(client),
        security_scan_task(client)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return all(isinstance(r, bool) and r for r in results)
```

### Tool Integration

- **yamllint**: YAML validation with custom configuration
- **ruff**: Python linting and formatting (replacing flake8, black, isort)
- **Security scanning**: Custom validation for Kubernetes manifests
- **Poetry**: Dependency management and task runner

### Cross-Platform Support

- Created both `.sh` and `.ps1` wrapper scripts
- Used Poetry for consistent dependency management
- Handled path separators correctly across platforms

## Consequences

### Positive

- Consistent pipeline execution across environments
- Better error handling and reporting
- Easier to extend and maintain
- Strong typing and IDE support
- Can run individual pipeline steps for debugging

### Negative

- Requires Docker/container runtime for execution
- Initial setup complexity higher than simple scripts
- Team needs to learn Dagger-specific patterns

## Alternatives Considered

### GitHub Actions

- **Pros**: Mature, well-documented, integrated with GitHub
- **Cons**: YAML-based, hard to test locally, vendor lock-in

### Shell Scripts

- **Pros**: Simple, universal, no dependencies
- **Cons**: Hard to maintain, poor error handling, platform-specific

### Jenkins

- **Pros**: Mature, flexible, self-hosted
- **Cons**: Heavy infrastructure, complex setup, maintenance overhead

## Review Date

This decision should be reviewed in 6 months (July 2025) to assess:

- Team adoption and satisfaction
- Pipeline reliability and performance
- Maintenance burden compared to alternatives
- Evolution of Dagger ecosystem
