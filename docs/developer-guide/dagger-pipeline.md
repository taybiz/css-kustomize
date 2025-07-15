# Dagger Pipeline

Deep dive into the Dagger pipeline implementation and internals.

## Overview

The CSS Kustomize project uses Dagger for containerized CI/CD pipelines, providing consistent execution environments and reproducible builds.

## Pipeline Architecture

### Core Components

```python
@dagger.function
async def lint_yaml(self, source: dagger.Directory) -> str:
    """Run YAML linting with yamllint."""
    return await (
        self.base_container()
        .with_directory("/src", source)
        .with_workdir("/src")
        .with_exec(["yamllint", "."])
        .stdout()
    )
```

### Container Strategy

All operations run in isolated containers:

- **Base Container**: Alpine Linux with required tools
- **Tool-Specific Containers**: Specialized for each operation
- **Caching**: Aggressive caching for performance

## Pipeline Functions

### Linting Operations

#### YAML Linting

```python
async def lint_yaml(self, source: dagger.Directory) -> str:
    """Lint YAML files using yamllint."""
```

#### Python Linting

```python
async def lint_python(self, source: dagger.Directory) -> str:
    """Lint Python files using ruff."""
```

#### Markdown Linting

```python
async def lint_markdown(self, source: dagger.Directory) -> str:
    """Check Markdown formatting."""
```

### Validation Operations

#### Kustomize Validation

```python
async def validate_kustomize(self, source: dagger.Directory) -> str:
    """Validate all Kustomize overlays."""
```

#### Version Validation

```python
async def validate_versions(self, source: dagger.Directory) -> str:
    """Validate version consistency across overlays."""
```

### Generation Operations

#### Manifest Generation

```python
async def generate_manifests(
    self, 
    source: dagger.Directory,
    output_dir: str
) -> dagger.Directory:
    """Generate Kubernetes manifests for all overlays."""
```

#### Single Overlay Generation

```python
async def generate_overlay(
    self,
    source: dagger.Directory,
    overlay_name: str
) -> str:
    """Generate manifest for specific overlay."""
```

### Security Operations

#### Security Scanning

```python
async def security_scan(self, source: dagger.Directory) -> str:
    """Run security checks on Kustomize configurations."""
```

#### Generated Manifest Scanning

```python
async def security_scan_generated(
    self,
    manifests_dir: dagger.Directory
) -> str:
    """Scan generated manifests for security issues."""
```

## Container Images

### Base Container

```python
def base_container(self) -> dagger.Container:
    """Create base container with common tools."""
    return (
        dag.container()
        .from_("alpine:3.19")
        .with_exec(["apk", "add", "--no-cache", 
                   "python3", "py3-pip", "kubectl", "git"])
        .with_exec(["pip", "install", "yamllint", "ruff"])
    )
```

### Specialized Containers

#### Kustomize Container

```python
def kustomize_container(self) -> dagger.Container:
    """Container with kubectl and kustomize."""
    return (
        self.base_container()
        .with_exec(["kubectl", "version", "--client"])
    )
```

#### Security Scanner Container

```python
def security_container(self) -> dagger.Container:
    """Container with security scanning tools."""
    return (
        self.base_container()
        .with_exec(["pip", "install", "checkov"])
    )
```

## Caching Strategy

### Layer Caching

Dagger automatically caches container layers:

- Base image layers
- Package installation layers
- Tool installation layers

### Volume Caching

Persistent caches for:

- Package manager caches
- Tool caches
- Build artifacts

### Cache Keys

Cache invalidation based on:

- Source code changes
- Dependency changes
- Tool version changes

## Error Handling

### Exception Management

```python
try:
    result = await self.lint_yaml(source)
except dagger.ExecError as e:
    logger.error(f"YAML linting failed: {e}")
    raise PipelineError("Linting failed") from e
```

### Graceful Degradation

- Continue on non-critical failures
- Aggregate error reporting
- Detailed error context

## Integration Points

### CLI Integration

```python
@click.command()
@click.option("--verbose", is_flag=True)
async def lint(verbose: bool):
    """Run linting pipeline."""
    async with dagger.Connection() as client:
        pipeline = CSSKustomizePipeline(client)
        result = await pipeline.lint_all(source_dir)
        click.echo(result)
```

### CI/CD Integration

```python
async def ci_pipeline(self, source: dagger.Directory) -> bool:
    """Complete CI pipeline."""
    # Run all operations
    lint_result = await self.lint_all(source)
    validate_result = await self.validate_all(source)
    security_result = await self.security_scan_all(source)
    
    return all([lint_result, validate_result, security_result])
```

## Performance Optimization

### Build Optimization

- Multi-stage container builds
- Minimal base images
- Efficient layer ordering

### Execution Optimization

- Smart dependency management
- Resource pooling

### Cache Optimization

- Aggressive caching strategies
- Cache warming techniques
- Cache invalidation optimization

## Debugging and Troubleshooting

### Verbose Mode

```python
if verbose:
    container = container.with_env_variable("DAGGER_LOG_LEVEL", "debug")
```

### Container Inspection

```python
# Debug container state
debug_container = (
    container
    .with_exec(["ls", "-la"])
    .with_exec(["env"])
)
```

### Log Collection

```python
# Collect logs from failed operations
logs = await container.stderr()
logger.error(f"Operation failed: {logs}")
```

## Extension Patterns

### Adding New Operations

1. **Define Function**:

   ```python
   @dagger.function
   async def new_operation(self, source: dagger.Directory) -> str:
       """New pipeline operation."""
   ```

1. **Add CLI Command**:

   ```python
   @click.command()
   async def new_command():
       """CLI command for new operation."""
   ```

1. **Integrate with CI**:

   ```python
   # Add to ci_pipeline function
   new_result = await self.new_operation(source)
   ```

### Custom Containers

```python
def custom_container(self) -> dagger.Container:
    """Custom container for specific needs."""
    return (
        dag.container()
        .from_("custom/base:latest")
        .with_exec(["custom-tool", "--version"])
    )
```

## Best Practices

### Container Design

- Use minimal base images
- Install only required tools
- Leverage multi-stage builds
- Implement proper caching

### Function Design

- Keep functions focused and small
- Use proper error handling
- Implement comprehensive logging
- Design for testability

### Performance

- Implement proper caching
- Optimize container layers
- Monitor resource usage

## Next Steps

- Learn about [Contributing](contributing.md)
- Explore [Architecture](architecture.md)
