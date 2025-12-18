# PROJECT_BRIEF.md

## Project Overview

| Field | Value |
|-------|-------|
| **Name** | TodoAPI |
| **Type** | REST API |
| **Goal** | A minimal REST API for managing todo items with SQLite persistence |
| **Timeline** | 2 days |
| **Team Size** | 1 |

## Target Users

- Frontend developers needing a backend
- Developers learning API patterns
- Anyone needing a simple task management API

## MVP Features (Must Have)

1. Create a todo item (POST /todos)
2. List all todo items (GET /todos)
3. Get a single todo item (GET /todos/{id})
4. Update a todo item (PUT /todos/{id})
5. Delete a todo item (DELETE /todos/{id})
6. Mark todo as complete (PATCH /todos/{id}/complete)

## Nice-to-Have (v2)

- User authentication
- Multiple todo lists
- Due dates and reminders
- Tags/categories

## Tech Stack

### Must Use
- Python 3.11+
- FastAPI (web framework)
- SQLite (database)
- Pydantic (validation)
- SQLAlchemy (ORM)

### Cannot Use
- Flask (use FastAPI)
- Raw SQL (use SQLAlchemy)
- JSON file storage (use SQLite)

## Constraints

- RESTful API design
- JSON request/response format
- OpenAPI documentation auto-generated
- 100% test coverage
- All endpoints return proper HTTP status codes
