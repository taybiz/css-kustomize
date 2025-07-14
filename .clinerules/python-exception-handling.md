## Brief overview

Project-specific guidelines for proper Python exception handling, emphasizing the use of exception chaining to maintain error context and comply with Ruff B904 rule.

## Exception chaining requirements

- Always use `raise ... from err` when re-raising exceptions within except blocks
- Use `raise ... from None` only when explicitly suppressing the original exception context
- Maintain the original exception chain to preserve debugging information

## Exception handling patterns

- When catching and re-raising with additional context: `raise CustomException("message") from original_exception`
- When catching subprocess errors: `raise Exception(f"Operation failed: {e}") from e`
- Avoid bare `raise Exception("message")` within except blocks without proper chaining

## Code quality compliance

- Ensure all exception handling passes Ruff B904 checks
- Run `poetry run ruff check . --select B904` to validate exception handling
- Fix any B904 violations by adding proper exception chaining

## Development workflow

- Check exception handling during code review
- Validate with Ruff linting before committing changes
- Maintain consistent exception chaining patterns across the codebase

## Project context

- This project uses Ruff for code quality enforcement including exception handling rules
- Exception chaining helps with debugging in the Dagger pipeline and release management modules
- Proper exception handling supports the project's emphasis on robust automation workflows
