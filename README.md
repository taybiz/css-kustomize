# CSS Kustomize - Community Solid Server

Kubernetes manifests for deploying the Community Solid Server using Kustomize, with comprehensive Dagger automation for CI/CD pipelines.

## Quick Start

```bash
# Install dependencies
poetry install

# Run comprehensive CI pipeline
poetry run dagger-pipeline ci

# Deploy with persistent storage
kubectl apply -k overlays/with-pvc/

# Deploy with ephemeral storage
kubectl apply -k overlays/without-pvc/
```

## Key Features

- **🔒 Security-first**: Non-root execution, comprehensive security contexts
- **🚀 Dagger Automation**: Modern containerized CI/CD pipeline
- **🏷️ Release Management**: Consistent labeling and version strategies
- **💾 Storage Options**: Persistent and ephemeral storage configurations
- **🔧 Developer Experience**: Rich CLI with caching and parallel execution

## Project Structure

```
├── base/                    # Base Kubernetes manifests
├── overlays/               # Environment-specific overlays
├── components/             # Reusable Kustomize components
├── dagger_pipeline/        # Dagger automation code
├── docs/                   # Comprehensive documentation
└── manifests/              # Generated manifests
```

## Documentation

For detailed information, see the comprehensive documentation:

- **[Getting Started](docs/getting-started/)** - Installation, quick start, and configuration
- **[User Guide](docs/user-guide/)** - CLI commands, overlays, release names, and version management
- **[Developer Guide](docs/developer-guide/)** - Architecture, Dagger pipeline, and contributing
- **[Examples](docs/examples/)** - Basic usage, advanced workflows, and CI/CD integration

### Quick Links

- [Installation Guide](docs/getting-started/installation.md)
- [CLI Commands Reference](docs/user-guide/cli-commands.md)
- [Dagger Pipeline Guide](docs/developer-guide/dagger-pipeline.md)
- [Contributing Guidelines](docs/developer-guide/contributing.md)

## Common Commands

```bash
# Development workflow
poetry run dagger-pipeline lint              # Comprehensive linting
poetry run dagger-pipeline generate          # Generate manifests
poetry run dagger-pipeline version update    # Update versions

# Deployment
kubectl apply -k overlays/with-pvc/          # With persistent storage
kubectl apply -k overlays/without-pvc/       # With ephemeral storage
```

## Resources

- [Community Solid Server](https://github.com/CommunitySolidServer/CommunitySolidServer)
- [Dagger Documentation](https://docs.dagger.io/)
- [Kustomize Documentation](https://kustomize.io/)
- [Project Documentation](docs/)
