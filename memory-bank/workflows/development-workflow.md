# Development Workflow

## Daily Development Process

### 1. Environment Setup

```bash
# Activate poetry environment
poetry shell

# Install/update dependencies
poetry install

# Install pre-commit hooks (first time only)
pre-commit install
```

### 2. Making Changes

1. Create/modify Kubernetes manifests in `base/` or `overlays/`
1. Update Dagger pipeline code if needed
1. Test changes locally before committing

### 3. Validation Pipeline

```bash
# Run full linting pipeline
python -m dagger_pipeline.main

# Run specific checks
python -m dagger_pipeline.main --yaml-only
python -m dagger_pipeline.main --python-only
```

### 4. Testing Changes

```bash
# Generate manifests for specific overlay
kustomize build overlays/local-pvc > manifests/local-pvc.yaml

# Validate generated manifests
kubectl apply --dry-run=client -f manifests/local-pvc.yaml
```

### 5. Commit Process

```bash
# Pre-commit hooks run automatically
git add .
git commit -m "feat: add new overlay configuration"

# Push changes
git push origin main
```

## Release Workflow

### 1. Version Management

- Update version in pyproject.toml
- Tag releases with semantic versioning
- Update CHANGELOG.md with release notes

### 2. Manifest Generation

```bash
# Generate all overlay manifests
for overlay in overlays/*/; do
    name=$(basename "$overlay")
    kustomize build "$overlay" > "manifests/${name}.yaml"
done
```

### 3. Deployment Validation

- Run security scans on generated manifests
- Validate against target cluster policies
- Test in staging environment first

## Maintenance Workflow

### Weekly Tasks

- Update dependencies: `poetry update`
- Run security audits: `poetry audit`
- Update pre-commit hooks: `pre-commit autoupdate`

### Monthly Tasks

- Review and update linting configurations
- Audit generated manifests for security compliance
- Update base images and tool versions

## Emergency Procedures

### Rollback Process

1. Identify last known good configuration
1. Revert to previous git commit
1. Regenerate and redeploy manifests
1. Validate system functionality

### Hotfix Workflow

1. Create hotfix branch from main
1. Make minimal necessary changes
1. Run abbreviated validation pipeline
1. Fast-track through review process
1. Deploy and monitor closely

## Collaboration Guidelines

### Code Review Process

- All changes require peer review
- Focus on security implications
- Validate linting pipeline passes
- Test manifest generation

### Documentation Updates

- Update memory bank when adding new patterns
- Document architectural decisions
- Keep troubleshooting guide current
- Update workflow documentation as processes evolve
