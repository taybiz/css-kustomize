## Brief overview
Project-specific guidelines for automation and scripting preferences, emphasizing the use of Dagger over traditional shell scripting approaches for consistency, cross-platform compatibility, and better error handling.

## Automation tool preferences
- Always prefer Dagger over shell, bash, or PowerShell scripts for automation tasks
- Use Dagger's Python SDK when implementing pipeline logic and automation workflows
- Leverage Dagger's container-based approach for consistent execution environments
- Avoid creating standalone shell scripts for CI/CD, build processes, or deployment automation

## Development workflow
- When implementing new automation features, structure them as Dagger functions in the dagger_pipeline module
- Use Dagger's caching capabilities to optimize pipeline performance
- Implement automation logic in Python within the Dagger context rather than external scripts

## Scripting guidelines
- Replace any existing shell scripts with equivalent Dagger implementations
- Use Dagger containers for executing commands that would traditionally be done in shell scripts
- Maintain cross-platform compatibility by avoiding platform-specific shell commands

## Project context
- This project already uses Dagger for pipeline automation (see dagger_pipeline/ directory)
- Existing decision documented in memory-bank/decisions/001-dagger-over-github-actions.md supports this approach
- Consistency with project's containerized and cloud-native architecture
