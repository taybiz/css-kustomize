# Kustomize Patterns

## Base + Overlay Pattern

The project follows the standard Kustomize base + overlay pattern for configuration management.

### Base Configuration

- Contains common Kubernetes resources (deployment, service)
- Defines default values and configurations
- Should be environment-agnostic

### Overlay Structure

```
overlays/
├── local-pvc/          # Local development with PVC
│   ├── kustomization.yaml
│   ├── deployment-patch.yaml
│   └── pvc.yaml
└── [future-env]/       # Additional environments
```

### Best Practices

1. **Keep base minimal**: Only include resources common to all environments
1. **Use patches strategically**: Prefer strategic merge patches over JSON patches
1. **Environment isolation**: Each overlay should be self-contained
1. **Resource naming**: Use consistent naming conventions across environments

## Configuration Management Patterns

### Resource Patching

- Use `patchesStrategicMerge` for complex modifications
- Use `patches` with target selectors for specific changes
- Avoid direct resource replacement when possible

### Secret Management

- Never commit secrets to version control
- Use external secret management tools
- Consider sealed-secrets or external-secrets operators

### Image Management

- Use image tags in overlays, not base
- Consider using image digests for production
- Implement proper image promotion workflows

## Anti-Patterns to Avoid

- Duplicating entire resources across overlays
- Hard-coding environment-specific values in base
- Using complex transformations that obscure intent
- Mixing configuration concerns in single patches
