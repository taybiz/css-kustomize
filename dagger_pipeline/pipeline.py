"""Core Dagger pipeline implementation for CSS Kustomize automation.

This module contains the Pipeline class which implements all the core functionality
for the CSS Kustomize Dagger automation pipeline. It provides methods for linting,
validation, manifest generation, security scanning, and version management.

The pipeline uses Dagger for containerized execution, ensuring consistent and
reproducible builds across different environments. All operations are performed
in isolated containers with the necessary tools and dependencies.

## Key Features

- **YAML Linting**: Comprehensive syntax and style validation with yamllint
- **Python Code Quality**: Automated checks and formatting with ruff
- **Markdown Validation**: Format checking and consistency enforcement
- **Kustomize Integration**: Configuration validation and manifest generation
- **Security Scanning**: Kubernetes manifest security analysis
- **Version Management**: Automated version updates across overlays
- **Parallel Execution**: High-performance concurrent operations
- **Rich Console Output**: Progress indicators and detailed feedback

## Usage Example

Basic usage of the Pipeline class:

```python
pipeline = Pipeline(verbose=True)
await pipeline.run_all_linting()
await pipeline.generate_all_overlays("manifests")
await pipeline.security_scan_generated("manifests")
```

## Container Architecture

The pipeline uses specialized containers for different operations:
- **Python Container**: Poetry-based environment for Python and Markdown linting
- **Kustomize Container**: Alpine-based environment with Kustomize CLI
- **YAML Container**: Alpine-based environment with yq for YAML processing
"""

import re
from pathlib import Path

