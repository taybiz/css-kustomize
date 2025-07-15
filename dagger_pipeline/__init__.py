"""Dagger pipeline for CSS Kustomize project automation.

This package provides comprehensive automation tools for Kubernetes manifest
management using Kustomize, with containerized execution via Dagger for
consistent and reproducible builds across different environments.

## Key Features

- **YAML Linting**: Comprehensive YAML syntax and style validation
- **Python Code Quality**: Automated linting and formatting with ruff
- **Markdown Validation**: Format checking and consistency enforcement
- **Kustomize Integration**: Configuration validation and manifest generation
- **Security Scanning**: Kubernetes manifest security analysis
- **Version Management**: Automated version updates across overlays

## Usage

The package provides both a CLI interface and programmatic API:

```python
from dagger_pipeline import Pipeline

# Create pipeline instance
pipeline = Pipeline(verbose=True)

# Run comprehensive linting
await pipeline.run_all_linting()

# Generate manifests
await pipeline.generate_all_overlays("manifests")
```

For CLI usage, see the `main` module documentation.
"""

__version__ = "0.1.0"
