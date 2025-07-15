# Kustomize Overlays

Learn how to work with Kustomize overlays in the CSS Kustomize project.

## Overview

This project uses Kustomize overlays to manage environment-specific configurations for the Community Solid Server.

## Available Overlays

### `with-pvc`

- **Purpose**: Production-like deployment
- **Release Name**: `css-with-pvc`
- **Storage**: PersistentVolumeClaim
- **Use Case**: Production deployments requiring persistence

### `without-pvc`

- **Purpose**: Stateless deployment
- **Release Name**: `css-without-pvc`
- **Storage**: None
- **Use Case**: Stateless production deployments

## Working with Overlays

### Building Manifests

```bash
# Build specific overlay
kubectl kustomize overlays/with-pvc

# Generate to file
kubectl kustomize overlays/with-pvc > manifests/with-pvc.yaml
```

### Using the CLI

```bash
# Generate all overlays
poetry run dagger-pipeline generate manifests/

# Generate specific overlay
poetry run dagger-pipeline generate-overlay with-pvc manifests/with-pvc.yaml
```

## Customization

### Adding New Overlays

1. Create new directory in `overlays/`
1. Add `kustomization.yaml`
1. Configure patches and resources
1. Update CLI to include new overlay

### Modifying Existing Overlays

Edit the `kustomization.yaml` files to customize:

- Resource patches
- ConfigMap generators
- Label transformers
- Name prefixes/suffixes

## Next Steps

- Explore [Version Management](version-management.md)
- Check [CLI Commands](cli-commands.md)
