# Documentation Strategy Patterns

## Overview

Project-specific guidelines for documentation strategy, emphasizing minimal duplication, clear hierarchy, and "less is more" approach to maintain consistency across the CSS Kustomize project.

## Documentation Hierarchy Principles

### README.md vs /docs Structure

- **README.md**: Concise overview serving as navigation hub

  - Quick project overview and purpose
  - Installation instructions
  - Links to comprehensive documentation in /docs
  - Avoid detailed examples or extensive guides

- **/docs Directory**: Comprehensive detailed documentation

  - Complete user guides and tutorials
  - Detailed configuration examples
  - Architecture and design decisions
  - Developer guides and API references

### Single Source of Truth

- Each topic should exist in only one authoritative location
- Use cross-references and links rather than duplicating content
- When updating information, ensure it exists in one place only
- Regularly audit for content duplication and consolidate

## Content Organization Philosophy

### "Less is More" Approach

- Provide essential information without overwhelming detail
- Focus on actionable guidance over exhaustive coverage
- Use clear, concise language and structure
- Balance accessibility with avoiding information overload

### Cross-Reference Strategy

- Use relative links to reference /docs content from README.md
- Maintain clear navigation paths between related topics
- Create logical information hierarchies
- Link related concepts across different sections

## Documentation Maintenance Workflow

### Markdown Formatting Requirements

**Mandatory Process**: Always run `poetry run mdformat .` after any Markdown file modifications

- Apply formatting before committing changes
- Use mdformat as the primary formatting tool for all Markdown files
- Format immediately after making changes, not just before commits
- Include formatting step in any documentation-related development tasks
- Ensure formatting is applied to entire project directory using `.` argument

### Quality Assurance Standards

- Treat Markdown formatting as mandatory development step
- Maintain consistency with project's existing mdformat configuration
- Apply formatting to all Markdown files including:
  - Documentation files in /docs
  - README files at all levels
  - Cline rules in .clinerules
  - Memory bank documentation

### Content Review Process

- Regularly review for content duplication
- Ensure README.md complements rather than duplicates /docs content
- Validate that cross-references remain accurate
- Update navigation and index files when adding new content

## Implementation Guidelines

### Code-First Documentation

- Always document code first versus creating standalone files in /docs
- Extract documentation from well-documented code when possible
- Keep code comments and documentation synchronized
- Use inline documentation for immediate context

### Project Context Integration

- Leverage comprehensive /docs structure with MkDocs
- Ensure README.md serves as effective entry point
- Maintain balance between quick access and comprehensive coverage
- Support both new users and experienced developers

## Best Practices

### Writing Guidelines

- Use clear, descriptive headings and structure
- Include practical examples and code snippets where helpful
- Maintain consistent tone and style across all documentation
- Focus on user needs and common use cases

### Maintenance Practices

- Update documentation as part of feature development
- Review and refresh content regularly
- Remove or consolidate outdated information
- Keep external links current and functional

### Navigation and Discovery

- Maintain clear index and navigation structures
- Use consistent naming conventions for files and sections
- Provide multiple paths to important information
- Support both linear reading and random access patterns

## Integration with Development Workflow

### Pre-commit Requirements

- Markdown formatting validation as part of pre-commit hooks
- Documentation completeness checks for new features
- Link validation for internal and external references
- Consistency checks across documentation hierarchy

### Release Process

- Update documentation as part of release preparation
- Validate that README.md accurately reflects current capabilities
- Ensure /docs content is current and comprehensive
- Review and update navigation and index files

## Measuring Success

### Quality Indicators

- Minimal content duplication across documentation
- Clear, navigable information architecture
- Consistent formatting and style
- User feedback indicating effective information discovery

### Maintenance Metrics

- Regular documentation updates aligned with code changes
- Consistent application of formatting standards
- Effective cross-referencing without broken links
- Balanced content distribution between README.md and /docs

## Cross-References

- See `.clinerules/documentation-strategy.md` for the original rule specification
- Related: [`python-code-quality.md`](python-code-quality.md) for formatting requirements
- Related: [`development-workflow.md`](../workflows/development-workflow.md) for workflow integration

______________________________________________________________________

*This pattern supports the project's emphasis on maintainable, user-friendly documentation that scales with project growth while avoiding information overload.*
