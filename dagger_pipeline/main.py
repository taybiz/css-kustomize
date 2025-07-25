"""Main CLI entry point for Dagger pipeline automation.

This module provides the command-line interface for the CSS Kustomize Dagger pipeline,
offering comprehensive automation for linting, validation, manifest generation, and
deployment workflows. The CLI is built using Click and provides rich console output
for better user experience.

## Pipeline Capabilities

- **YAML Linting**: Comprehensive syntax and style validation with yamllint
- **Python Code Quality**: Automated checks and formatting with ruff
- **Markdown Validation**: Format checking and consistency enforcement
- **Kustomize Integration**: Configuration validation and manifest generation
- **Version Management**: Automated version updates across overlays

## Usage Examples

Run the complete CI pipeline:
```bash
poetry run dagger-pipeline ci --verbose
```

Generate manifests for all overlays:
```bash
poetry run dagger-pipeline generate
```

Update version across all overlays:
```bash
poetry run dagger-pipeline version update 1.2.3
```

## CLI Structure

The CLI is organized into command groups:
- `lint`: Code quality and validation commands
- `generate`: Manifest generation commands
- `ci`: Complete CI pipeline execution
- `version`: Version management commands
- `setup`: Development environment setup
"""

import asyncio
import sys

import click
from rich.console import Console
from rich.panel import Panel

from .pipeline import Pipeline

console = Console()


