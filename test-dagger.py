#!/usr/bin/env python3
"""Simple test script to verify Dagger pipeline functionality."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔍 {description}...")
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def check_poetry() -> bool:
    """Check if Poetry is available."""
    try:
        subprocess.run(["poetry", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    """Main test function."""
    print("🚀 Testing Dagger Pipeline Setup")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Please run from project root.")
        sys.exit(1)

    # Check Poetry availability
    has_poetry = check_poetry()

    if has_poetry:
        print("✅ Poetry detected - using Poetry workflow")
        tests = [
            (["poetry", "--version"], "Poetry installation"),
            (["poetry", "install"], "Installing dependencies"),
            (["poetry", "run", "dagger-pipeline", "--help"], "Dagger pipeline CLI"),
        ]
        next_steps = [
            "  poetry run dagger-pipeline lint --help",
            "  poetry run dagger-pipeline ci",
        ]
    else:
        print("⚠️  Poetry not found - using pip workflow")
        tests = [
            (
                ["python", "-m", "pip", "install", "-e", "."],
                "Installing package with pip",
            ),
            (
                ["python", "-m", "pip", "install", "yamllint", "ruff", "pre-commit"],
                "Installing lint dependencies",
            ),
            (["dagger-pipeline", "--help"], "Dagger pipeline CLI"),
        ]
        next_steps = ["  dagger-pipeline lint --help", "  dagger-pipeline ci"]

    success_count = 0
    for cmd, description in tests:
        if run_command(cmd, description):
            success_count += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {success_count}/{len(tests)} passed")

    if success_count == len(tests):
        print("🎉 All tests passed! Dagger pipeline is ready to use.")
        print("\nNext steps:")
        for step in next_steps:
            print(step)
    else:
        print("❌ Some tests failed. Please check the errors above.")
        if not has_poetry:
            print("\n💡 Consider installing Poetry for better dependency management:")
            print("   https://python-poetry.org/docs/#installation")
        sys.exit(1)


if __name__ == "__main__":
    main()
