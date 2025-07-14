# Release Name Strategy for app.kubernetes.io/instance

## Overview

This strategy implements consistent `app.kubernetes.io/instance` labeling across all Kubernetes resources using Kustomize's native capabilities for parameterization and label management.

## Strategy Components

### 1. Base Layer Standardization

- Remove hardcoded `release-name` from base resources
- Use placeholder values that will be replaced by overlays
- Ensure all resources have consistent label structure

### 2. Overlay-Specific Release Names

- Each overlay defines its own release name
- Use Kustomize's `labels` and `labelSelectors` for consistency
- Support environment-specific naming (dev, staging, prod)

### 3. Component Integration

- Ensure components inherit release names from parent overlays
- Maintain label consistency across patched resources

### 4. Validation and Testing

- Automated validation of label consistency
- Test manifests to verify proper release name propagation

## Implementation Approach

### Phase 1: Base Resource Cleanup

1. Update base/deployment.yaml to use placeholder or remove hardcoded instance
1. Add missing app.kubernetes.io/instance to base/service.yaml
1. Update components/pvc/pvc.yaml with instance label

### Phase 2: Overlay Configuration

1. Configure each overlay with appropriate release names:
   - `local-base`: `css-local`
   - `local-pvc`: `css-local-pvc`
   - `with-pvc`: `css-with-pvc`
   - `without-pvc`: `css-without-pvc`

### Phase 3: Kustomization Enhancement

1. Use `labels` in overlays to apply instance labels
1. Ensure `labelSelectors` are updated for services
1. Test manifest generation for each overlay

### Phase 4: Automation Integration

1. Add validation to Dagger pipeline
1. Ensure linting covers label consistency
1. Document usage patterns

## Benefits

- **Consistency**: All resources have proper instance labeling
- **Flexibility**: Each overlay can define its own release name
- **Maintainability**: Centralized label management through Kustomize
- **Compliance**: Follows Kubernetes labeling best practices
- **Automation**: Integrated with existing linting and validation

## Usage Examples

```bash
# Generate manifests with proper instance labels
kustomize build overlays/local-base
kustomize build overlays/with-pvc

# Validate label consistency
./scripts/lint.sh --yaml-only
```

## Next Steps

1. Implement base resource updates
1. Configure overlay-specific release names
1. Test manifest generation
1. Update documentation
1. Integrate with CI/CD pipeline
