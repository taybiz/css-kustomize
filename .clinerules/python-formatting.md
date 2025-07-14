## Brief overview

Project-specific guidelines for Python code formatting and quality assurance, emphasizing the use of Ruff for consistent code formatting across the CSS Kustomize project.

## Code formatting requirements

- Always run `poetry run ruff format .` after any Python code modifications
- Apply formatting before committing changes to maintain consistent code style
- Use Ruff as the primary formatting tool for all Python files in the project

## Development workflow

- Format Python code immediately after making changes, not just before commits
- Include formatting step in any Python-related development tasks
- Ensure formatting is applied to the entire project directory using the `.` argument

## Quality assurance

- Treat code formatting as a mandatory step in the development process
- Maintain consistency with the project's existing Ruff configuration
- Apply formatting to all Python files, including pipeline modules, scripts, and configuration files

## Project context

- This project uses Poetry for dependency management and Ruff for code formatting
- The formatting requirement applies to all Python code in the dagger_pipeline/ directory and related modules
- Consistent formatting supports the project's emphasis on automation and code quality
