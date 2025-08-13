# Gemini Interaction Guidelines

## My Persona

I am a software engineer focused on applying software development best practices. I prefer solutions and tools that are open source.

## Development Workflow

- **Test-Driven Development (TDD):** Solutions should always be created from tests to ensure that maintenance never breaks the application.
- **Incremental Changes:** Apply changes in small, logical increments. Each change should be self-contained and address a single concern.
- **Commits:** After each incremental change, prepare a commit. This allows for a clean and traceable history.
- **GitFlow:** Adhere to the GitFlow branching model. All development work should be done on feature branches.
- **Branching:** Always create a new branch for any changes. NEVER commit directly to the `main` or `develop` branches. Use the following naming conventions:
    - For bug fixes originating from `develop`: `bugfix/your-bug-description`
    - For new functionalities: `feature/your-feature-name`
    - For urgent corrections directly on `main`: `hotfix/your-hotfix-description`
- **Pull Requests:** Once a feature is complete, create a draft Pull Request (`--draft`) for review and merging, always targeting the `develop` branch. Do not merge it automatically.
- **Pushing:** Always confirm with me before pushing any changes to the remote repository.
- **Proposed Solution Summary:** Before applying any changes, present a summarized solution for approval.