import dagger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class Pipeline:
    """Main pipeline class for CSS Kustomize automation.

    This class orchestrates all pipeline operations including linting, validation,
    manifest generation, and security scanning. It uses Dagger for containerized
    execution to ensure consistent and reproducible builds.

    Attributes:
        verbose (bool): Whether to enable verbose output during operations.
        project_root (Path): Path to the project root directory.

    The pipeline supports both sequential and parallel execution modes for
    different operations, with automatic caching through Dagger to improve
    performance on subsequent runs.
    """

    def __init__(self, verbose: bool = False):
        """Initialize the Pipeline instance.

        Args:
            verbose: If True, enables detailed output during pipeline execution.
                    This includes container build logs, command outputs, and
                    detailed progress information.
        """
        self.verbose = verbose
        self.project_root = Path.cwd()

    def _get_client(self) -> dagger.Connection:
        """Get Dagger client connection.

        Creates and configures a Dagger client connection for containerized execution.
        If verbose mode is enabled, configures the client to output detailed logs.

        Returns:
            dagger.Connection: Configured Dagger client connection.
        """
        config = dagger.Config()
        if self.verbose:
            config = dagger.Config(log_output=console.file)
        return dagger.Connection(config)

    async def _get_python_container(self, client: dagger.Client) -> dagger.Container:
        """Get Python container with Poetry and dependencies installed.

        Creates a containerized Python environment with Poetry package manager
        and installs the project's linting dependencies. This container is used
        for all Python-related operations including linting, formatting, and
        markdown validation.

        Args:
            client: Dagger client instance for container operations.

        Returns:
            dagger.Container: Configured Python container with Poetry and lint dependencies.

        The container includes:
        - Python 3.11 slim base image
        - System packages: curl, git
        - Poetry package manager
        - Project source code mounted at /src
        - Lint dependencies installed via Poetry
        """
        return (
            client.container()
            .from_("python:3.11-slim")
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "curl", "git"])
            .with_exec(["pip", "install", "poetry"])
            .with_directory("/src", client.host().directory("."))
            .with_workdir("/src")
            .with_exec(["poetry", "config", "virtualenvs.create", "false"])
            .with_exec(["poetry", "install", "--only=lint"])
        )

    async def _get_kustomize_container(self, client: dagger.Client) -> dagger.Container:
        """Get container with Kustomize installed.

        Creates a containerized environment with Kustomize CLI tool for building
        and validating Kubernetes manifests. This container is used for all
        Kustomize-related operations including validation and manifest generation.

        Args:
            client: Dagger client instance for container operations.

        Returns:
            dagger.Container: Configured Alpine container with Kustomize installed.

        The container includes:
        - Alpine Linux base image
        - System packages: curl, bash
        - Latest Kustomize CLI tool
        - Project source code mounted at /src
        """
        return (
            client.container()
            .from_("alpine:latest")
            .with_exec(["apk", "add", "--no-cache", "curl", "bash"])
            .with_exec(
                [
                    "sh",
                    "-c",
                    "curl -s https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh | bash",  # noqa: E501
                ]
            )
            .with_exec(["mv", "kustomize", "/usr/local/bin/"])
            .with_directory("/src", client.host().directory("."))
            .with_workdir("/src")
        )

    async def lint_yaml(self) -> None:
        """Run YAML linting using yamllint."""
        if self.verbose:
            console.print("🔍 Running YAML linting...")

        async with self._get_client() as client:
            container = await self._get_python_container(client)

            result = await container.with_exec(
                ["poetry", "run", "yamllint", "."]
            ).stdout()

            if self.verbose:
                console.print(result)

            console.print("✅ YAML linting passed", style="green")

    async def lint_python(self) -> None:
        """Run Python linting and formatting checks."""
        if self.verbose:
            console.print("🔍 Running Python linting...")

        async with self._get_client() as client:
            container = await self._get_python_container(client)

            # Run ruff check
            await container.with_exec(["poetry", "run", "ruff", "check", "."]).stdout()

            # Run ruff format check
            await container.with_exec(
                ["poetry", "run", "ruff", "format", "--check", "."]
            ).stdout()

            console.print("✅ Python linting passed", style="green")

    async def lint_markdown(self) -> None:
        """Run Markdown linting and formatting checks."""
        if self.verbose:
            console.print("🔍 Running Markdown linting...")

        async with self._get_client() as client:
            container = await self._get_python_container(client)

            # Check if there are any markdown files to lint
            try:
                # Find markdown files
                md_files_result = await container.with_exec(
                    [
                        "find",
                        ".",
                        "-name",
                        "*.md",
                        "-type",
                        "f",
                        "!",
                        "-path",
                        "./.venv/*",
                        "!",
                        "-path",
                        "./node_modules/*",
                    ]
                ).stdout()

                md_files = [
                    f.strip() for f in md_files_result.strip().split("\n") if f.strip()
                ]

                if not md_files:
                    console.print("📝 No markdown files found to lint", style="yellow")
                    return

                if self.verbose:
                    console.print(f"Found {len(md_files)} markdown files to check")

                # Run mdformat check (dry-run to validate formatting)
                await container.with_exec(
                    ["poetry", "run", "mdformat", "--check"] + md_files
                ).stdout()

                console.print("✅ Markdown linting passed", style="green")

            except Exception as e:
                console.print(
                    f"❌ Markdown formatting issues found: {str(e)}", style="red"
                )
                raise Exception(
                    "Markdown files need formatting. Run 'poetry run mdformat .' to fix."
                ) from e

    async def validate_kustomize(self) -> None:
        """Validate Kustomize configurations."""
        if self.verbose:
            console.print("🔍 Validating Kustomize configurations...")

        async with self._get_client() as client:
            container = await self._get_kustomize_container(client)

            # Validate base configuration
            await container.with_exec(["kustomize", "build", "base/"]).stdout()

            # Validate overlays
            overlays_dir = self.project_root / "overlays"
            if overlays_dir.exists():
                for overlay_path in overlays_dir.iterdir():
                    if overlay_path.is_dir():
                        overlay_name = overlay_path.name
                        if self.verbose:
                            console.print(f"Validating overlay: {overlay_name}")

                        await container.with_exec(
                            ["kustomize", "build", f"overlays/{overlay_name}/"]
                        ).stdout()

            console.print("✅ Kustomize validation passed", style="green")

    async def security_scan(self) -> None:
        """Run security checks on Kustomize configurations."""
        if self.verbose:
            console.print("🔍 Running security scan...")

        async with self._get_client() as client:
            container = await self._get_kustomize_container(client)

            # Generate manifests for security scanning
            overlays_dir = self.project_root / "overlays"
            security_issues = 0

            if overlays_dir.exists():
                for overlay_path in overlays_dir.iterdir():
                    if overlay_path.is_dir():
                        overlay_name = overlay_path.name
                        if self.verbose:
                            console.print(f"Scanning overlay: {overlay_name}")

                        # Generate manifest
                        manifest_content = await container.with_exec(
                            ["kustomize", "build", f"overlays/{overlay_name}/"]
                        ).stdout()

                        # Check for security issues
                        issues = self._check_security_issues(
                            manifest_content, overlay_name
                        )
                        security_issues += issues

            if security_issues > 0:
                raise Exception(f"Found {security_issues} security issues")

            console.print("✅ Security scan passed", style="green")

    async def security_scan_generated(self, output_dir: str) -> None:
        """Run security checks on generated manifests."""
        if self.verbose:
            console.print("🔍 Running security scan on generated manifests...")

        manifests_dir = Path(output_dir)
        if not manifests_dir.exists():
            raise Exception(f"Manifests directory {output_dir} does not exist")

        security_issues = 0
        for manifest_file in manifests_dir.glob("*.yaml"):
            if self.verbose:
                console.print(f"Scanning manifest: {manifest_file.name}")

            content = manifest_file.read_text()
            issues = self._check_security_issues(content, manifest_file.name)
            security_issues += issues

        if security_issues > 0:
            raise Exception(
                f"Found {security_issues} security issues in generated manifests"
            )

        console.print("✅ Security scan on generated manifests passed", style="green")

    def _check_security_issues(self, manifest_content: str, name: str) -> int:
        """Check for security issues in manifest content."""
        issues = 0

        # Check for root user
        if re.search(r"runAsUser:\s*0\b", manifest_content):
            console.print(f"❌ Found root user in {name}", style="red")
            issues += 1

        # Check for runAsNonRoot
        if not re.search(r"runAsNonRoot.*true", manifest_content):
            console.print(f"⚠️ runAsNonRoot not found in {name}", style="yellow")

        # Check for privileged containers
        if re.search(r"privileged.*true", manifest_content):
            console.print(f"❌ Found privileged container in {name}", style="red")
            issues += 1

        return issues

    async def generate_overlay(self, overlay_name: str, output_dir: str) -> None:
        """Generate manifest for a specific overlay."""
        if self.verbose:
            console.print(f"🏗️ Generating overlay: {overlay_name}")

        overlay_path = self.project_root / "overlays" / overlay_name
        if not overlay_path.exists():
            raise Exception(f"Overlay {overlay_name} does not exist")

        async with self._get_client() as client:
            container = await self._get_kustomize_container(client)

            # Generate manifest
            manifest_content = await container.with_exec(
                ["kustomize", "build", f"overlays/{overlay_name}/"]
            ).stdout()

            # Write to output directory
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)

            manifest_file = output_path / f"{overlay_name}.yaml"
            manifest_file.write_text(manifest_content)

            if self.verbose:
                console.print(f"Generated manifest: {manifest_file}")

    async def generate_all_overlays(self, output_dir: str) -> None:
        """Generate manifests for all overlays."""
        if self.verbose:
            console.print("🏗️ Generating all overlays...")

        overlays_dir = self.project_root / "overlays"
        if not overlays_dir.exists():
            console.print("No overlays directory found", style="yellow")
            return

        for overlay_path in overlays_dir.iterdir():
            if overlay_path.is_dir():
                await self.generate_overlay(overlay_path.name, output_dir)

        console.print("✅ All overlays generated", style="green")

    async def run_all_linting(self) -> None:
        """Run all linting checks."""
        if self.verbose:
            console.print("🔍 Running comprehensive linting...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task1 = progress.add_task("YAML linting...", total=None)
            await self.lint_yaml()
            progress.update(task1, completed=True)

            task2 = progress.add_task("Python linting...", total=None)
            await self.lint_python()
            progress.update(task2, completed=True)

            task3 = progress.add_task("Markdown linting...", total=None)
            await self.lint_markdown()
            progress.update(task3, completed=True)

            task4 = progress.add_task("Kustomize validation...", total=None)
            await self.validate_kustomize()
            progress.update(task4, completed=True)

            task5 = progress.add_task("Security scan...", total=None)
            await self.security_scan()
            progress.update(task5, completed=True)

        console.print("✅ All linting checks completed", style="green")

    async def setup_environment(self) -> None:
        """Set up development environment."""
        if self.verbose:
            console.print("⚙️ Setting up development environment...")

        async with self._get_client() as client:
            # Install Python dependencies
            container = await self._get_python_container(client)

            # Install pre-commit hooks
            await container.with_exec(
                ["poetry", "run", "pre-commit", "install"]
            ).stdout()

            console.print("✅ Development environment setup completed", style="green")

    async def run_pre_commit(self) -> None:
        """Run pre-commit hooks."""
        if self.verbose:
            console.print("🔍 Running pre-commit hooks...")

        async with self._get_client() as client:
            container = await self._get_python_container(client)

            await container.with_exec(
                ["poetry", "run", "pre-commit", "run", "--all-files"]
            ).stdout()

            console.print("✅ Pre-commit hooks passed", style="green")

    async def _get_yaml_container(self, client: dagger.Client) -> dagger.Container:
        """Get container with yq for YAML processing."""
        return (
            client.container()
            .from_("alpine:latest")
            .with_exec(["apk", "add", "--no-cache", "curl", "bash"])
            .with_exec(
                [
                    "sh",
                    "-c",
                    "curl -L https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -o /usr/local/bin/yq && chmod +x /usr/local/bin/yq",
                ]
            )
            .with_directory("/src", client.host().directory("."))
            .with_workdir("/src")
        )

    def _validate_version_format(self, version: str) -> bool:
        """Validate semantic version format."""
        import re

        pattern = r"^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$"
        return bool(re.match(pattern, version))

    async def update_overlay_version(
        self, overlay_name: str, version: str, dry_run: bool = False
    ) -> None:
        """Update version for a specific overlay."""
        if not self._validate_version_format(version):
            raise Exception(
                f"Invalid version format: {version}. Expected X.Y.Z or X.Y.Z-prerelease"
            )

        overlay_path = self.project_root / "overlays" / overlay_name
        if not overlay_path.exists():
            raise Exception(f"Overlay {overlay_name} does not exist")

        kustomization_file = overlay_path / "kustomization.yaml"
        if not kustomization_file.exists():
            raise Exception(f"Kustomization file not found: {kustomization_file}")

        if self.verbose:
            console.print(f"🏷️ Processing overlay: {overlay_name}")

        async with self._get_client() as client:
            container = await self._get_yaml_container(client)

            # Read current values for dry run
            if dry_run:
                current_tag_result = await container.with_exec(
                    [
                        "yq",
                        '.images[] | select(.name == "docker.io/solidproject/community-server") | .newTag',
                        f"overlays/{overlay_name}/kustomization.yaml",
                    ]
                ).stdout()
                current_tag = (
                    current_tag_result.strip()
                    if current_tag_result.strip() != "null"
                    else "not set"
                )

                current_version_result = await container.with_exec(
                    [
                        "yq",
                        '.labels[0].pairs."app.kubernetes.io/version"',
                        f"overlays/{overlay_name}/kustomization.yaml",
                    ]
                ).stdout()
                current_version = (
                    current_version_result.strip()
                    if current_version_result.strip() != "null"
                    else "not set"
                )

                console.print(
                    f"  [DRY RUN] Would update image tag from '{current_tag}' to '{version}'"
                )
                console.print(
                    f"  [DRY RUN] Would update version label from '{current_version}' to '{version}'"
                )
                return

            # Update image tag
            await container.with_exec(
                [
                    "yq",
                    "-i",
                    f'.images[] |= select(.name == "docker.io/solidproject/community-server").newTag = "{version}"',
                    f"overlays/{overlay_name}/kustomization.yaml",
                ]
            ).stdout()

            # Update version label
            await container.with_exec(
                [
                    "yq",
                    "-i",
                    f'.labels[0].pairs."app.kubernetes.io/version" = "{version}"',
                    f"overlays/{overlay_name}/kustomization.yaml",
                ]
            ).stdout()

            # Update version patch if it exists
            patch_check = await container.with_exec(
                [
                    "yq",
                    '.patches[] | select(.target.kind == "Deployment") | .patch',
                    f"overlays/{overlay_name}/kustomization.yaml",
                ]
            ).stdout()

            if "app.kubernetes.io~1version" in patch_check:
                await container.with_exec(
                    [
                        "yq",
                        "-i",
                        f'(.patches[] | select(.target.kind == "Deployment") | .patch) |= sub("value: \\"[^\\"]*\\""; "value: \\"{version}\\""; "g")',
                        f"overlays/{overlay_name}/kustomization.yaml",
                    ]
                ).stdout()
                console.print(f"  ✅ Updated deployment version patch to: {version}")
            else:
                # Add version patch if it doesn't exist
                patch_content = f'      - op: add\\n        path: /spec/template/metadata/labels/app.kubernetes.io~1version\\n        value: \\"{version}\\"'
                await container.with_exec(
                    [
                        "yq",
                        "-i",
                        f'(.patches[] | select(.target.kind == "Deployment") | .patch) += "\\n{patch_content}"',
                        f"overlays/{overlay_name}/kustomization.yaml",
                    ]
                ).stdout()
                console.print(f"  ✅ Added deployment version patch: {version}")

            # Copy updated file back to host
            updated_content = await container.file(
                f"overlays/{overlay_name}/kustomization.yaml"
            ).contents()
            kustomization_file.write_text(updated_content)

            console.print(f"  ✅ Updated image tag to: {version}")
            console.print(f"  ✅ Updated version label to: {version}")

    async def update_all_versions(self, version: str, dry_run: bool = False) -> None:
        """Update version for all overlays."""
        if not self._validate_version_format(version):
            raise Exception(
                f"Invalid version format: {version}. Expected X.Y.Z or X.Y.Z-prerelease"
            )

        overlays_dir = self.project_root / "overlays"
        if not overlays_dir.exists():
            console.print("No overlays directory found", style="yellow")
            return

        overlay_names = [d.name for d in overlays_dir.iterdir() if d.is_dir()]

        if not overlay_names:
            console.print("No overlays found to update", style="yellow")
            return

        for overlay_name in overlay_names:
            await self.update_overlay_version(overlay_name, version, dry_run)

        if not dry_run:
            console.print(
                f"✅ Updated {len(overlay_names)} overlays to version: {version}"
            )

    async def validate_version_consistency(self) -> None:
        """Validate version consistency across all overlays.

        This validates that:
        - Image tags are present and valid (CSS application version)
        - Version labels are present and valid (project version from pyproject.toml)
        - Both are consistently applied across all overlays

        Note: Image tags and version labels are intentionally independent -
        image tags represent the CSS application version while version labels
        represent the project/tooling version.
        """
        if self.verbose:
            console.print("🔍 Validating version consistency...")

        overlays_dir = self.project_root / "overlays"
        if not overlays_dir.exists():
            console.print("No overlays directory found", style="yellow")
            return

        # Get expected project version from pyproject.toml
        expected_project_version = await self._get_project_version()

        async with self._get_client() as client:
            container = await self._get_yaml_container(client)
            issues = []

            for overlay_path in overlays_dir.iterdir():
                if overlay_path.is_dir():
                    overlay_name = overlay_path.name
                    kustomization_file = f"overlays/{overlay_name}/kustomization.yaml"

                    # Get image tag
                    try:
                        image_tag_result = await container.with_exec(
                            [
                                "yq",
                                '.images[] | select(.name == "docker.io/solidproject/community-server") | .newTag',
                                kustomization_file,
                            ]
                        ).stdout()
                        image_tag = (
                            image_tag_result.strip()
                            if image_tag_result.strip() != "null"
                            else None
                        )
                    except:
                        image_tag = None

                    # Get version label
                    try:
                        version_label_result = await container.with_exec(
                            [
                                "yq",
                                '.labels[0].pairs."app.kubernetes.io/version"',
                                kustomization_file,
                            ]
                        ).stdout()
                        version_label = (
                            version_label_result.strip()
                            if version_label_result.strip() != "null"
                            else None
                        )
                    except:
                        version_label = None

                    # Validate image tag presence
                    if not image_tag:
                        issues.append(f"{overlay_name}: missing image tag")
                    elif not self._validate_version_format(image_tag):
                        issues.append(
                            f"{overlay_name}: invalid image tag format '{image_tag}'"
                        )

                    # Validate version label presence and consistency with project version
                    if not version_label:
                        issues.append(f"{overlay_name}: missing version label")
                    elif version_label != expected_project_version:
                        issues.append(
                            f"{overlay_name}: version label '{version_label}' != project version '{expected_project_version}'"
                        )

            if issues:
                console.print("❌ Version consistency issues found:", style="red")
                for issue in issues:
                    console.print(f"  • {issue}", style="red")
                raise Exception(f"Found {len(issues)} version consistency issues")

            console.print("✅ Version consistency validation passed", style="green")

    async def generate_version_report(self) -> None:
        """Generate a report of current versions across all overlays."""
        if self.verbose:
            console.print("📊 Generating version report...")

        overlays_dir = self.project_root / "overlays"
        if not overlays_dir.exists():
            console.print("No overlays directory found", style="yellow")
            return

        async with self._get_client() as client:
            container = await self._get_yaml_container(client)

            console.print("\n📋 Version Report", style="bold blue")
            console.print("=" * 50)

            for overlay_path in overlays_dir.iterdir():
                if overlay_path.is_dir():
                    overlay_name = overlay_path.name
                    kustomization_file = f"overlays/{overlay_name}/kustomization.yaml"

                    # Get image tag
                    try:
                        image_tag_result = await container.with_exec(
                            [
                                "yq",
                                '.images[] | select(.name == "docker.io/solidproject/community-server") | .newTag',
                                kustomization_file,
                            ]
                        ).stdout()
                        image_tag = (
                            image_tag_result.strip()
                            if image_tag_result.strip() != "null"
                            else "not set"
                        )
                    except:
                        image_tag = "not set"

                    # Get version label
                    try:
                        version_label_result = await container.with_exec(
                            [
                                "yq",
                                '.labels[0].pairs."app.kubernetes.io/version"',
                                kustomization_file,
                            ]
                        ).stdout()
                        version_label = (
                            version_label_result.strip()
                            if version_label_result.strip() != "null"
                            else "not set"
                        )
                    except:
                        version_label = "not set"

                    # Get instance label for context
                    try:
                        instance_label_result = await container.with_exec(
                            [
                                "yq",
                                '.labels[0].pairs."app.kubernetes.io/instance"',
                                kustomization_file,
                            ]
                        ).stdout()
                        instance_label = (
                            instance_label_result.strip()
                            if instance_label_result.strip() != "null"
                            else "not set"
                        )
                    except:
                        instance_label = "not set"

                    # Display overlay info
                    console.print(f"\n🏷️ Overlay: {overlay_name}", style="bold")
                    console.print(f"   Instance: {instance_label}")
                    console.print(f"   Image Tag: {image_tag}")
                    console.print(f"   Version Label: {version_label}")

                    # Check completeness (both should be present but independent)
                    if image_tag != "not set" and version_label != "not set":
                        console.print("   Status: ✅ Complete", style="green")
                    else:
                        missing = []
                        if image_tag == "not set":
                            missing.append("image tag")
                        if version_label == "not set":
                            missing.append("version label")
                        console.print(
                            f"   Status: ⚠️ Missing {', '.join(missing)}", style="yellow"
                        )

            console.print("\n" + "=" * 50)
            console.print("📊 Report completed", style="bold blue")

    async def run_all_linting_parallel(self) -> None:
        """Run all linting checks in parallel for maximum speed."""
        if self.verbose:
            console.print("🔍 Running comprehensive linting in parallel...")

        import asyncio

        # Run all linting tasks in parallel
        tasks = [
            self.lint_yaml(),
            self.lint_python(),
            self.lint_markdown(),
            self.validate_kustomize(),
            self.security_scan(),
        ]

        try:
            await asyncio.gather(*tasks)
            console.print("✅ All parallel linting checks completed", style="green")
        except Exception as e:
            console.print(f"❌ Parallel linting failed: {e}", style="red")
            raise

    async def generate_all_overlays_parallel(self, output_dir: str) -> None:
        """Generate manifests for all overlays in parallel for maximum speed."""
        if self.verbose:
            console.print("🏗️ Generating all overlays in parallel...")

        overlays_dir = self.project_root / "overlays"
        if not overlays_dir.exists():
            console.print("No overlays directory found", style="yellow")
            return

        import asyncio

        # Get all overlay names
        overlay_names = [d.name for d in overlays_dir.iterdir() if d.is_dir()]

        if not overlay_names:
            console.print("No overlays found to generate", style="yellow")
            return

        # Generate all overlays in parallel
        tasks = [
            self.generate_overlay(overlay_name, output_dir)
            for overlay_name in overlay_names
        ]

        try:
            await asyncio.gather(*tasks)
            console.print("✅ All overlays generated in parallel", style="green")
        except Exception as e:
            console.print(f"❌ Parallel generation failed: {e}", style="red")
            raise

    async def _get_docs_container(self, client: dagger.Client) -> dagger.Container:
        """Get Python container with documentation dependencies installed.

        Creates a containerized Python environment with Poetry package manager
        and installs the project's documentation dependencies including MkDocs,
        mike, and related tools.

        Args:
            client: Dagger client instance for container operations.

        Returns:
            dagger.Container: Configured Python container with docs dependencies.
        """
        return (
            client.container()
            .from_("python:3.11-slim")
            .with_exec(["apt-get", "update"])
            .with_exec(["apt-get", "install", "-y", "curl", "git"])
            .with_exec(["pip", "install", "poetry"])
            .with_directory("/src", client.host().directory("."))
            .with_workdir("/src")
            .with_exec(["poetry", "config", "virtualenvs.create", "false"])
            .with_exec(["poetry", "install", "--with=docs"])
        )

    async def _get_project_version(self) -> str:
        """Get the current project version from pyproject.toml."""
        async with self._get_client() as client:
            container = await self._get_docs_container(client)
            version_result = await container.with_exec(
                ["poetry", "version", "--short"]
            ).stdout()
            return version_result.strip()

    async def build_docs(self) -> None:
        """Build documentation locally using MkDocs."""
        if self.verbose:
            console.print("🏗️ Building documentation...")

        async with self._get_client() as client:
            container = await self._get_docs_container(client)

            # Build documentation
            await container.with_exec(
                ["poetry", "run", "mkdocs", "build", "--strict"]
            ).stdout()

            # Copy built site back to host
            site_dir = self.project_root / "site"
            site_dir.mkdir(exist_ok=True)

            # Export the built site
            built_site = container.directory("site")
            await built_site.export(str(site_dir))

            console.print("✅ Documentation built successfully", style="green")
            console.print(f"📁 Built site available at: {site_dir}")

    async def serve_docs(self, port: int = 8000) -> None:
        """Serve documentation locally for development."""
        if self.verbose:
            console.print(f"🌐 Starting documentation server on port {port}...")

        async with self._get_client() as client:
            container = await self._get_docs_container(client)

            console.print(
                f"📚 Documentation server starting at http://localhost:{port}"
            )
            console.print("Press Ctrl+C to stop the server")

            # Serve documentation (this will run until interrupted)
            await container.with_exec(
                ["poetry", "run", "mkdocs", "serve", "--dev-addr", f"0.0.0.0:{port}"]
            ).stdout()

    async def deploy_docs(
        self,
        version: str | None = None,
        alias: str = "latest",
        set_default: bool = False,
        title: str | None = None,
    ) -> None:
        """Deploy documentation with version management using mike.

        Args:
            version: Version to deploy. If None, uses project version from pyproject.toml
            alias: Version alias (default: "latest")
            set_default: Whether to set this version as the default
            title: Version title for display. If None, uses version as title
        """
        if self.verbose:
            console.print("📚 Deploying documentation with mike...")

        # Get version if not provided
        if version is None:
            version = await self._get_project_version()
            if self.verbose:
                console.print(f"Using project version: {version}")

        # Use version as title if not provided
        if title is None:
            title = version

        async with self._get_client() as client:
            container = await self._get_docs_container(client)

            # Configure git for mike
            container = container.with_exec(
                ["git", "config", "user.name", "dagger-pipeline"]
            ).with_exec(["git", "config", "user.email", "pipeline@css-kustomize.local"])

            # Deploy with mike using explicit title
            deploy_cmd = [
                "poetry",
                "run",
                "mike",
                "deploy",
                "--update-aliases",
                "--title",
                title,
                version,
                alias,
            ]

            if self.verbose:
                console.print(
                    f"Deploying version {version} (title: {title}) with alias {alias}"
                )

            await container.with_exec(deploy_cmd).stdout()

            # Set as default if requested
            if set_default:
                if self.verbose:
                    console.print(f"Setting {alias} as default version")

                await container.with_exec(
                    ["poetry", "run", "mike", "set-default", alias]
                ).stdout()

            console.print(
                f"✅ Documentation deployed: {version} ({alias})", style="green"
            )

    async def list_doc_versions(self) -> None:
        """List all deployed documentation versions."""
        if self.verbose:
            console.print("📋 Listing documentation versions...")

        async with self._get_client() as client:
            container = await self._get_docs_container(client)

            try:
                versions_result = await container.with_exec(
                    ["poetry", "run", "mike", "list"]
                ).stdout()

                console.print(
                    "\n📚 Deployed Documentation Versions:", style="bold blue"
                )
                console.print("=" * 40)
                console.print(versions_result)
                console.print("=" * 40)

            except Exception as e:
                console.print(
                    "No versions deployed yet or git repository not initialized",
                    style="yellow",
                )
                if self.verbose:
                    console.print(f"Error: {e}", style="red")

    async def delete_doc_version(self, version: str) -> None:
        """Delete a specific documentation version.

        Args:
            version: Version to delete
        """
        if self.verbose:
            console.print(f"🗑️ Deleting documentation version: {version}")

        async with self._get_client() as client:
            container = await self._get_docs_container(client)

            await container.with_exec(
                ["poetry", "run", "mike", "delete", version]
            ).stdout()

            console.print(f"✅ Deleted documentation version: {version}", style="green")
