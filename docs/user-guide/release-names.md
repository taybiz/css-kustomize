# Release Name Usage Guide

## Overview

This project implements a comprehensive release name strategy using `app.kubernetes.io/instance` labels across all Kubernetes resources. Each overlay defines its own unique release name, ensuring proper resource identification and isolation.

## Current Release Names

| Overlay       | Release Name      | Purpose                                 |
| ------------- | ----------------- | --------------------------------------- |
| `without-pvc` | `css-local`       | Local development without PVC           |
| `with-pvc`    | `css-with-pvc`    | Local development with PVC              |
| `with-pvc`    | `css-with-pvc`    | Production-like with persistent storage |
| `without-pvc` | `css-without-pvc` | Stateless deployment                    |

## How It Works

### Base Resources

- Base resources (`base/deployment.yaml`, `base/service.yaml`) contain no hardcoded instance labels
- The base `kustomization.yaml` applies common labels like `app.kubernetes.io/name: community-solid-server`

### Overlay Configuration

Each overlay uses `labels` to apply the `app.kubernetes.io/instance` label:

```yaml
labels:
  app.kubernetes.io/instance: css-with-pvc
```

### Automatic Label Propagation

Kustomize automatically applies the instance label to:

- **Metadata labels** on all resources
- **Selectors** in Services (for pod selection)
- **matchLabels** in Deployments (for pod selection)
- **Pod template labels** (for proper identification)

## Generated Manifests

When you build an overlay, all resources will have consistent labeling:

```yaml
# Service
metadata:
  labels:
    app.kubernetes.io/name: community-solid-server
    app.kubernetes.io/instance: css-with-pvc
    app.kubernetes.io/version: "6.0.2"
spec:
  selector:
    app.kubernetes.io/name: community-solid-server
    app.kubernetes.io/instance: css-with-pvc
    app.kubernetes.io/version: "6.0.2"

# Deployment
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: community-solid-server
      app.kubernetes.io/instance: css-with-pvc
      app.kubernetes.io/version: "6.0.2"
  template:
    metadata:
      labels:
        app.kubernetes.io/name: community-solid-server
        app.kubernetes.io/instance: css-with-pvc
        app.kubernetes.io/version: "6.0.2"
```

## Usage Examples

### Building Manifests

```bash
# Build specific overlay
kubectl kustomize overlays/with-pvc

# Apply to cluster
kubectl apply -k overlays/with-pvc

# Generate and save manifests
kubectl kustomize overlays/without-pvc > manifests/without-pvc.yaml
```

### Querying Resources by Release

```bash
# Find all resources for a specific release
kubectl get all -l app.kubernetes.io/instance=css-with-pvc

# Find pods for a specific release
kubectl get pods -l app.kubernetes.io/instance=css-local

# Describe deployment for a specific release
kubectl describe deployment -l app.kubernetes.io/instance=css-without-pvc
```

## Adding New Overlays

To create a new overlay with a custom release name:

1. Create overlay directory:

```bash
mkdir -p overlays/my-environment
```

2. Create `kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: my-namespace

resources:
  - ../../base

labels:
  app.kubernetes.io/instance: css-my-environment
```

3. Test the configuration:

```bash
kubectl kustomize overlays/my-environment
```

## Best Practices

### Release Naming Convention

- Use descriptive, environment-specific names
- Include the `css-` prefix for consistency
- Use lowercase with hyphens (kebab-case)
- Examples: `css-dev`, `css-staging`, `css-prod-us-east`

### Label Consistency

- Always use `labels` in overlays for instance labels
- Ensure all resources inherit the same instance label
- Verify selectors include the instance label for proper isolation

### Validation

```bash
# Validate label consistency across resources
kubectl kustomize overlays/with-pvc | grep -A 5 -B 5 "app.kubernetes.io/instance"

# Check that selectors include instance labels
kubectl kustomize overlays/with-pvc | grep -A 10 "selector:"
```

## Troubleshooting

### Common Issues

1. **Missing instance labels in selectors**

   - Ensure you're using `labels`, not `labels`
   - Verify the overlay kustomization.yaml syntax

1. **Deprecation warnings**

   - The `labels` warnings are informational
   - `labels` provides necessary selector functionality
   - The newer `labels` field doesn't update selectors

1. **Resource conflicts**

   - Different overlays with same release name will conflict
   - Ensure unique instance labels per environment
   - Use namespaces for additional isolation

### Validation Commands

```bash
# Test all overlays
for overlay in overlays/*/; do
  echo "Testing $overlay"
  kubectl kustomize "$overlay" > /dev/null && echo "✓ Valid" || echo "✗ Invalid"
done

# Check for label consistency
kubectl kustomize overlays/with-pvc | yq eval '.metadata.labels."app.kubernetes.io/instance"' -
```

## Integration with CI/CD

The release name strategy integrates with your existing Dagger pipeline:

```python
# Example: Validate release names in pipeline
def validate_release_names(self):
    overlays = ["with-pvc", "without-pvc"]
    for overlay in overlays:
        result = self.container.with_exec([
            "kubectl", "kustomize", f"overlays/{overlay}"
        ]).stdout()
        # Validate that instance labels are present
        assert "app.kubernetes.io/instance" in result
```

This ensures consistent release name application across all environments and deployments.
