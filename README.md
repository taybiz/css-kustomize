# CSS Kustomize - Community Solid Server

This repository contains Kubernetes manifests for deploying the Community Solid Server using Kustomize, with a focus on security best practices and local testing capabilities.

## 🏗️ Structure

```
├── base/                           # Base Kustomize configuration
│   ├── deployment.yaml            # Main deployment (runs as non-root, uses emptyDir)
│   ├── service.yaml               # Service configuration
│   └── kustomization.yaml         # Base kustomization
├── components/                    # Optional Kustomize components
│   └── pvc/                       # PVC component (replaces emptyDir)
│       ├── deployment-patch.yaml  # Patches deployment to use PVC
│       ├── kustomization.yaml     # Component kustomization
│       └── pvc.yaml               # Persistent Volume Claim definition
├── overlays/                      # Environment-specific overlays
│   ├── with-pvc/                  # Deployment with persistent storage
│   │   └── kustomization.yaml     # Uses PVC component
│   ├── without-pvc/               # Deployment with ephemeral storage
│   │   └── kustomization.yaml     # Uses base emptyDir
│   └── local-pvc/                 # Legacy overlay (deprecated)
│       ├── deployment-patch.yaml  # Deployment patches
│       ├── kustomization.yaml     # Overlay kustomization
│       └── pvc.yaml               # Persistent Volume Claim
├── dagger_pipeline/               # Dagger automation pipeline
│   ├── __init__.py                # Package initialization
│   ├── main.py                    # CLI entry point
│   └── pipeline.py                # Core pipeline implementation
├── manifests/                     # Generated manifests (created by Dagger)
├── .clinerules/                   # Cline development rules
│   └── linting-automation.md      # Linting and automation guidelines
├── .github/workflows/             # GitHub Actions workflows
│   └── dagger-ci.yml              # Dagger-based CI pipeline
├── dagger.json                    # Dagger project configuration
├── pyproject.toml                 # Python project and dependencies
├── .yamllint.yml                  # YAML linting configuration
└── .pre-commit-config.yaml        # Pre-commit hooks configuration
```

## 🔒 Security Features

- **Non-root execution**: All containers run as user ID 1000 (non-root)
- **Security contexts**: Comprehensive security policies applied
- **Privilege escalation prevention**: `allowPrivilegeEscalation: false`
- **Capability dropping**: All Linux capabilities dropped
- **Automated security scanning**: CI/CD pipeline includes security checks

## 🏷️ Release Name Strategy

This project implements a comprehensive release name strategy using `app.kubernetes.io/instance` labels for proper resource identification and isolation. Each overlay defines its own unique release name:

| Overlay       | Release Name      | Purpose                                 |
| ------------- | ----------------- | --------------------------------------- |
| `local-base`  | `css-local`       | Local development without PVC           |
| `local-pvc`   | `css-local-pvc`   | Local development with PVC              |
| `with-pvc`    | `css-with-pvc`    | Production-like with persistent storage |
| `without-pvc` | `css-without-pvc` | Stateless deployment                    |

### Benefits

- **Resource Isolation**: Each deployment has unique instance labels
- **Easy Querying**: Find resources by release name using label selectors
- **Kubernetes Best Practices**: Follows recommended labeling conventions
- **Multi-Environment Support**: Deploy multiple instances without conflicts

### Usage Examples

```bash
# Query resources by release name
kubectl get all -l app.kubernetes.io/instance=css-with-pvc

# Deploy specific release
kubectl apply -k overlays/with-pvc

# Find pods for a specific release
kubectl get pods -l app.kubernetes.io/instance=css-local
```

For detailed information, see [Release Name Usage Guide](docs/RELEASE_NAME_USAGE.md).

## 🏷️ Version Management Strategy

This project implements a comprehensive version management strategy that ensures consistency between container image tags and Kubernetes labels across all deployments.

### Key Features

- **Automated Version Updates**: Use Dagger pipelines to update all overlays consistently
- **Version Consistency**: Image tags always match `app.kubernetes.io/version` labels
- **Semantic Versioning**: Support for standard semantic versioning (X.Y.Z) and pre-releases
- **Validation Tools**: Automated checks to ensure version consistency across all overlays

### Version Commands

```bash
# Update all overlays to a specific version
poetry run dagger-pipeline version update 6.1.0

# Preview version changes without applying them
poetry run dagger-pipeline version update 6.1.0 --dry-run

# Generate comprehensive version report
poetry run dagger-pipeline version report

# Validate version consistency across overlays
poetry run dagger-pipeline version validate
```

### Example Version Report

```
📋 Version Report

🏷️ Overlay: local-base
   Instance: css-local
   Image Tag: 6.0.2
   Version Label: 6.0.2
   Status: ✅ Consistent

🏷️ Overlay: with-pvc
   Instance: css-with-pvc
   Image Tag: 6.0.2
   Version Label: 6.0.2
   Status: ✅ Consistent
```

