# CLI Commands

The CSS Kustomize project provides a comprehensive command-line interface through the `dagger-pipeline` command. This page documents all available commands, their options, and usage examples.

## Overview

The CLI is built using Click and provides rich output with colors, progress indicators, and detailed error messages. All commands support a `--verbose` flag for detailed debugging output.

```bash
poetry run dagger-pipeline --help
```

## Global Options

All commands support these global options:

- `--verbose` / `-v`: Enable verbose output with detailed logging
- `--help`: Show help message and exit

## Commands Reference

### `lint` - Code Quality Checks

Run various linting and formatting checks on the codebase.

```bash
poetry run dagger-pipeline lint [OPTIONS]
```

#### Options

- `--yaml` / `--no-yaml`: Run YAML linting with yamllint (default: enabled)
- `--python` / `--no-python`: Run Python linting with ruff (default: enabled)
- `--markdown` / `--no-markdown`: Run Markdown formatting checks (default: enabled)
- `--parallel` / `--no-parallel`: Run linting checks in parallel (default: sequential)

#### Examples

```bash
# Run all linting checks
poetry run dagger-pipeline lint

# Run only YAML linting
poetry run dagger-pipeline lint --yaml --no-python --no-markdown

# Run with verbose output
poetry run dagger-pipeline lint --verbose

# Run in parallel for faster execution
poetry run dagger-pipeline lint --parallel
```

### `validate` - Kustomize Validation

Validate Kustomize configurations for all overlays.

```bash
poetry run dagger-pipeline validate [OPTIONS]
```

#### Examples

```bash
# Validate all overlays
poetry run dagger-pipeline validate

# Validate with verbose output
poetry run dagger-pipeline validate --verbose
```

### `generate` - Generate Manifests

Generate Kubernetes manifests for all overlays.

```bash
poetry run dagger-pipeline generate [OPTIONS] OUTPUT_DIR
```

#### Arguments

- `OUTPUT_DIR`: Directory where generated manifests will be saved

#### Options

- `--parallel` / `--no-parallel`: Generate manifests in parallel (default: sequential)

#### Examples

```bash
# Generate all manifests
poetry run dagger-pipeline generate manifests/

# Generate with parallel execution
poetry run dagger-pipeline generate --parallel manifests/

# Generate to custom directory
poetry run dagger-pipeline generate /tmp/k8s-manifests/
```

### `generate-overlay` - Generate Single Overlay

Generate manifest for a specific overlay.

```bash
poetry run dagger-pipeline generate-overlay [OPTIONS] OVERLAY_NAME OUTPUT_PATH
```

#### Arguments

- `OVERLAY_NAME`: Name of the overlay to generate (e.g., `with-pvc`, `local-base`)
- `OUTPUT_PATH`: Path where the generated manifest will be saved

#### Examples

```bash
# Generate specific overlay
poetry run dagger-pipeline generate-overlay with-pvc manifests/with-pvc.yaml

# Generate local development overlay
poetry run dagger-pipeline generate-overlay local-base /tmp/local.yaml
```

### `security-scan` - Security Scanning

Run security checks on Kustomize configurations.

```bash
poetry run dagger-pipeline security-scan [OPTIONS]
```

#### Examples

```bash
# Scan all overlays for security issues
poetry run dagger-pipeline security-scan

# Scan with verbose output
poetry run dagger-pipeline security-scan --verbose
```

### `security-scan-generated` - Scan Generated Manifests

Run security checks on previously generated manifest files.

```bash
poetry run dagger-pipeline security-scan-generated [OPTIONS] MANIFESTS_DIR
```

#### Arguments

- `MANIFESTS_DIR`: Directory containing generated manifest files

#### Examples

```bash
# Scan generated manifests
poetry run dagger-pipeline security-scan-generated manifests/

# Scan with verbose output
poetry run dagger-pipeline security-scan-generated --verbose manifests/
```

### `update-version` - Update Version

Update the version across all overlays (image tags and labels).

```bash
poetry run dagger-pipeline update-version [OPTIONS] VERSION
```

#### Arguments

- `VERSION`: Semantic version to update to (e.g., `6.0.3`, `6.1.0-beta.1`)

#### Options

- `--dry-run`: Show what would be changed without making actual changes

#### Examples

```bash
# Update to new version
poetry run dagger-pipeline update-version 6.0.3

# Preview changes without applying
poetry run dagger-pipeline update-version --dry-run 6.1.0

# Update with verbose output
poetry run dagger-pipeline update-version --verbose 6.0.3
```

### `update-overlay-version` - Update Single Overlay

Update version for a specific overlay only.

```bash
poetry run dagger-pipeline update-overlay-version [OPTIONS] OVERLAY_NAME VERSION
```

#### Arguments

- `OVERLAY_NAME`: Name of the overlay to update
- `VERSION`: Semantic version to update to

