# Memory Bank Index

Quick navigation guide to all knowledge stored in the css-kustomize memory bank.

## 📋 Project Overview

- [`project-overview.md`](project-overview.md) - Complete project description, architecture, and current status

## 🎯 Patterns & Best Practices

- [`patterns/kustomize-patterns.md`](patterns/kustomize-patterns.md) - Kustomize configuration patterns and anti-patterns
- [`patterns/dagger-automation.md`](patterns/dagger-automation.md) - Dagger pipeline architecture and best practices

## 🔧 Troubleshooting

- [`troubleshooting/common-issues.md`](troubleshooting/common-issues.md) - Solutions for linting, Dagger, Kustomize, and development issues

## 🔄 Workflows

- [`workflows/development-workflow.md`](workflows/development-workflow.md) - Daily development, release, and maintenance processes

## 📝 Architecture Decisions

- [`decisions/001-dagger-over-github-actions.md`](decisions/001-dagger-over-github-actions.md) - Decision to use Dagger Python SDK for automation

## 🔗 External Resources

- [`references/external-resources.md`](references/external-resources.md) - Curated links to documentation, tools, and learning materials

## Quick Reference

### Common Commands

```bash
# Run full linting pipeline
python -m dagger_pipeline.main

# Generate manifests
kustomize build overlays/with-pvc > manifests/with-pvc.yaml

# Setup development environment
poetry install && pre-commit install
```

### Key Files

- `pyproject.toml` - Python dependencies and tool configuration
- `.yamllint.yml` - YAML linting rules
- `dagger_pipeline/` - Automation pipeline code
- `base/` - Base Kubernetes manifests
- `overlays/` - Environment-specific configurations

### Project Structure

```
css-kustomize/
├── memory-bank/           # 📚 This knowledge repository
├── base/                  # 🏗️ Base Kubernetes manifests
├── overlays/             # 🎯 Environment-specific configs
├── dagger_pipeline/      # 🔄 Automation pipeline
├── manifests/            # 📄 Generated output
└── pyproject.toml        # ⚙️ Python configuration
```

## Navigation Tips

- Use the file links above for quick access
- Each section contains detailed information and examples
- Troubleshooting guide includes common error solutions
- External resources provide additional learning materials
- Architecture decisions explain why certain choices were made

## Contributing to Memory Bank

When adding new knowledge:

1. Choose the appropriate section (patterns, troubleshooting, etc.)
1. Use clear, descriptive filenames
1. Include practical examples and code snippets
1. Update this index file with new entries
1. Cross-reference related content where helpful

______________________________________________________________________

*Last updated: 2025-01-13*
