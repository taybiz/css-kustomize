# Quick Start

Get up and running with CSS Kustomize in just a few minutes.

## Prerequisites

- Python 3.11+
- Poetry
- Docker
- kubectl

See the [Installation Guide](installation.md) for detailed setup instructions.

## Basic Usage

1. **Clone and setup**:

   ```bash
   git clone https://github.com/your-org/css-kustomize.git
   cd css-kustomize
   poetry install
   ```

1. **Run the CI pipeline**:

   ```bash
   poetry run dagger-pipeline ci --verbose
   ```

1. **Generate manifests**:

   ```bash
   poetry run dagger-pipeline generate manifests/
   ```

1. **Deploy to Kubernetes**:

   ```bash
   kubectl apply -f manifests/with-pvc.yaml
   ```

## Next Steps

- Read the [CLI Commands](../user-guide/cli-commands.md) guide
- Explore [Kustomize Overlays](../user-guide/kustomize-overlays.md)
- Check out [Examples](../examples/basic-usage.md)
