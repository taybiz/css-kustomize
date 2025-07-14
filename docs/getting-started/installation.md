# Installation

This guide will help you set up CSS Kustomize on your local development environment.

## Prerequisites

Before installing CSS Kustomize, ensure you have the following tools installed:

### Required Tools

- **Python 3.11+**: The project requires Python 3.11 or later
- **Poetry**: For dependency management and virtual environments
- **Docker**: Required for Dagger containerized execution
- **kubectl**: For Kubernetes manifest validation and deployment
- **Git**: For version control

### Optional Tools

- **Kustomize**: While not strictly required (Dagger containers include it), having it locally can be helpful
- **yq**: For YAML processing and debugging

## Installation Methods

### Method 1: Poetry (Recommended)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/taybiz/css-kustomize.git
   cd css-kustomize
   ```

1. **Install Poetry** (if not already installed):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

1. **Install dependencies**:

   ```bash
   # Install all dependencies
   poetry install

   # Or install only specific groups
   poetry install --only=main,lint
   poetry install --only=docs  # For documentation development
   ```

1. **Verify installation**:

   ```bash
   poetry run dagger-pipeline --help
   ```

### Method 2: Development Installation

For active development on the CSS Kustomize project:

1. **Clone and enter the repository**:

   ```bash
   git clone https://github.com/taybiz/css-kustomize.git
   cd css-kustomize
   ```

1. **Install in development mode**:

   ```bash
   poetry install --with=lint,docs
   ```

1. **Set up pre-commit hooks**:

   ```bash
   poetry run pre-commit install
   ```

1. **Run the test suite**:

   ```bash
   poetry run dagger-pipeline ci --verbose
   ```

## Platform-Specific Instructions

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Install Docker
sudo apt install docker.io
sudo usermod -aG docker $USER
newgrp docker

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

### macOS

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install python@3.11 docker kubectl poetry

# Start Docker Desktop
open /Applications/Docker.app
```

### Windows

1. **Install Python 3.11** from [python.org](https://www.python.org/downloads/)
1. **Install Docker Desktop** from [docker.com](https://www.docker.com/products/docker-desktop/)
1. **Install kubectl** using [official instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
1. **Install Poetry**:
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```

## Verification

After installation, verify everything is working correctly:

### 1. Check Python Version

```bash
python --version
# Should output: Python 3.11.x or later
```

### 2. Check Poetry

```bash
poetry --version
# Should output: Poetry (version 1.x.x)
```

### 3. Check Docker

```bash
docker --version
# Should output: Docker version x.x.x
```

### 4. Check kubectl

```bash
kubectl version --client
# Should output client version information
```

### 5. Test CSS Kustomize

```bash
cd css-kustomize
poetry run dagger-pipeline --help
# Should display the CLI help
```

### 6. Run Quick Test

```bash
# Run a quick linting test
poetry run dagger-pipeline lint --yaml-only

# Generate a test manifest
poetry run dagger-pipeline generate-overlay without-pvc /tmp/test-manifest.yaml
```

## Troubleshooting

### Common Issues

#### Poetry Not Found

If `poetry` command is not found after installation:

```bash
# Add Poetry to PATH (Linux/macOS)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or for zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Docker Permission Denied

If you get permission denied errors with Docker:

```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Test Docker access
docker run hello-world
```

#### Python Version Issues

If you have multiple Python versions:

```bash
# Use Poetry with specific Python version
poetry env use python3.11

# Verify the environment
poetry env info
```

#### Dagger Connection Issues

If Dagger fails to connect:

```bash
# Ensure Docker is running
docker ps

# Check Docker daemon
sudo systemctl status docker  # Linux
brew services list | grep docker  # macOS
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Run commands with `--verbose` flag for detailed output
1. **Search existing issues**: Check [GitHub Issues](https://github.com/taybiz/css-kustomize/issues)
1. **Create a new issue**: Include your OS, Python version, and error messages
1. **Join discussions**: Use [GitHub Discussions](https://github.com/taybiz/css-kustomize/discussions)

## Next Steps

Once installation is complete:

1. **Read the [Quick Start Guide](quick-start.md)** to get familiar with basic operations
1. **Review [Configuration](configuration.md)** to customize the setup for your needs
1. **Explore [CLI Commands](../user-guide/cli-commands.md)** to understand available operations
1. **Check out [Examples](../examples/basic-usage.md)** for common workflows

## Development Environment

For contributors and advanced users, see the [Contributing Guide](../developer-guide/contributing.md) for additional setup steps including:

- Development dependencies
- Testing frameworks
- Documentation building
- Code quality tools
