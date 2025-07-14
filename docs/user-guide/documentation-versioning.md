# Documentation Versioning

This guide explains how to manage versioned documentation for the CSS Kustomize project using MkDocs and mike.

## Overview

The CSS Kustomize project uses [mike](https://github.com/jimporter/mike) for versioned documentation deployment. This allows you to:

- Deploy multiple versions of documentation simultaneously
- Maintain documentation for different releases
- Set default versions and aliases
- Provide users with version-specific documentation

## Version Management

### Automatic Versioning

The documentation version is automatically derived from the project version in `pyproject.toml`. When you deploy documentation, it will use the current project version unless explicitly specified.

### Manual Version Deployment

You can deploy documentation for a specific version:

```bash
# Deploy current project version
poetry run dagger-pipeline docs deploy

# Deploy specific version with alias
poetry run dagger-pipeline docs deploy --version 1.2.3 --alias stable

# Deploy and set as default
poetry run dagger-pipeline docs deploy --version 1.2.3 --set-default
```

## Available Commands

### Build Documentation

Build documentation locally for testing:

```bash
poetry run dagger-pipeline docs build
```

This creates a `site/` directory with the built documentation.

### Serve Documentation

Serve documentation locally for development:

```bash
# Serve on default port 8000
poetry run dagger-pipeline docs serve

# Serve on custom port
poetry run dagger-pipeline docs serve --port 3000
```

### Deploy Documentation

Deploy versioned documentation to GitHub Pages:

```bash
# Deploy with project version and 'latest' alias
poetry run dagger-pipeline docs deploy

# Deploy specific version
poetry run dagger-pipeline docs deploy --version 2.0.0

# Deploy with custom alias
poetry run dagger-pipeline docs deploy --version 2.0.0 --alias stable

# Deploy and set as default version
poetry run dagger-pipeline docs deploy --version 2.0.0 --set-default
```

### List Versions

List all deployed documentation versions:

```bash
poetry run dagger-pipeline docs list-versions
```

### Delete Version

Delete a specific documentation version:

```bash
poetry run dagger-pipeline docs delete-version 1.0.0
```

## GitHub Actions Integration

The project's CI/CD pipeline automatically deploys documentation when changes are pushed to the main branch. The workflow:

1. Gets the current project version from `pyproject.toml`
1. Deploys documentation with that version and the `latest` alias
1. Sets `latest` as the default version

## Version Display

The documentation site includes:

- **Version selector**: Users can switch between different versions
- **Version badge**: Shows the current version being viewed
- **Latest indicator**: Clearly marks the latest/default version

## Best Practices

### Version Naming

- Use semantic versioning (e.g., `1.2.3`)
- Use meaningful aliases like `latest`, `stable`, `dev`
- Avoid overwriting existing versions unless necessary

### Deployment Strategy

- Deploy documentation for each release
- Keep the `latest` alias pointing to the most recent stable release
- Use descriptive commit messages when deploying documentation

### Maintenance

- Regularly review and clean up old versions
- Ensure documentation stays in sync with code changes
- Test documentation builds before deployment

## Troubleshooting

### Common Issues

**Git configuration errors**: Ensure git is properly configured in your environment.

**Version conflicts**: Use `list-versions` to check existing versions before deployment.

**Build failures**: Run `docs build` locally to test before deployment.

### Getting Help

For issues with documentation versioning:

1. Check the build logs with `--verbose` flag
1. Verify your git configuration
1. Ensure all dependencies are installed with `poetry install --with=docs`

## Examples

### Release Workflow

When releasing version 2.1.0:

```bash
# Update project version
poetry version 2.1.0

# Deploy documentation
poetry run dagger-pipeline docs deploy --version 2.1.0 --alias latest --set-default

# Verify deployment
poetry run dagger-pipeline docs list-versions
```

### Development Workflow

For development documentation:

```bash
# Serve locally during development
poetry run dagger-pipeline docs serve

# Build and test
poetry run dagger-pipeline docs build

# Deploy development version
poetry run dagger-pipeline docs deploy --version dev --alias development
```