### Version Strategy Benefits

- **Observability**: Query resources by version using label selectors
- **Consistency**: Automated tools prevent version drift between image tags and labels
- **Traceability**: Clear version tracking across all environments
- **Automation**: Reduce manual errors with automated version management

For detailed information, see [Version Strategy Guide](VERSION_STRATEGY.md).

## 🚀 Dagger Automation Pipeline

This project uses [Dagger](https://dagger.io/) for comprehensive automation, replacing traditional shell scripts and GitHub Actions with a modern, containerized pipeline.

### Quick Start

```bash
# Install dependencies
poetry install

# Run all linting and validation (cached for speed)
poetry run dagger-pipeline lint

# Run parallel linting for maximum speed (60-80% faster)
poetry run dagger-pipeline lint-parallel

# Run specific checks
poetry run dagger-pipeline lint --yaml-only
poetry run dagger-pipeline lint --python-only
poetry run dagger-pipeline lint --kustomize-only
poetry run dagger-pipeline lint --security-only

# Generate Kustomize manifests
poetry run dagger-pipeline generate

# Generate all manifests in parallel (4x faster)
poetry run dagger-pipeline generate-parallel

# Run complete CI pipeline
poetry run dagger-pipeline ci

# Set up development environment
poetry run dagger-pipeline setup

# Cache management for optimal performance
poetry run dagger-pipeline cache status
poetry run dagger-pipeline cache clear
```

### Available Pipeline Commands

- **`dagger-pipeline lint`**: Comprehensive linting (YAML, Python, Kustomize, Security)
- **`dagger-pipeline generate`**: Generate Kustomize manifests for all overlays
- **`dagger-pipeline ci`**: Complete CI pipeline (lint + generate + security scan)
- **`dagger-pipeline setup`**: Set up development environment and pre-commit hooks
- **`dagger-pipeline version`**: Version management commands (update, report, validate)

### Dagger Pipeline Features

- **Containerized Execution**: All operations run in isolated containers
- **Cross-platform**: Works consistently across Linux, macOS, and Windows
- **Fast Caching**: Dagger's intelligent caching speeds up repeated operations
- **Parallel Execution**: Multiple pipeline steps can run concurrently
- **Rich Output**: Colored, structured output with progress indicators

### Poetry Tasks (Dagger-based)

```bash
# Dagger pipeline tasks
poetry run poe dagger-lint           # All linting checks
poetry run poe dagger-lint-yaml      # YAML linting only
poetry run poe dagger-lint-python    # Python linting only
poetry run poe dagger-lint-kustomize # Kustomize validation only
poetry run poe dagger-lint-security  # Security scanning only
poetry run poe dagger-generate       # Generate manifests
poetry run poe dagger-ci             # Complete CI pipeline
poetry run poe dagger-setup          # Environment setup
```

### Configuration Files

- **`dagger.json`**: Dagger project configuration
- **`.yamllint.yml`**: YAML linting configuration
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration
- **`pyproject.toml`**: Python dependencies and tool configuration

### CI/CD Pipeline

The project includes a streamlined Dagger-based workflow (`.github/workflows/dagger-ci.yml`) that:

1. **Sets up the environment**: Python, Poetry, and dependencies
1. **Runs the complete Dagger CI pipeline**: All linting, validation, generation, and security checks
1. **Uploads artifacts**: Generated Kubernetes manifests
1. **Builds and deploys documentation**: Automatically publishes to GitHub Pages (when not in local development mode)

#### LOCAL_DEV Environment Flag

The CI pipeline supports a `LOCAL_DEV` environment variable to control documentation publishing:

- **When `LOCAL_DEV` is NOT set** (default): Documentation is built and published to GitHub Pages on main branch pushes
- **When `LOCAL_DEV` is set to `'true'`**: Documentation building and publishing is skipped (useful for development/testing)

##### Setting up LOCAL_DEV

To configure the LOCAL_DEV flag in your GitHub repository:

1. Go to your repository **Settings** → **Secrets and variables** → **Actions**
1. Click on the **Variables** tab
1. Click **New repository variable**
1. Set **Name**: `LOCAL_DEV`
1. Set **Value**: `true` (to disable documentation publishing) or leave unset/`false` (to enable publishing)

##### Documentation Publishing Behavior

```yaml
# When LOCAL_DEV is not set or false (default behavior):
- Documentation is built using MkDocs
- Published to GitHub Pages on main branch pushes
- Available at: https://your-username.github.io/css-kustomize

# When LOCAL_DEV is set to 'true':
- Documentation building is skipped
- No GitHub Pages deployment occurs
- Useful for development branches or testing
```

##### Local Documentation Development

For local documentation development:

```bash
# Install documentation dependencies
poetry install --with docs

# Serve documentation locally
poetry run mkdocs serve

# Build documentation locally
poetry run mkdocs build

# View built documentation
open site/index.html
```

The documentation is automatically built from the `docs/` directory using MkDocs Material theme and includes:

- **Getting Started Guide**: Installation, quick start, and configuration
- **User Guide**: CLI commands, Kustomize overlays, release names, and version management
- **Developer Guide**: Architecture, Dagger pipeline, caching strategy, and contributing
- **Examples**: Basic usage, advanced workflows, and CI/CD integration

## 💾 Storage Options

The Community Solid Server can be deployed with two storage configurations:

### Ephemeral Storage (Default)

Uses Kubernetes `emptyDir` volumes that are deleted when the pod is removed. Suitable for testing and development.

```bash
# Deploy with ephemeral storage
kubectl kustomize overlays/without-pvc/ | kubectl apply -f -
```

### Persistent Storage (Optional)

Uses Kubernetes Persistent Volume Claims (PVC) to retain data across pod restarts and deployments.

```bash
# Deploy with persistent storage
kubectl kustomize overlays/with-pvc/ | kubectl apply -f -
```

### PVC Component Details

The PVC component (`components/pvc/`) provides:

- **1Gi storage** by default (configurable in `components/pvc/pvc.yaml`)
- **ReadWriteOnce** access mode
- **Automatic replacement** of emptyDir with PVC mount

To customize storage size:

```yaml
# components/pvc/pvc.yaml
spec:
  resources:
    requests:
      storage: 5Gi  # Change as needed
```

## 🔧 Manual Kustomize Usage

### Generate Base Manifests

```bash
kubectl kustomize base/
```

### Generate Overlay Manifests

```bash
# Ephemeral storage (emptyDir)
kubectl kustomize overlays/without-pvc/ > manifests/without-pvc.yaml

# Persistent storage (PVC)
kubectl kustomize overlays/with-pvc/ > manifests/with-pvc.yaml

# Legacy PVC overlay (deprecated)
kubectl kustomize overlays/local-pvc/ > manifests/local-pvc.yaml
```

### Apply to Kubernetes

```bash
# Apply base configuration (ephemeral storage)
kubectl kustomize base/ | kubectl apply -f -

# Apply with persistent storage
kubectl kustomize overlays/with-pvc/ | kubectl apply -f -

# Apply with ephemeral storage (explicit)
kubectl kustomize overlays/without-pvc/ | kubectl apply -f -
```

## 🛠️ Development

### Adding New Overlays

1. Create a new directory under `overlays/`
1. Add `kustomization.yaml` with base reference
1. Add any patches or additional resources
1. The Dagger pipeline will automatically detect and process new overlays

### Testing Changes

Before committing:

```bash
# Run comprehensive testing with Dagger
poetry run dagger-pipeline ci

# Test specific components
poetry run dagger-pipeline lint --kustomize-only
poetry run dagger-pipeline generate --overlay your-overlay-name
```

### Local Development Workflow

```bash
# Set up development environment
poetry run dagger-pipeline setup

# Make changes to manifests or overlays
# ...

# Validate changes
poetry run dagger-pipeline lint

# Generate and test manifests
poetry run dagger-pipeline generate

# Run security scan
poetry run dagger-pipeline lint --security-only
```

## 📦 Deployment

### Prerequisites

- Kubernetes cluster
- `kubectl` configured
- `kustomize` installed

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace solid

# Deploy with local PVC overlay
kustomize build overlays/local-pvc/ | kubectl apply -f -

# Check deployment
kubectl get pods -n solid
kubectl get svc -n solid
```

## 🔍 Troubleshooting

### Common Issues

1. **Dagger fails to run**: Ensure Docker is running and accessible
1. **Poetry dependency issues**: Run `poetry install` to ensure all dependencies are installed
1. **Container build failures**: Check Docker daemon status and available disk space
1. **Permission errors**: Ensure Docker daemon is accessible to your user

### Debugging

```bash
# Check generated manifests
cat manifests/local-pvc.yaml

# Validate Kubernetes resources
kubectl --dry-run=client apply -f manifests/local-pvc.yaml

# Run Dagger pipeline with verbose output
poetry run dagger-pipeline lint --verbose

# Check Dagger configuration
cat dagger.json

# Test individual pipeline components
poetry run dagger-pipeline lint --yaml-only --verbose
```

### Performance Tips

- **Docker layer caching**: Dagger automatically caches container layers for faster builds
- **Parallel execution**: Use `poetry run dagger-pipeline ci` for optimal performance
- **Incremental builds**: Only changed components will be rebuilt

## 📚 Resources

- [Dagger Documentation](https://docs.dagger.io/)
- [Kustomize Documentation](https://kustomize.io/)
- [Community Solid Server](https://github.com/CommunitySolidServer/CommunitySolidServer)
- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [Poetry Documentation](https://python-poetry.org/docs/)