#### Options

- `--dry-run`: Show what would be changed without making actual changes

#### Examples

```bash
# Update specific overlay
poetry run dagger-pipeline update-overlay-version with-pvc 6.0.3

# Preview changes
poetry run dagger-pipeline update-overlay-version --dry-run local-base 6.1.0
```

### `version-report` - Version Report

Generate a report showing current versions across all overlays.

```bash
poetry run dagger-pipeline version-report [OPTIONS]
```

#### Examples

```bash
# Show version report
poetry run dagger-pipeline version-report

# Show with verbose details
poetry run dagger-pipeline version-report --verbose
```

### `validate-versions` - Validate Version Consistency

Check that image tags match version labels across all overlays.

```bash
poetry run dagger-pipeline validate-versions [OPTIONS]
```

#### Examples

```bash
# Validate version consistency
poetry run dagger-pipeline validate-versions

# Validate with verbose output
poetry run dagger-pipeline validate-versions --verbose
```

### `ci` - Complete CI Pipeline

Run the complete CI/CD pipeline including all linting, validation, generation, and security scanning.

```bash
poetry run dagger-pipeline ci [OPTIONS]
```

#### Options

- `--parallel` / `--no-parallel`: Run operations in parallel where possible (default: sequential)

#### Examples

```bash
# Run complete CI pipeline
poetry run dagger-pipeline ci

# Run with verbose output
poetry run dagger-pipeline ci --verbose

# Run with parallel execution
poetry run dagger-pipeline ci --parallel --verbose
```

### `setup-env` - Setup Development Environment

Set up the development environment with pre-commit hooks and dependencies.

```bash
poetry run dagger-pipeline setup-env [OPTIONS]
```

#### Examples

```bash
# Setup development environment
poetry run dagger-pipeline setup-env

# Setup with verbose output
poetry run dagger-pipeline setup-env --verbose
```

### `pre-commit` - Run Pre-commit Hooks

Execute pre-commit hooks on all files.

```bash
poetry run dagger-pipeline pre-commit [OPTIONS]
```

#### Examples

```bash
# Run pre-commit hooks
poetry run dagger-pipeline pre-commit

# Run with verbose output
poetry run dagger-pipeline pre-commit --verbose
```

## Common Workflows

### Development Workflow

```bash
# Quick checks during development
poetry run dagger-pipeline lint --yaml --python

# Validate changes
poetry run dagger-pipeline validate

# Generate and test manifests
poetry run dagger-pipeline generate manifests/
poetry run dagger-pipeline security-scan-generated manifests/
```

### Release Workflow

```bash
# Update version across all overlays
poetry run dagger-pipeline update-version 6.0.3

# Validate version consistency
poetry run dagger-pipeline validate-versions

# Run complete CI pipeline
poetry run dagger-pipeline ci --verbose

# Generate final manifests
poetry run dagger-pipeline generate --parallel manifests/
```

### Debugging Workflow

```bash
# Run with maximum verbosity
poetry run dagger-pipeline ci --verbose

# Check specific overlay
poetry run dagger-pipeline generate-overlay with-pvc /tmp/debug.yaml

# Validate single aspect
poetry run dagger-pipeline lint --python-only --verbose
```

## Exit Codes

The CLI uses standard exit codes:

- `0`: Success
- `1`: General error (linting failures, validation errors, etc.)
- `2`: Command line usage error

## Environment Variables

The CLI respects these environment variables:

- `DAGGER_LOG_LEVEL`: Set Dagger logging level (`debug`, `info`, `warn`, `error`)
- `NO_COLOR`: Disable colored output when set to any value
- `FORCE_COLOR`: Force colored output even in non-TTY environments

## Performance Tips

### Use Parallel Execution

For faster execution, use parallel options where available:

```bash
poetry run dagger-pipeline lint --parallel
poetry run dagger-pipeline generate --parallel manifests/
poetry run dagger-pipeline ci --parallel
```

### Selective Operations

Run only what you need during development:

```bash
# Only YAML linting
poetry run dagger-pipeline lint --yaml-only

# Only specific overlay
poetry run dagger-pipeline generate-overlay local-base manifests/local.yaml
```

### Verbose Output for Debugging

Use verbose mode to understand what's happening:

```bash
poetry run dagger-pipeline ci --verbose
```

## Integration with Other Tools

### Pre-commit Integration

```bash
# Install pre-commit hooks
poetry run dagger-pipeline setup-env

# Run hooks manually
poetry run dagger-pipeline pre-commit
```

### CI/CD Integration

```bash
# In CI/CD pipelines
poetry run dagger-pipeline ci --parallel --verbose
```

### IDE Integration

Many IDEs can be configured to run these commands as tasks or build steps. See the [Examples](../examples/cicd-integration.md) section for specific integrations.
