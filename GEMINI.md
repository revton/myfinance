# Gemini Interaction Guidelines

## My Persona

I am a software engineer focused on applying software development best practices. I prefer solutions and tools that are open source.

## Development Workflow

- **Test-Driven Development (TDD):** Solutions should always be created from tests to ensure that maintenance never breaks the application.
- **Incremental Changes:** Apply changes in small, logical increments. Each change should be self-contained and address a single concern.
- **Commits:** After each incremental change, prepare a commit. This allows for a clean and traceable history.
- **GitFlow:** Adhere to the GitFlow branching model. All development work should be done on feature branches.
- **Branching:** Never commit or push changes directly to the `main` or `develop` branches. Always work on a feature branch (e.g., `feature/my-new-feature`).
- **Pull Requests:** Once a feature is complete, create a draft Pull Request (`--draft`) for review and merging. Do not merge it automatically.
- **Pushing:** Always confirm with me before pushing any changes to the remote repository.
- **Proposed Solution Summary:** Before applying any changes, present a summarized solution for approval.