# Version Management

Learn how to manage versions across CSS Kustomize overlays and deployments.

## Overview

CSS Kustomize provides comprehensive version management capabilities to ensure consistency across all overlays and deployments.

## Version Strategy

### Semantic Versioning

The project follows semantic versioning (SemVer) for Community Solid Server versions:

- `MAJOR.MINOR.PATCH` (e.g., `6.0.3`)
- Pre-release versions: `6.1.0-beta.1`

### Version Consistency

All overlays maintain consistent versions across:

- Container image tags
- Kubernetes labels (`app.kubernetes.io/version`)
- Documentation references

## CLI Commands

### Update All Overlays

```bash
# Update version across all overlays
poetry run dagger-pipeline update-version 6.0.3

# Preview changes without applying
poetry run dagger-pipeline update-version --dry-run 6.1.0
```

### Update Single Overlay

```bash
# Update specific overlay only
poetry run dagger-pipeline update-overlay-version with-pvc 6.0.3

# Preview changes for single overlay
poetry run dagger-pipeline update-overlay-version --dry-run local-base 6.1.0
```

### Version Reporting

```bash
# Show current versions across all overlays
poetry run dagger-pipeline version-report

# Validate version consistency
poetry run dagger-pipeline validate-versions
```

## Version Locations

### Image Tags

Container image versions are specified in overlay patches:

```yaml
# overlays/with-pvc/kustomization.yaml
images:
  - name: solidproject/community-server
    newTag: "6.0.3"
```

### Kubernetes Labels

Version labels are applied automatically:

```yaml
labels:
  - includeSelectors: false
    pairs:
      app.kubernetes.io/version: "6.0.3"
```

### Documentation

Version references in documentation are updated automatically during version updates.

## Best Practices

### Before Updating

1. **Check current versions**:

   ```bash
   poetry run dagger-pipeline version-report
   ```

1. **Validate consistency**:

   ```bash
   poetry run dagger-pipeline validate-versions
   ```

### During Updates

1. **Use dry-run first**:

   ```bash
   poetry run dagger-pipeline update-version --dry-run 6.0.3
   ```

1. **Update incrementally** for major changes

1. **Test after updates**:

   ```bash
   poetry run dagger-pipeline ci --verbose
   ```

### After Updates

1. **Validate changes**:

   ```bash
   poetry run dagger-pipeline validate-versions
   ```

1. **Generate manifests**:

   ```bash
   poetry run dagger-pipeline generate manifests/
   ```

1. **Test deployments** in development environment

## Troubleshooting

### Version Mismatches

If versions are inconsistent:

```bash
# Check what's wrong
poetry run dagger-pipeline validate-versions --verbose

# Fix automatically
poetry run dagger-pipeline update-version $(current-version)
```

### Rollback Changes

To rollback version changes:

```bash
# Use git to revert
git checkout -- overlays/

# Or update to previous version
poetry run dagger-pipeline update-version 6.0.2
```

## Integration

### CI/CD Pipelines

Include version validation in CI:

```bash
# In CI pipeline
poetry run dagger-pipeline validate-versions
poetry run dagger-pipeline ci
```

### Release Workflows

Typical release workflow:

```bash
# 1. Update version
poetry run dagger-pipeline update-version 6.0.3

# 2. Validate and test
poetry run dagger-pipeline validate-versions
poetry run dagger-pipeline ci --verbose

# 3. Generate final manifests
poetry run dagger-pipeline generate manifests/

# 4. Commit and tag
git add .
git commit -m "Release 6.0.3"
git tag v6.0.3
```

## Next Steps

- Learn about [Release Names](release-names.md)
- Explore [CLI Commands](cli-commands.md)
- Check [Examples](../examples/basic-usage.md)
