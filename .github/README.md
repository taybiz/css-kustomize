# GitHub Actions Workflows

This directory contains simplified GitHub Actions workflows that leverage the Dagger pipeline for all automation tasks.

## Workflows

### CI Pipeline (`ci.yml`)

**Triggers:** Push to main/develop, Pull Requests, Manual dispatch

**What it does:**

- Runs the complete Dagger CI pipeline (`dagger-pipeline ci`)
- Uploads generated Kubernetes manifests as artifacts
- Builds and deploys documentation (main branch only)

**Key command:** `poetry run dagger-pipeline ci --verbose`

### Development (`dev.yml`)

**Triggers:** Manual dispatch only

**What it does:**

- Provides a menu of development tasks to run via Dagger
- Available tasks:
  - `setup` - Environment setup
  - `lint` - Run linting checks
  - `generate` - Generate manifests
  - `ci` - Complete CI pipeline
  - `version-validate` - Validate version consistency
  - `version-report` - Generate version report

**Usage:** Go to Actions → Development → Run workflow → Select task

### Release (`release.yml`)

**Triggers:** Git tags (v\*), Manual dispatch

**What it does:**

- Validates release tag format
- Runs Dagger CI pipeline
- Validates version consistency
- Creates release archives
- Creates GitHub release with artifacts
- Updates documentation

**Key commands:**

- `poetry run dagger-pipeline ci --verbose`
- `poetry run dagger-pipeline version validate --verbose`

### Version Update (`version-update.yml`)

**Triggers:** Manual dispatch only

**What it does:**

- Updates version across overlays using Dagger
- Supports specific overlay updates or all overlays
- Supports dry-run mode
- Commits changes automatically
- Tests updated version with CI pipeline

**Key command:** `poetry run dagger-pipeline version update <version> [--overlay <name>] [--dry-run]`

## Design Philosophy

These workflows follow the project's automation guidelines:

1. **Dagger-First**: All logic is implemented in the Dagger pipeline, not in GitHub Actions
1. **Minimal Duplication**: GitHub Actions only handle environment setup and call Dagger commands
1. **Consistent Interface**: All workflows use the same `dagger-pipeline` CLI commands
1. **Cross-Platform**: Dagger ensures consistent execution across different environments

## Available Dagger Commands

```bash
# Complete CI pipeline
poetry run dagger-pipeline ci --verbose

# Linting
poetry run dagger-pipeline lint

# Manifest generation
poetry run dagger-pipeline generate [--overlay <name>]

# Version management
poetry run dagger-pipeline version update <version> [--overlay <name>] [--dry-run]
poetry run dagger-pipeline version validate
poetry run dagger-pipeline version report

# Environment setup
poetry run dagger-pipeline setup
```

## Migration from Complex Workflows

The previous workflows contained extensive GitHub Actions logic that has been replaced with simple Dagger command calls. This provides:

- **Better maintainability**: Logic is centralized in Python code
- **Local reproducibility**: Same commands work locally and in CI
- **Cross-platform consistency**: Dagger containers ensure identical execution
- **Faster development**: No need to push to test workflow changes
