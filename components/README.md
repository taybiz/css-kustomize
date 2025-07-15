# Kustomize Components

This directory contains reusable Kustomize components that can be mixed and matched to create different deployment configurations for the Community Solid Server.

## Available Components

### Storage Components

#### `pvc/`

Replaces the default `emptyDir` storage with a Persistent Volume Claim for data persistence across pod restarts.

**Features:**

- 1Gi storage by default (configurable)
- ReadWriteOnce access mode
- Automatic replacement of emptyDir with PVC mount

**Usage:**

```yaml
components:
  - ../../components/pvc
```

### Networking Components

#### `ingress/`

Adds Kubernetes Ingress support for external access with SSL/TLS capabilities.

**Features:**

- NGINX ingress controller support
- SSL/TLS termination
- Configurable host and path
- Cert-manager integration ready
- Updates base URL for ingress access

**Usage:**

```yaml
components:
  - ../../components/ingress
```

#### `nodeport-service/`

Changes the service type from ClusterIP to NodePort for direct node access.

**Features:**

- NodePort service type
- Fixed port 30080 (configurable)
- Suitable for development and testing

**Usage:**

```yaml
components:
  - ../../components/nodeport-service
```

#### `metallb-loadbalancer/`

Configures the service to use MetalLB LoadBalancer for external access with a fixed IP address.

**Features:**

- LoadBalancer service type with MetalLB
- Fixed IP address assignment (192.168.1.81)
- MetalLB annotations for shared IP configuration
- Suitable for bare-metal Kubernetes clusters

**Usage:**

```yaml
components:
  - ../../components/metallb-loadbalancer
```

### Performance Components

#### `multithreading/`

Enables Community Solid Server multithreading with worker processes.

**Features:**

- Configurable worker count (default: num_cores-1)
- Enhanced resource limits for multi-core usage
- Performance-optimized settings

**Usage:**

```yaml
components:
  - ../../components/multithreading
```

### Configuration Components

#### `custom-config/`

Provides custom Community Solid Server configuration via ConfigMap.

**Features:**

- Custom JSON-LD configuration
- ConfigMap-based config injection
- Modular configuration imports
- Volume mount for config files

**Usage:**

```yaml
components:
  - ../../components/custom-config
```

#### `env-vars/`

Adds common environment variables for CSS configuration and performance tuning.

**Features:**

- Logging level configuration
- Performance tuning variables
- CORS settings
- Security configurations
- Node.js optimization flags

**Usage:**

```yaml
components:
  - ../../components/env-vars
```

### Data Access Components

#### `sparql-endpoint/`

Configures Community Solid Server to use SPARQL endpoint backend for GraphQL-like query capabilities.

**Features:**

- SPARQL endpoint configuration
- Support for external SPARQL stores (e.g., Fuseki)
- Environment variables for endpoint URLs
- Enhanced query capabilities

**Usage:**

```yaml
components:
  - ../../components/sparql-endpoint
```

### Security Components

#### `security-hardening/`

Applies enhanced security contexts and hardening measures.

**Features:**

- Read-only root filesystem
- Enhanced security contexts
- AppArmor and seccomp profiles
- Additional temporary volume mounts
- Comprehensive capability dropping

**Usage:**

```yaml
components:
  - ../../components/security-hardening
```

## Component Combinations

Components can be combined to create powerful deployment configurations:

### High-Performance Setup

```yaml
components:
  - ../../components/pvc
  - ../../components/multithreading
  - ../../components/custom-config
  - ../../components/env-vars
  - ../../components/security-hardening
```

### External Access with SPARQL

```yaml
components:
  - ../../components/pvc
  - ../../components/ingress
  - ../../components/sparql-endpoint
  - ../../components/env-vars
```

### Development Environment

```yaml
components:
  - ../../components/nodeport-service
  - ../../components/env-vars
```

### MetalLB LoadBalancer Setup

```yaml
components:
  - ../../components/pvc
  - ../../components/metallb-loadbalancer
  - ../../components/env-vars
```

## Creating Custom Components

To create a new component:

1. Create a new directory under `components/`
1. Add a `kustomization.yaml` file with `kind: Component`
1. Include resources and/or patches as needed
1. Document the component in this README

### Component Structure

```
components/my-component/
├── kustomization.yaml      # Component definition
├── resource.yaml          # Optional: new resources
└── deployment-patch.yaml  # Optional: patches to existing resources
```

### Example Component

```yaml
# components/my-component/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

resources:
  - resource.yaml

patchesStrategicMerge:
  - deployment-patch.yaml
```

## Best Practices

1. **Single Responsibility**: Each component should have a focused purpose
1. **Composability**: Components should work well together
1. **Documentation**: Always document component features and usage
1. **Testing**: Test components in isolation and in combination
1. **Versioning**: Consider component compatibility with base resources

## Helm Chart Feature Parity

These components provide feature parity with the official Community Solid Server Helm chart, including:

- ✅ Ingress support with TLS
- ✅ Persistent storage options
- ✅ SPARQL endpoint configuration
- ✅ Multithreading support
- ✅ Custom configuration via ConfigMaps
- ✅ Environment variable configuration
- ✅ NodePort service support
- ✅ MetalLB LoadBalancer support
- ✅ Enhanced security contexts
- ✅ Resource limits and requests
- ✅ Performance optimizations

## Migration from Helm

To migrate from the Helm chart to these Kustomize components:

1. Identify your current Helm values
1. Select appropriate components that match your configuration
1. Create an overlay that combines the needed components
1. Apply any custom patches for your specific requirements
1. Test the deployment in a non-production environment

For detailed migration guidance, see the project documentation.
