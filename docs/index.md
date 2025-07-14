# CSS Kustomize Documentation

Welcome to the CSS Kustomize project documentation! This project provides Kubernetes manifests for the Community Solid Server with comprehensive Dagger automation for CI/CD pipelines.

## Overview

CSS Kustomize is a modern DevOps solution that combines:

- **Kubernetes Manifests**: Production-ready configurations for Community Solid Server
- **Kustomize Overlays**: Environment-specific customizations with proper release name strategies
- **Dagger Automation**: Containerized CI/CD pipelines with comprehensive linting and validation
- **Python CLI**: Rich command-line interface for development and deployment workflows

## Key Features

### 🚀 **Automated CI/CD Pipeline**

- Comprehensive linting (YAML, Python, Markdown)
- Kustomize validation and manifest generation
- Security scanning for Kubernetes resources
- Parallel execution for maximum performance

### 🏷️ **Release Name Strategy**

- Consistent `app.kubernetes.io/instance` labeling
- Environment-specific release names
- Proper resource isolation and identification
- Easy querying and management

### 🔧 **Developer Experience**

- Rich CLI with colored output and progress indicators
- Verbose mode for debugging and troubleshooting
- Fast feedback loops with caching strategies
- Cross-platform compatibility

### 📦 **Production Ready**

- Security best practices built-in
- Comprehensive validation and testing
- Documentation-driven development
- Modern tooling and dependencies

## Quick Start

Get started with CSS Kustomize in just a few commands:

```bash
# Clone the repository
git clone https://github.com/your-org/css-kustomize.git
cd css-kustomize

# Install dependencies
poetry install

# Run comprehensive CI pipeline
poetry run dagger-pipeline ci

# Generate manifests for all overlays
poetry run dagger-pipeline generate manifests/

# Build specific overlay
kubectl kustomize overlays/with-pvc
```

## Project Structure

```
css-kustomize/
├── base/                    # Base Kubernetes manifests
├── overlays/               # Environment-specific overlays
│   ├── local-base/        # Local development (no PVC)
│   ├── local-pvc/         # Local development (with PVC)
│   ├── with-pvc/          # Production with persistent storage
│   └── without-pvc/       # Stateless deployment
├── dagger_pipeline/       # Dagger automation code
│   ├── main.py           # CLI interface
│   └── pipeline.py       # Core pipeline logic
├── docs/                  # Documentation source
├── manifests/            # Generated manifests
└── scripts/              # Utility scripts
```

## Available Overlays

| Overlay       | Release Name      | Purpose                | Storage |
| ------------- | ----------------- | ---------------------- | ------- |
| `local-base`  | `css-local`       | Local development      | None    |
| `local-pvc`   | `css-local-pvc`   | Local with persistence | PVC     |
| `with-pvc`    | `css-with-pvc`    | Production-like        | PVC     |
| `without-pvc` | `css-without-pvc` | Stateless              | None    |

## CLI Commands

The project provides a comprehensive CLI for all operations:

```bash
# Linting and validation
poetry run dagger-pipeline lint --yaml --python --markdown
poetry run dagger-pipeline validate

# Manifest generation
poetry run dagger-pipeline generate manifests/
poetry run dagger-pipeline generate-overlay with-pvc manifests/

# Security scanning
poetry run dagger-pipeline security-scan
poetry run dagger-pipeline security-scan-generated manifests/

# Version management
poetry run dagger-pipeline update-version 6.0.3
poetry run dagger-pipeline version-report

# Complete CI pipeline
poetry run dagger-pipeline ci --verbose
```

## Documentation Sections

### 📚 **Getting Started**

- [Installation](getting-started/installation.md) - Set up your development environment
- [Quick Start](getting-started/quick-start.md) - Get running in minutes
- [Configuration](getting-started/configuration.md) - Customize for your needs

### 👥 **User Guide**

- [CLI Commands](user-guide/cli-commands.md) - Complete command reference
- [Kustomize Overlays](user-guide/kustomize-overlays.md) - Working with overlays
- [Release Names](user-guide/release-names.md) - Release name strategy
- [Version Management](user-guide/version-management.md) - Managing versions

### 🔧 **Developer Guide**

- [Architecture](developer-guide/architecture.md) - System design and components
- [Dagger Pipeline](developer-guide/dagger-pipeline.md) - Pipeline internals
- [Caching Strategy](developer-guide/caching-strategy.md) - Performance optimization
- [Contributing](developer-guide/contributing.md) - How to contribute

### 📖 **API Reference**

- [Pipeline Module](developer-guide/dagger-pipeline.md) - Core pipeline classes and functions
- [CLI Module](user-guide/cli-commands.md) - Command-line interface reference

### 💡 **Examples**

- [Basic Usage](examples/basic-usage.md) - Common workflows
- [Advanced Workflows](examples/advanced-workflows.md) - Complex scenarios
- [CI/CD Integration](examples/cicd-integration.md) - Integration patterns

## Community and Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/your-org/css-kustomize/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/your-org/css-kustomize/discussions)
- **Contributing**: See our [Contributing Guide](developer-guide/contributing.md)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/your-org/css-kustomize/blob/main/LICENSE) file for details.
