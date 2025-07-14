# Kustomize Components

This directory contains optional Kustomize components that can be mixed and matched to customize your Community Solid Server deployment.

## Available Components

### PVC Component (`pvc/`)

The PVC component replaces the default `emptyDir` volume with a Persistent Volume Claim, providing persistent storage that survives pod restarts and deployments.

**Features:**

- 1Gi storage by default (configurable)
- ReadWriteOnce access mode
- Automatic replacement of emptyDir volume

**Usage:**

```yaml
# In your kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base

components:
  - ../../components/pvc
```

**Customization:**
To change the storage size, edit `components/pvc/pvc.yaml`:

```yaml
spec:
  resources:
    requests:
      storage: 5Gi  # Change as needed
```

## Component Architecture

Components in Kustomize are reusable pieces that can be included in multiple overlays. They differ from overlays in that:

- **Components** are reusable building blocks
- **Overlays** are complete deployment configurations
- Components can be mixed and matched in different overlays

## Examples

### Basic Usage with PVC

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: solid-prod

resources:
  - ../../base

components:
  - ../../components/pvc
```

### Advanced Usage with Multiple Customizations

```yaml
# overlays/staging/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: solid-staging

resources:
  - ../../base

components:
  - ../../components/pvc

# Add custom labels
labels:
  environment: staging
  team: platform

# Add resource limits
patches:
  - patch: |-
      - op: add
        path: /spec/template/spec/containers/0/resources/limits
        value:
          cpu: "1000m"
          memory: "1Gi"
    target:
      kind: Deployment
      name: community-solid-server
```

## Testing Components

Test your component configurations:

```bash
# Test with PVC component
kubectl kustomize overlays/with-pvc/

# Test without PVC component
kubectl kustomize overlays/without-pvc/

# Test custom overlay
kubectl kustomize examples/custom-overlay-with-pvc/
```

## Adding New Components

To add a new component:

1. Create a new directory under `components/`
1. Add a `kustomization.yaml` with `kind: Component`
1. Include any resources and patches needed
1. Use `apiVersion: kustomize.config.k8s.io/v1alpha1` for components

Example structure:

```
components/
└── my-component/
    ├── kustomization.yaml
    ├── resource.yaml
    └── patch.yaml
```
