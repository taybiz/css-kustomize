# Architecture

Understanding the CSS Kustomize project architecture and design decisions.

## Overview

CSS Kustomize is designed as a modern DevOps solution that combines Kubernetes manifests, Kustomize overlays, and Dagger automation for a complete CI/CD experience.

## System Components

### 1. Base Kubernetes Manifests

Located in `base/`, these provide the foundation:

- `deployment.yaml`: Core Community Solid Server deployment
- `service.yaml`: Kubernetes service configuration
- `kustomization.yaml`: Base Kustomize configuration

### 2. Overlay System

Environment-specific configurations in `overlays/`:

- **with-pvc**: Production with storage
- **without-pvc**: Stateless production

### 3. Dagger Pipeline

Python-based automation in `dagger_pipeline/`:

- **main.py**: CLI interface using Click
- **pipeline.py**: Core pipeline logic and Dagger functions

### 4. Documentation System

MkDocs-based documentation:

- **docs/**: Source documentation
- **mkdocs.yml**: Configuration
- **Auto-generated API docs**: From Python docstrings

## Design Principles

### 1. Containerized Everything

All operations run in containers via Dagger:

- Consistent execution environment
- Reproducible builds
- No local tool dependencies

### 2. Release Name Strategy

Consistent labeling across all resources:

- `app.kubernetes.io/instance` labels
- Environment-specific release names
- Proper resource isolation

### 3. Version Management

Centralized version control:

- Semantic versioning
- Consistent across all overlays
- Automated updates and validation

### 4. Developer Experience

Rich CLI with modern features:

- Colored output and progress indicators
- Verbose mode for debugging
- Parallel execution options

## Data Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Base YAML     │    │   Kustomize      │    │   Generated     │
│   Manifests     │───▶│   Overlays       │───▶│   Manifests     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Linting &     │    │   Validation     │    │   Security      │
│   Formatting    │    │   Checks         │    │   Scanning      │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Technology Stack

### Core Technologies

- **Kubernetes**: Container orchestration platform
- **Kustomize**: Kubernetes configuration management
- **Dagger**: Containerized CI/CD pipelines
- **Python**: Automation and CLI development

### Development Tools

- **Poetry**: Dependency management
- **Click**: CLI framework
- **Ruff**: Python linting and formatting
- **yamllint**: YAML validation
- **MkDocs**: Documentation generation

### Container Images

- **Community Solid Server**: Main application
- **Alpine Linux**: Base for utility containers
- **Python**: For Dagger pipeline execution

## Security Architecture

### Container Security

- Non-root user execution
- Read-only root filesystems
- Security contexts applied
- Resource limits enforced

### Pipeline Security

- Isolated container execution
- No persistent credentials
- Scan generated manifests
- Validate security contexts

### Access Control

- RBAC-ready manifests
- Service account configuration
- Network policy support
- Secret management patterns

## Scalability Considerations

### Horizontal Scaling

- Stateless deployment options
- Load balancer ready services
- Resource request/limit patterns

### Performance

- Parallel pipeline execution
- Dagger caching strategies
- Efficient container builds
- Optimized manifest generation

## Extension Points

### Adding New Overlays

1. Create overlay directory structure
1. Define kustomization.yaml
1. Add to CLI overlay list
1. Update documentation

### Custom Pipeline Steps

1. Extend pipeline.py with new functions
1. Add CLI commands in main.py
1. Update documentation
1. Add tests

### Integration Hooks

- Pre-commit hooks for development
- CI/CD pipeline integration
- Custom validation rules
- External tool integration

## Monitoring and Observability

### Pipeline Metrics

- Execution time tracking
- Success/failure rates
- Resource usage monitoring
- Cache hit rates

### Application Metrics

- Kubernetes resource monitoring
- Application health checks
- Performance metrics
- Error tracking

## Next Steps

- Learn about [Dagger Pipeline](dagger-pipeline.md) internals
- Read [Contributing Guide](contributing.md)
- Explore [Examples](../examples/basic-usage.md)
