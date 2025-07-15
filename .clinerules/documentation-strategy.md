## Brief overview

Project-specific guidelines for documentation strategy, emphasizing minimal duplication, clear hierarchy, and "less is more" approach to maintain consistency across the CSS Kustomize project.

## Documentation hierarchy

- README.md should be concise and primarily reference /docs for detailed information
- Avoid duplicating content between README.md and documentation files
- Use README.md for quick overview, installation, and links to comprehensive docs
- Don't Keep detailed examples, workflows, and guides in the /docs directory structure
- Always document code first, versus creating files in /docs

## Content organization principles

- Follow "less is more" philosophy - provide essential information without overwhelming detail
- Use clear cross-references between files rather than duplicating content
- Maintain single source of truth for each topic in the appropriate /docs section
- README.md should serve as a navigation hub to detailed documentation

## Documentation maintenance

- When updating information, ensure it exists in only one authoritative location
- Use relative links to reference /docs content from README.md
- Regularly review for content duplication and consolidate when found
- Apply mdformat consistently across all markdown files per project standards

## Markdown formatting requirements

- Always run `poetry run mdformat .` after any Markdown file modifications
- Apply formatting before committing changes to maintain consistent documentation style
- Use mdformat as the primary formatting tool for all Markdown files in the project
- Format Markdown files immediately after making changes, not just before commits
- Include formatting step in any documentation-related development tasks
- Ensure formatting is applied to the entire project directory using the `.` argument

## Quality assurance

- Treat Markdown formatting as a mandatory step in the development process
- Maintain consistency with the project's existing mdformat configuration
- Apply formatting to all Markdown files, including documentation, README files, and Cline rules

## Project context

- This project uses comprehensive /docs structure with MkDocs for detailed documentation
- README.md should complement, not duplicate, the /docs content
- Users expect concise README with clear pointers to comprehensive documentation
- Maintain balance between accessibility and avoiding information overload
