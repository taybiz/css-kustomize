# Configuration

Learn how to configure CSS Kustomize for your environment and needs.

## Overview

CSS Kustomize uses several configuration files and environment variables to customize behavior.

## Configuration Files

### Poetry Configuration (`pyproject.toml`)

The main project configuration is in `pyproject.toml`:

```toml
[tool.poetry]
name = "css-kustomize"
version = "0.1.0"
description = "Kubernetes manifests for Community Solid Server"

[tool.poetry.scripts]
dagger-pipeline = "dagger_pipeline.main:cli"
```

### YAML Linting (`.yamllint.yml`)

Configure YAML linting rules:

```yaml
extends: default
rules:
  line-length:
    max: 120
  truthy:
    allowed-values: ['true', 'false', 'on', 'off']
```

### Dagger Configuration (`dagger.json`)

Dagger engine configuration:

```json
{
  "name": "css-kustomize",
  "sdk": "python"
}
```

## Environment Variables

### Dagger Settings

- `DAGGER_LOG_LEVEL`: Set logging level (`debug`, `info`, `warn`, `error`)
- `DAGGER_CACHE_VOLUME`: Custom cache volume name

### CLI Behavior

- `NO_COLOR`: Disable colored output
- `FORCE_COLOR`: Force colored output in non-TTY environments

## Customization

### Adding New Overlays

1. Create overlay directory in `overlays/`
1. Add `kustomization.yaml`
1. Update CLI to include new overlay

### Modifying Base Resources

Edit files in the `base/` directory to change default configurations.

## Next Steps

- Explore [CLI Commands](../user-guide/cli-commands.md)
- Learn about [Kustomize Overlays](../user-guide/kustomize-overlays.md)
