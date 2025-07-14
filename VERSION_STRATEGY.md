# Version Strategy for CSS Kustomize

## Overview

This document outlines the comprehensive strategy for managing `app.kubernetes.io/version` labels in conjunction with container image tags across all Kubernetes resources in the CSS Kustomize project.

## Core Principles

### 1. Version Consistency

- The `app.kubernetes.io/version` label MUST match the container image tag
- All resources (Deployment, Service, PVC) inherit the same version label
- Version labels are applied to both metadata and pod templates

### 2. Semantic Versioning

- Follow semantic versioning format: `X.Y.Z` or `X.Y.Z-prerelease`
- Examples: `6.0.2`, `6.1.0-beta`, `7.0.0-rc1`
- Development versions use `-dev` suffix: `6.0.2-dev`

### 3. Automation-First Approach

- Version updates are automated using Dagger pipelines
- Manual version updates are discouraged to prevent inconsistencies
- Validation tools ensure version consistency across all overlays

## Implementation Strategy

### Image Tag Management

Each overlay defines the container image version using the `images` field:

```yaml
images:
  - name: docker.io/solidproject/community-server
    newTag: 6.0.2
```

### Version Label Application

Version labels are applied at multiple levels:

#### 1. Overlay-Level Labels

Applied to all resources via the `labels` field:

```yaml
labels:
  - pairs:
      app.kubernetes.io/instance: css-with-pvc
      app.kubernetes.io/version: 6.0.2
```

#### 2. Pod Template Labels

Applied directly to pod templates via JSON patches:

```yaml
patches:
  - target:
      kind: Deployment
      name: community-solid-server
    patch: |-
      - op: add
        path: /spec/template/metadata/labels/app.kubernetes.io~1version
        value: 6.0.2
```

### Selector Strategy

**Important**: Version labels are applied to resource metadata and pod templates, but **NOT** to selectors. This approach provides:

- **Backward Compatibility**: Existing deployments continue to work without selector changes
- **Flexibility**: Allows rolling updates without selector conflicts
- **Observability**: Version tracking through labels without affecting pod selection
- **Best Practices**: Follows Kubernetes recommendations for label usage

### Overlay Configuration

Each overlay follows this pattern:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: solid

resources:
  - ../../base

images:
  - name: docker.io/solidproject/community-server
    newTag: 6.0.2

labels:
  - pairs:
      app.kubernetes.io/instance: css-overlay-name
      app.kubernetes.io/version: 6.0.2

patches:
  - target:
      kind: Service
      name: community-solid-server
    patch: |-
      - op: add
        path: /spec/selector/app.kubernetes.io~1instance
        value: css-overlay-name
  - target:
      kind: Deployment
      name: community-solid-server
    patch: |-
      - op: add
        path: /spec/selector/matchLabels/app.kubernetes.io~1instance
        value: css-overlay-name
      - op: add
        path: /spec/template/metadata/labels/app.kubernetes.io~1instance
        value: css-overlay-name
      - op: add
        path: /spec/template/metadata/labels/app.kubernetes.io~1version
        value: 6.0.2
```

**Note**: Only `app.kubernetes.io/instance` is used in selectors for resource isolation. Version labels are applied to metadata for observability without affecting pod selection.

## Automation Tools

### Version Update Command

Update all overlays to a specific version:

```bash
poetry run dagger-pipeline version update 6.1.0
```

Update with dry-run to preview changes:

```bash
poetry run dagger-pipeline version update 6.1.0 --dry-run
```

### Version Validation

Generate a comprehensive version report:

```bash
poetry run dagger-pipeline version report
```

Validate version consistency:

```bash
poetry run dagger-pipeline version validate
```

### Example Output

```
📋 Version Report
==================================================

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

==================================================
```

## Version Lifecycle Management

### Development Workflow

1. **Development Versions**: Use `-dev` suffix for active development

   ```yaml
   newTag: 6.1.0-dev
   app.kubernetes.io/version: 6.1.0-dev
   ```

1. **Release Candidates**: Use `-rc` suffix for pre-release testing

   ```yaml
   newTag: 6.1.0-rc1
   app.kubernetes.io/version: 6.1.0-rc1
   ```

1. **Production Releases**: Use clean semantic version

   ```yaml
   newTag: 6.1.0
   app.kubernetes.io/version: 6.1.0
   ```

### Version Promotion Process

1. **Update Version**: Use automation tools to update all overlays
1. **Validate Consistency**: Run version validation to ensure consistency
1. **Generate Manifests**: Create updated Kubernetes manifests
1. **Test Deployment**: Validate in staging environment
1. **Production Deployment**: Apply to production clusters

## Monitoring and Observability

### Label-Based Queries

Query resources by version:

```bash
kubectl get pods -l app.kubernetes.io/version=6.0.2
kubectl get deployments -l app.kubernetes.io/version=6.0.2
kubectl get services -l app.kubernetes.io/version=6.0.2
```

Query by instance and version:

```bash
kubectl get all -l app.kubernetes.io/instance=css-with-pvc,app.kubernetes.io/version=6.0.2
```

### Version Tracking

Monitor version distribution across environments:

```bash
kubectl get deployments -o custom-columns=NAME:.metadata.name,VERSION:.metadata.labels.app\.kubernetes\.io/version
```

## Best Practices

### 1. Consistency Enforcement

- Always use automation tools for version updates
- Run validation after any manual changes
- Include version validation in CI/CD pipelines

### 2. Version Naming

- Use semantic versioning for all releases
- Include meaningful suffixes for pre-releases
- Avoid arbitrary or date-based version numbers

### 3. Documentation

- Document version changes in release notes
- Maintain version history in git tags
- Update deployment documentation with version requirements

### 4. Testing Strategy

- Test version updates in staging environments
- Validate label propagation in generated manifests
- Verify monitoring and observability with new versions

## Troubleshooting

### Common Issues

#### Version Mismatch

**Problem**: Image tag doesn't match version label
**Solution**: Run `poetry run dagger-pipeline version update <version>` to synchronize

#### Missing Version Labels

**Problem**: Some resources lack version labels
**Solution**: Ensure all overlays include version patches for pod templates

#### Inconsistent Versions

**Problem**: Different overlays have different versions
**Solution**: Use `poetry run dagger-pipeline version report` to identify and fix inconsistencies

### Validation Commands

Check for version consistency:

```bash
poetry run dagger-pipeline version validate
```

Generate detailed version report:

```bash
poetry run dagger-pipeline version report
```

Dry-run version update:

```bash
poetry run dagger-pipeline version update <version> --dry-run
```

## Integration with Release Management

### Git Workflow

1. Create feature branch for version updates
1. Run version update automation
1. Commit changes with descriptive message
1. Create pull request with version validation results
1. Tag release after merge

### CI/CD Integration

- Include version validation in pipeline checks
- Automate manifest generation after version updates
- Deploy to staging for version validation
- Promote to production after successful validation

## Future Enhancements

### Planned Features

- Automatic version detection from git tags
- Integration with container registry for version validation
- Support for multi-container version management
- Advanced rollback capabilities

### Monitoring Improvements

- Prometheus metrics for version tracking
- Grafana dashboards for version distribution
- Alerting for version inconsistencies
- Automated version drift detection

## Conclusion

This version strategy ensures consistent, automated, and observable version management across all CSS Kustomize deployments. By following these guidelines and using the provided automation tools, teams can maintain reliable version tracking while minimizing manual errors and inconsistencies.
