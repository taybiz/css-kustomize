# Basic Usage Examples

Common workflows and usage patterns for CSS Kustomize.

## Quick Start Examples

### 1. Initial Setup

```bash
# Clone and setup
git clone https://github.com/taybiz/css-kustomize.git
cd css-kustomize
poetry install

# Verify installation
poetry run dagger-pipeline --help
```

### 2. Run Complete CI Pipeline

```bash
# Run all checks and validations
poetry run dagger-pipeline ci --verbose
```

### 3. Generate All Manifests

```bash
# Generate manifests for all overlays
poetry run dagger-pipeline generate manifests/

# Check generated files
ls -la manifests/
```

## Development Workflows

### Daily Development

```bash
# Quick linting during development
poetry run dagger-pipeline lint --yaml --python

# Validate Kustomize configurations
poetry run dagger-pipeline validate

# Generate specific overlay for testing
poetry run dagger-pipeline generate-overlay without-pvc /tmp/test.yaml
```

### Pre-commit Workflow

```bash
# Setup pre-commit hooks
poetry run pre-commit install

# Run hooks manually
poetry run pre-commit run --all-files

# Or use the CLI wrapper
poetry run dagger-pipeline pre-commit
```

## Overlay Management

### Working with Specific Overlays

```bash
# Generate local development overlay
poetry run dagger-pipeline generate-overlay without-pvc manifests/local.yaml

# Generate production overlay with PVC
poetry run dagger-pipeline generate-overlay with-pvc manifests/production.yaml

# Validate specific overlay
kubectl kustomize overlays/with-pvc --dry-run=client
```

### Comparing Overlays

```bash
# Generate all overlays
poetry run dagger-pipeline generate manifests/

# Compare differences
diff manifests/with-pvc.yaml manifests/without-pvc.yaml
```

## Version Management

### Updating Versions

```bash
# Check current versions
poetry run dagger-pipeline version-report

# Update to new version (dry run first)
poetry run dagger-pipeline update-version --dry-run 6.0.3

# Apply version update
poetry run dagger-pipeline update-version 6.0.3

# Validate consistency
poetry run dagger-pipeline validate-versions
```

### Single Overlay Version Update

```bash
# Update only development overlay
poetry run dagger-pipeline update-overlay-version without-pvc 6.1.0-beta.1

# Update production overlay
poetry run dagger-pipeline update-overlay-version with-pvc 6.0.3
```

## Security Scanning

### Scanning Configurations

```bash
# Scan Kustomize configurations
poetry run dagger-pipeline security-scan

# Scan generated manifests
poetry run dagger-pipeline generate manifests/
poetry run dagger-pipeline security-scan-generated manifests/
```

### Security Best Practices

```bash
# Always scan before deployment
poetry run dagger-pipeline security-scan --verbose

# Check for common security issues
grep -r "privileged: true" overlays/ || echo "No privileged containers found"
grep -r "runAsRoot: true" overlays/ || echo "No root containers found"
```

## Deployment Examples

### Local Development

```bash
# Generate local overlay
poetry run dagger-pipeline generate-overlay without-pvc manifests/local.yaml

# Deploy to local cluster
kubectl apply -f manifests/local.yaml

# Check deployment
kubectl get pods -l app.kubernetes.io/instance=css-local
```

### Production Deployment

```bash
# Generate production manifest
poetry run dagger-pipeline generate-overlay with-pvc manifests/production.yaml

# Review before deployment
kubectl apply -f manifests/production.yaml --dry-run=client

# Deploy to production
kubectl apply -f manifests/production.yaml

# Monitor deployment
kubectl rollout status deployment/css-with-pvc
```

## Troubleshooting Examples

### Debugging Failed Builds

```bash
# Run with maximum verbosity
poetry run dagger-pipeline ci --verbose

# Check specific component
poetry run dagger-pipeline lint --python-only --verbose

# Validate individual overlay
kubectl kustomize overlays/with-pvc
```

### Fixing Common Issues

```bash
# Fix YAML formatting issues
poetry run dagger-pipeline lint --yaml-only

# Check for version mismatches
poetry run dagger-pipeline validate-versions --verbose

# Regenerate all manifests
rm -rf manifests/
poetry run dagger-pipeline generate manifests/
```

## Integration Examples

### Git Hooks

```bash
# Pre-commit hook
poetry run dagger-pipeline lint --yaml --python

# Pre-push hook
poetry run dagger-pipeline ci
```

### IDE Integration

```json
// VS Code tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "CSS Kustomize: Lint",
      "type": "shell",
      "command": "poetry",
      "args": ["run", "dagger-pipeline", "lint"],
      "group": "build"
    },
    {
      "label": "CSS Kustomize: Generate",
      "type": "shell",
      "command": "poetry",
      "args": ["run", "dagger-pipeline", "generate", "manifests/"],
      "group": "build"
    }
  ]
}
```

## Performance Tips

### Faster Development

```bash
# Run only what you need
poetry run dagger-pipeline lint --yaml-only
poetry run dagger-pipeline generate-overlay without-pvc /tmp/quick-test.yaml

# Use parallel execution
poetry run dagger-pipeline lint --parallel
poetry run dagger-pipeline generate --parallel manifests/
```

### Caching Optimization

```bash
# Warm up caches
poetry run dagger-pipeline lint

# Subsequent runs will be faster
poetry run dagger-pipeline ci
```

## Monitoring and Validation

### Health Checks

```bash
# Validate all configurations
poetry run dagger-pipeline validate

# Check generated manifests
poetry run dagger-pipeline generate manifests/
kubectl apply -f manifests/ --dry-run=client --validate=true
```

### Resource Monitoring

```bash
# Check resource usage after deployment
kubectl top pods -l app.kubernetes.io/name=community-solid-server

# Monitor logs
kubectl logs -l app.kubernetes.io/instance=css-with-pvc -f
```

## Next Steps

- Explore [Advanced Workflows](advanced-workflows.md)
- Learn about [CI/CD Integration](cicd-integration.md)
- Read [CLI Commands](../user-guide/cli-commands.md) reference
- Check [Kustomize Overlays](../user-guide/kustomize-overlays.md) guide