@click.group()
@click.version_option()
def cli():
    """CSS Kustomize Dagger Pipeline - Comprehensive automation for linting, validation, and deployment.

    This CLI provides a comprehensive suite of tools for managing Kubernetes manifests
    using Kustomize, with automated linting, validation, and deployment capabilities
    powered by Dagger for containerized execution.

    The pipeline ensures code quality, and consistent deployment
    practices across different environments and overlays.
    """
    pass


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def lint(
    verbose: bool,
):
    """Run comprehensive linting and validation checks.

    This command performs various code quality and configuration validation checks
    on the project. By default, it runs all available linting checks, but can be
    configured to run specific checks only.

    Args:
        verbose: If True, enable detailed output during execution

    The linting includes:
    - YAML syntax and style validation
    - Python code quality checks (syntax, style, imports)
    - Python code formatting validation
    - Markdown formatting validation
    - Kustomize configuration validation
    - Security scanning of Kubernetes manifests

    Examples:
        Run all linting checks:
            $ poetry run dagger-pipeline lint

        Run with verbose output:
            $ poetry run dagger-pipeline lint --verbose
    """

    console.print(Panel.fit("🔍 CSS Kustomize Linting Pipeline", style="bold blue"))

    async def run_lint():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.run_all_linting()

            console.print("🎉 All linting checks passed!", style="bold green")

        except Exception as e:
            console.print(f"❌ Linting failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_lint())


@cli.command()
@click.option("--overlay", help="Specific overlay to generate (e.g., with-pvc)")
@click.option("--output-dir", default="manifests", help="Output directory for generated manifests")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def generate(overlay: str | None, output_dir: str, verbose: bool):
    """Generate Kustomize manifests for overlays.

    This command uses Kustomize to build and generate Kubernetes manifests
    from the configured overlays. It can generate manifests for a specific
    overlay or all available overlays.

    Args:
        overlay: Name of specific overlay to generate (e.g., 'with-pvc', 'with-pvc').
                If None, generates manifests for all overlays.
        output_dir: Directory where generated manifests will be saved.
                   Defaults to 'manifests'.
        verbose: If True, enable detailed output during generation.

    The generated manifests include all Kubernetes resources defined in the
    base configuration and modified by the overlay-specific patches and
    configurations.

    Examples:
        Generate all overlays:
            $ poetry run dagger-pipeline generate

        Generate specific overlay:
            $ poetry run dagger-pipeline generate --overlay with-pvc

        Generate to custom directory:
            $ poetry run dagger-pipeline generate --output-dir ./output
    """

    console.print(Panel.fit("🏗️ CSS Kustomize Generation Pipeline", style="bold blue"))

    async def run_generate():
        pipeline = Pipeline(verbose=verbose)

        try:
            if overlay:
                await pipeline.generate_overlay(overlay, output_dir)
            else:
                await pipeline.generate_all_overlays(output_dir)

            console.print("🎉 Manifest generation completed!", style="bold green")

        except Exception as e:
            console.print(f"❌ Generation failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_generate())


@cli.command()
@click.option("--output-dir", default="manifests", help="Output directory for generated manifests")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def ci(output_dir: str, verbose: bool):
    """Run complete CI pipeline (lint, validate, generate).

    This is the main CI command that executes the full pipeline workflow.
    It performs all quality checks, and generates manifests.

    Args:
        output_dir: Directory where generated manifests will be saved.
                   Defaults to 'manifests'.
        verbose: If True, enable detailed output during execution.

    The CI pipeline includes:
    1. Comprehensive linting (YAML, Python, Markdown)
    2. Kustomize configuration validation
    3. Security scanning of configurations
    4. Manifest generation for all overlays
    5. Security scanning of generated manifests

    This command is designed to be run in CI/CD environments to ensure
    code quality and deployment readiness.

    Examples:
        Run complete CI pipeline:
            $ poetry run dagger-pipeline ci

        Run with verbose output:
            $ poetry run dagger-pipeline ci --verbose

        Generate to custom directory:
            $ poetry run dagger-pipeline ci --output-dir ./build
    """

    console.print(Panel.fit("🚀 CSS Kustomize CI Pipeline", style="bold blue"))

    async def run_ci():
        pipeline = Pipeline(verbose=verbose)

        try:
            # Run all linting checks
            await pipeline.run_all_linting()
            console.print("✅ Linting completed", style="green")

            # Generate all overlays
            await pipeline.generate_all_overlays(output_dir)
            console.print("✅ Manifest generation completed", style="green")

            console.print("🎉 Complete CI pipeline passed!", style="bold green")

        except Exception as e:
            console.print(f"❌ CI pipeline failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_ci())


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def setup(verbose: bool):
    """Set up development environment and install dependencies."""

    console.print(Panel.fit("⚙️ CSS Kustomize Setup", style="bold blue"))

    async def run_setup():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.setup_environment()
            console.print("🎉 Environment setup completed!", style="bold green")

        except Exception as e:
            console.print(f"❌ Setup failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_setup())


@cli.group()
def docs():
    """Documentation building and deployment commands."""
    pass


@docs.command()
@click.option("--version", help="Version to deploy (defaults to project version)")
@click.option("--alias", default="latest", help="Version alias (default: latest)")
@click.option("--set-default", is_flag=True, help="Set this version as default")
@click.option("--title", help="Version title for display (defaults to version)")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def deploy(version: str | None, alias: str, set_default: bool, title: str | None, verbose: bool):
    """Deploy documentation with version management using mike."""

    console.print(Panel.fit("📚 CSS Kustomize Documentation Deployment", style="bold blue"))

    async def run_docs_deploy():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.deploy_docs(version, alias, set_default, title)
            console.print("🎉 Documentation deployed successfully!", style="bold green")

        except Exception as e:
            console.print(f"❌ Documentation deployment failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_docs_deploy())


@docs.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def build(verbose: bool):
    """Build documentation locally for testing."""

    console.print(Panel.fit("🏗️ CSS Kustomize Documentation Build", style="bold blue"))

    async def run_docs_build():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.build_docs()
            console.print("🎉 Documentation built successfully!", style="bold green")

        except Exception as e:
            console.print(f"❌ Documentation build failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_docs_build())


@docs.command()
@click.option("--port", default=8000, help="Port to serve documentation on")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def serve(port: int, verbose: bool):
    """Serve documentation locally for development."""

    console.print(Panel.fit("🌐 CSS Kustomize Documentation Server", style="bold blue"))

    async def run_docs_serve():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.serve_docs(port)

        except Exception as e:
            console.print(f"❌ Documentation server failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_docs_serve())


@docs.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def list_versions(verbose: bool):
    """List all deployed documentation versions."""

    console.print(Panel.fit("📋 CSS Kustomize Documentation Versions", style="bold blue"))

    async def run_list_versions():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.list_doc_versions()

        except Exception as e:
            console.print(f"❌ Failed to list versions: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_list_versions())


@docs.command()
@click.argument("version")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def delete_version(version: str, verbose: bool):
    """Delete a specific documentation version."""

    console.print(Panel.fit("🗑️ CSS Kustomize Documentation Version Deletion", style="bold blue"))

    async def run_delete_version():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.delete_doc_version(version)

        except Exception as e:
            console.print(f"❌ Failed to delete version: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_delete_version())


@cli.group()
def version():
    """Version management commands for image tags and labels."""
    pass


@version.command()
@click.argument("new_version")
@click.option("--overlay", help="Update specific overlay only (e.g., with-base, with-pvc)")
@click.option("--dry-run", is_flag=True, help="Show what would be changed without making changes")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def update(new_version: str, overlay: str | None, dry_run: bool, verbose: bool):
    """Update image tags and version labels across overlays."""

    console.print(Panel.fit("🏷️ CSS Kustomize Version Update", style="bold blue"))

    async def run_version_update():
        pipeline = Pipeline(verbose=verbose)

        try:
            if overlay:
                await pipeline.update_overlay_version(overlay, new_version, dry_run)
            else:
                await pipeline.update_all_versions(new_version, dry_run)

            if dry_run:
                console.print("🔍 Dry run completed. No changes were made.", style="bold yellow")
            else:
                console.print(f"🎉 Version updated to {new_version}!", style="bold green")

        except Exception as e:
            console.print(f"❌ Version update failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_version_update())


@version.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def validate(verbose: bool):
    """Validate version consistency across all overlays."""

    console.print(Panel.fit("🔍 CSS Kustomize Version Validation", style="bold blue"))

    async def run_version_validate():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.validate_version_consistency()
            console.print("🎉 Version validation passed!", style="bold green")

        except Exception as e:
            console.print(f"❌ Version validation failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_version_validate())


@version.command()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def report(verbose: bool):
    """Generate version report showing current versions across overlays."""

    console.print(Panel.fit("📊 CSS Kustomize Version Report", style="bold blue"))

    async def run_version_report():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.generate_version_report()

        except Exception as e:
            console.print(f"❌ Version report failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_version_report())


if __name__ == "__main__":
    cli()
