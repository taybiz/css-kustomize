# CSS-Kustomize Project Overview

## Project Description

A Kubernetes application deployment project using Kustomize for configuration management, featuring a comprehensive linting and automation pipeline built with Dagger.

## Architecture

### Core Components

- **Base Configuration**: Standard Kubernetes manifests (deployment, service, kustomization)
- **Overlays**: Environment-specific configurations
  - `with-pvc`: Local development with persistent volume claims
- **Dagger Pipeline**: Python-based automation for linting and validation
- **Memory Bank**: Knowledge repository for project documentation

### Technology Stack

- **Kubernetes**: Container orchestration
- **Kustomize**: Configuration management
- **Python**: Automation and tooling
- **Dagger**: CI/CD pipeline automation
- **Poetry**: Python dependency management

## Directory Structure

```
css-kustomize/
├── base/                    # Base Kubernetes manifests
├── overlays/               # Environment-specific overlays
├── dagger_pipeline/        # Dagger automation code
├── memory-bank/           # Knowledge repository
├── manifests/             # Generated manifests (output)
├── pyproject.toml         # Python project configuration
├── .yamllint.yml          # YAML linting configuration
└── README.md              # Project documentation
```

## Key Features

- Multi-environment configuration management
- Comprehensive linting (YAML, Python, security)
- Automated pipeline with Dagger
- Cross-platform automation scripts
- Security-focused validation

## Development Workflow

1. Modify base configurations or overlays
1. Run linting pipeline for validation
1. Generate manifests using Kustomize
1. Deploy to target environment

## Current Status

- Base infrastructure: ✅ Complete
- Linting pipeline: ✅ Complete
- Dagger automation: ✅ Complete
- Memory bank: 🔄 In progress
- Documentation: 🔄 Ongoing

## Next Steps

- Expand overlay configurations for additional environments
- Enhance security scanning capabilities
- Add integration testing
- Improve documentation coverage
