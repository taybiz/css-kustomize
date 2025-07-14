# Documentation Versioning Setup

This document explains how version information is included in the GitHub Pages documentation built from MkDocs.

## Implementation

The CSS Kustomize project uses the following approach for documentation versioning:

### 1. Mike for Version Management

- **Tool**: [mike](https://github.com/jimporter/mike) - A utility for managing multiple versions of MkDocs documentation
- **Configuration**: Added to `mkdocs.yml` with `version.provider: mike`
- **Dependency**: Added `mike = "^2.1.0"` to `pyproject.toml` docs dependencies

### 2. Automatic Version Detection

- **Source**: Project version from `pyproject.toml`
- **Method**: Uses `poetry version --short` to get current version
- **Integration**: GitHub Actions workflow automatically deploys with current version

### 3. GitHub Actions Integration

The CI workflow (`.github/workflows/ci.yml`) includes:

```yaml
- name: Get version from pyproject.toml
  id: get_version
  run: |
    VERSION=$(poetry version --short)
    echo "version=$VERSION" >> $GITHUB_OUTPUT

- name: Deploy documentation with mike
  run: |
    poetry run mike deploy --push --update-aliases ${{ steps.get_version.outputs.version }} latest
    poetry run mike set-default --push latest
```

### 4. Dagger Pipeline Integration

The project includes Dagger-based commands for documentation management:

```bash
# Build documentation
poetry run dagger-pipeline docs build

# Serve locally
poetry run dagger-pipeline docs serve

# Deploy with versioning
poetry run dagger-pipeline docs deploy

# List versions
poetry run dagger-pipeline docs list-versions

# Delete version
poetry run dagger-pipeline docs delete-version 1.0.0
```

## Features

### Version Selector

Users can switch between different versions of the documentation using the version selector in the Material theme.

### Version Display

- Current version is displayed in the documentation
- Version information is automatically updated based on `pyproject.toml`
- Each deployment creates a versioned copy of the documentation

### Aliases

- `latest` alias always points to the most recent version
- Custom aliases can be set during deployment
- Default version can be configured

## Usage Examples

### Manual Deployment

```bash
# Deploy current version
poetry run dagger-pipeline docs deploy

# Deploy specific version with alias
poetry run dagger-pipeline docs deploy --version 1.2.3 --alias stable

# Deploy and set as default
poetry run dagger-pipeline docs deploy --version 1.2.3 --set-default
```

### Automatic Deployment

Documentation is automatically deployed when:

- Changes are pushed to the `main` branch
- The CI pipeline completes successfully
- Uses the current project version from `pyproject.toml`

## Benefits

1. **Version History**: Maintain documentation for multiple releases
1. **User Experience**: Users can access version-specific documentation
1. **Automation**: Seamless integration with CI/CD pipeline
1. **Consistency**: Version information stays in sync with project releases
1. **Flexibility**: Support for custom versions and aliases

## File Structure

```
├── mkdocs.yml                 # MkDocs configuration with mike provider
├── pyproject.toml            # Project version source
├── .github/workflows/ci.yml  # Automated deployment
├── dagger_pipeline/
│   ├── main.py              # CLI commands for docs
│   └── pipeline.py          # Dagger implementation
└── docs/
    └── user-guide/
        └── documentation-versioning.md  # User guide
```

This setup provides a robust, automated solution for including version information in GitHub Pages documentation while maintaining multiple versions for different releases.
