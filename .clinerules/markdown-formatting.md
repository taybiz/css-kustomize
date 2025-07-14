## Brief overview

Project-specific guidelines for Markdown file formatting and quality assurance, emphasizing the use of mdformat for consistent Markdown formatting across the CSS Kustomize project.

## Markdown formatting requirements

- Always run `poetry run mdformat .` after any Markdown file modifications
- Apply formatting before committing changes to maintain consistent documentation style
- Use mdformat as the primary formatting tool for all Markdown files in the project

## Development workflow

- Format Markdown files immediately after making changes, not just before commits
- Include formatting step in any documentation-related development tasks
- Ensure formatting is applied to the entire project directory using the `.` argument

## Quality assurance

- Treat Markdown formatting as a mandatory step in the development process
- Maintain consistency with the project's existing mdformat configuration
- Apply formatting to all Markdown files, including documentation, README files, and Cline rules

## Project context

- This project uses Poetry for dependency management and mdformat for Markdown formatting
- The formatting requirement applies to all Markdown files in the docs/ directory, .clinerules/, and root-level files
- Consistent formatting supports the project's emphasis on high-quality documentation and automation
