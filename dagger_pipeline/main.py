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
- **Security Scanning**: Kubernetes manifest security analysis
- **Version Management**: Automated version updates across overlays
- **Parallel Execution**: High-performance concurrent operations

## Usage Examples

Run the complete CI pipeline:
```bash
poetry run dagger-pipeline ci --verbose
```

Run only YAML linting:
```bash
poetry run dagger-pipeline lint --yaml-only
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

    The pipeline ensures code quality, security compliance, and consistent deployment
    practices across different environments and overlays.
    """
    pass


@cli.command()
@click.option("--yaml-only", is_flag=True, help="Run only YAML linting")
@click.option("--python-only", is_flag=True, help="Run only Python linting and formatting")
@click.option("--kustomize-only", is_flag=True, help="Run only Kustomize validation")
@click.option("--security-only", is_flag=True, help="Run only security checks")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def lint(
    yaml_only: bool,
    python_only: bool,
    kustomize_only: bool,
    security_only: bool,
    verbose: bool,
):
    """Run comprehensive linting and validation checks.

    This command performs various code quality and configuration validation checks
    on the project. By default, it runs all available linting checks, but can be
    configured to run specific checks only.

    Args:
        yaml_only: If True, run only YAML linting with yamllint
        python_only: If True, run only Python linting and formatting checks with ruff
        kustomize_only: If True, run only Kustomize configuration validation
        security_only: If True, run only security checks on Kubernetes manifests
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

        Run only YAML linting:
            $ poetry run dagger-pipeline lint --yaml-only

        Run with verbose output:
            $ poetry run dagger-pipeline lint --verbose
    """

    console.print(Panel.fit("🔍 CSS Kustomize Linting Pipeline", style="bold blue"))

    async def run_lint():
        pipeline = Pipeline(verbose=verbose)

        try:
            if yaml_only:
                await pipeline.lint_yaml()
            elif python_only:
                await pipeline.lint_python()
            elif kustomize_only:
                await pipeline.validate_kustomize()
            elif security_only:
                await pipeline.security_scan()
            else:
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
    """Run complete CI pipeline (lint, validate, generate, security scan).

    This is the main CI command that executes the full pipeline workflow.
    It performs all quality checks, generates manifests, and runs security
    scans to ensure the project is ready for deployment.

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

            # Run security scan on generated manifests
            await pipeline.security_scan_generated(output_dir)
            console.print("✅ Security scan completed", style="green")

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


@cli.command()
@click.option("--yaml-only", is_flag=True, help="Run only YAML linting")
@click.option("--python-only", is_flag=True, help="Run only Python linting")
@click.option("--kustomize-only", is_flag=True, help="Run only Kustomize validation")
@click.option("--security-only", is_flag=True, help="Run only security checks")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def lint_parallel(
    yaml_only: bool,
    python_only: bool,
    kustomize_only: bool,
    security_only: bool,
    verbose: bool,
):
    """Run linting checks in parallel for maximum speed (cached)."""

    console.print(Panel.fit("🚀 CSS Kustomize Parallel Linting Pipeline", style="bold blue"))

    async def run_lint_parallel():
        pipeline = Pipeline(verbose=verbose)

        try:
            if yaml_only:
                await pipeline.lint_yaml()
            elif python_only:
                await pipeline.lint_python()
            elif kustomize_only:
                await pipeline.validate_kustomize()
            elif security_only:
                await pipeline.security_scan()
            else:
                await pipeline.run_all_linting_parallel()

            console.print("🎉 All parallel linting checks passed!", style="bold green")

        except Exception as e:
            console.print(f"❌ Parallel linting failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_lint_parallel())


@cli.command()
@click.option("--output-dir", default="manifests", help="Output directory for generated manifests")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def generate_parallel(output_dir: str, verbose: bool):
    """Generate all Kustomize manifests in parallel for maximum speed."""

    console.print(Panel.fit("🚀 CSS Kustomize Parallel Generation Pipeline", style="bold blue"))

    async def run_generate_parallel():
        pipeline = Pipeline(verbose=verbose)

        try:
            await pipeline.generate_all_overlays_parallel(output_dir)
            console.print("🎉 Parallel manifest generation completed!", style="bold green")

        except Exception as e:
            console.print(f"❌ Parallel generation failed: {e}", style="bold red")
            sys.exit(1)

    asyncio.run(run_generate_parallel())


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
