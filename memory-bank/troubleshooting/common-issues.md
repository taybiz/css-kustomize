# Common Issues and Solutions

## Linting Issues

### YAML Linting Failures

**Problem**: yamllint fails with line length or truthy value errors

```
line too long (82 > 80 characters)
truthy value should be one of [false, true]
```

**Solution**:

1. Check `.yamllint.yml` configuration
1. Ensure line-length is set to reasonable value (120)
1. Allow truthy values for Kubernetes manifests

```yaml
rules:
  line-length:
    max: 120
  truthy:
    allowed-values: ['true', 'false', 'yes', 'no']
```

### Python Linting with Ruff

**Problem**: Ruff reports import sorting or formatting issues

**Solution**:

1. Use ruff's auto-fix capabilities: `ruff check --fix`
1. Configure ruff in pyproject.toml for project needs
1. Run ruff format for consistent formatting

## Dagger Pipeline Issues

### Container Build Failures

**Problem**: Pipeline fails during container setup

**Symptoms**:

- "Failed to pull image" errors
- Dependency installation timeouts
- Permission denied errors

**Solutions**:

1. Check internet connectivity
1. Verify base image availability
1. Use specific image tags, not 'latest'
1. Implement retry logic for network operations

### Mount Path Issues

**Problem**: Files not found in container

**Solution**:

```python
# Correct: Mount as directory
container = container.with_directory("/src", source_dir)

# Incorrect: Mount as file
container = container.with_file("/src/file.py", source_file)
```

## Kustomize Issues

### Resource Not Found

**Problem**: `kustomize build` fails with "resource not found"

**Common Causes**:

1. Incorrect file paths in kustomization.yaml
1. Missing base resources
1. Typos in resource names

**Solution**:

1. Verify all paths are relative to kustomization.yaml
1. Check file existence and spelling
1. Use `kustomize build --enable-alpha-plugins` if needed

### Patch Application Failures

**Problem**: Strategic merge patches don't apply correctly

**Debugging Steps**:

1. Validate YAML syntax
1. Check patch target selectors
1. Verify resource structure matches base
1. Use `kubectl explain` to understand resource schema

## Development Environment

### Poetry Issues

**Problem**: Dependency conflicts or installation failures

**Solutions**:

1. Clear poetry cache: `poetry cache clear --all pypi`
1. Update poetry: `poetry self update`
1. Recreate virtual environment: `poetry env remove python && poetry install`

### Pre-commit Hook Failures

**Problem**: Pre-commit hooks fail or skip

**Solutions**:

1. Update hooks: `pre-commit autoupdate`
1. Run manually: `pre-commit run --all-files`
1. Skip temporarily: `git commit --no-verify`

## Security Scanning

### False Positives

**Problem**: Security scanner reports issues that aren't actual vulnerabilities

**Approach**:

1. Analyze the specific finding
1. Determine if it's a false positive
1. Add appropriate exclusions or suppressions
1. Document the decision

### Missing Security Context

**Problem**: Containers running as root or without security context

**Solution**:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```
