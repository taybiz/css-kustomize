# Contributing

Guidelines for contributing to the CSS Kustomize project.

## Getting Started

### Development Setup

1. **Fork and clone the repository**:

   ```bash
   git clone https://github.com/your-username/css-kustomize.git
   cd css-kustomize
   ```

1. **Install development dependencies**:

   ```bash
   poetry install --with=lint,docs
   ```

1. **Set up pre-commit hooks**:

   ```bash
   poetry run pre-commit install
   ```

1. **Verify setup**:

   ```bash
   poetry run dagger-pipeline ci --verbose
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

1. **Make your changes** following the coding standards

1. **Run tests and linting**:

   ```bash
   poetry run dagger-pipeline lint
   poetry run dagger-pipeline validate
   ```

1. **Commit your changes**:

   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

### Coding Standards

#### Python Code

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Use ruff for linting and formatting

#### YAML Files

- Use 2-space indentation
- Follow yamllint configuration
- Use meaningful names and comments

#### Documentation

- Write clear, concise documentation
- Include code examples
- Update relevant sections

## Testing

### Running Tests

```bash
# Run complete CI pipeline
poetry run dagger-pipeline ci

# Run specific tests
poetry run dagger-pipeline lint --python-only
poetry run dagger-pipeline validate
poetry run dagger-pipeline security-scan
```

### Adding Tests

- Add tests for new functionality
- Ensure good test coverage
- Test both success and failure cases

## Documentation

### Building Documentation

```bash
# Install docs dependencies
poetry install --only=docs

# Build documentation
poetry run mkdocs build

# Serve locally
poetry run mkdocs serve
```

### Writing Documentation

- Use clear, concise language
- Include practical examples
- Update navigation in mkdocs.yml
- Follow existing structure

## Pull Request Process

### Before Submitting

1. **Ensure all tests pass**:

   ```bash
   poetry run dagger-pipeline ci --verbose
   ```

1. **Update documentation** if needed

1. **Add changelog entry** if applicable

### Submitting

1. **Push your branch**:

   ```bash
   git push origin feature/your-feature-name
   ```

1. **Create pull request** with:

   - Clear description of changes
   - Reference to related issues
   - Screenshots if applicable

1. **Address review feedback** promptly

## Code Review Guidelines

### For Authors

- Keep changes focused and small
- Write clear commit messages
- Respond to feedback constructively
- Update based on suggestions

### For Reviewers

- Be constructive and helpful
- Focus on code quality and maintainability
- Test the changes locally
- Approve when ready

## Release Process

### Version Updates

```bash
# Update version across overlays
poetry run dagger-pipeline version update 6.0.3

# Validate changes
poetry run dagger-pipeline validate-versions
poetry run dagger-pipeline ci
```

### Creating Releases

1. Update version numbers
1. Update changelog
1. Create git tag
1. Generate release notes

## Community Guidelines

### Communication

- Be respectful and inclusive
- Use clear, professional language
- Help others learn and grow
- Share knowledge and experience

### Issue Reporting

- Use issue templates
- Provide clear reproduction steps
- Include relevant system information
- Search existing issues first

## Getting Help

### Resources

- **Documentation**: Read the full documentation
- **Issues**: Search existing issues
- **Discussions**: Join GitHub discussions
- **Code**: Review existing code patterns

### Contact

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## Recognition

Contributors are recognized through:

- GitHub contributor graphs
- Release notes mentions
- Documentation credits
- Community acknowledgments

Thank you for contributing to CSS Kustomize!
