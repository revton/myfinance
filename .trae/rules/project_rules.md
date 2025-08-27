# Qwen Code Interaction Guidelines

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

## Architectural Principles

To ensure the project is scalable, maintainable, and ready for future expansions (like mobile applications), the following architectural principles must be followed:

- **Backend-centric Logic:** All business logic, data validation, and data access must be centralized in the backend API (the `src` directory). The backend is the single source of truth.
- **Decoupled Frontend:** The frontend (the `frontend` directory) is responsible for the user interface (UI) and user experience (UX). It must communicate with the backend exclusively through the defined RESTful API. It **must not** have direct access to the database or other backend-only services (e.g., direct Supabase calls).
- **Platform Agnostic API:** The API should be designed to be platform-agnostic, ensuring that any client (web, mobile, etc.) can consume it and receive consistent behavior and data.
- **Clear Separation of Concerns:** A strict separation must be maintained between the data layer (database models and access), the business logic layer (backend API services and routes), and the presentation layer (frontend components).

## Context7 Integration

- **Library Documentation:** When incorporating or referencing external libraries or frameworks, utilize the MCP Context7 tool to fetch the most up-to-date and relevant documentation. This ensures accuracy and helps in understanding the best practices associated with the library.
- **Guided Implementation:** Use Context7 to guide the implementation process, especially when dealing with complex libraries or when specific functionalities need to be integrated. This helps in reducing errors and speeds up the development process.
- **Code Snippets and Examples:** Leverage code snippets and examples provided by Context7 to ensure that the implementation aligns with the recommended usage patterns of the libraries being used.