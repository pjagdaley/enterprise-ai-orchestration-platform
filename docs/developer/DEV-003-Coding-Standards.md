# DEV-003 – Coding Standards

## 1. Purpose

This document defines the coding standards for the Enterprise AI Orchestration Platform.

The objective is to ensure that all contributors produce code that is consistent, maintainable, testable, and production-ready. Following a common coding standard improves readability, simplifies code reviews, and reduces long-term maintenance costs.

These standards apply to all Python source code within the project.

---

## 2. Development Principles

All code should follow these principles:

- Clean Architecture
- Domain-Driven Design (DDD)
- SOLID Principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- YAGNI (You Aren't Gonna Need It)
- Separation of Concerns

Code should optimize for readability rather than cleverness.

---

## 3. General Guidelines

Developers should:

- Write self-explanatory code.
- Keep methods focused on a single responsibility.
- Prefer composition over inheritance.
- Avoid unnecessary abstractions.
- Minimize code duplication.
- Keep business logic independent of infrastructure.

---

## 4. Python Style Guide

The project follows:

- PEP 8
- PEP 257
- Type Hinting (PEP 484)

Maximum line length:

```text
100 characters
```

Indentation:

```text
4 spaces
```

Tabs are not permitted.

---

## 5. Naming Conventions

### Modules

```python
document_service.py

firestore_service.py

embedding_service.py
```

---

### Packages

```text
application

domain

infrastructure

bootstrap
```

---

### Classes

```python
DocumentService

ChatController

EmbeddingService

QdrantRepository
```

Always use PascalCase.

---

### Functions

```python
create_document()

search_documents()

generate_embeddings()

load_configuration()
```

Always use snake_case.

---

### Variables

```python
document_id

user_query

search_results

embedding_model
```

Avoid abbreviations unless widely understood.

---

### Constants

```python
MAX_RESULTS

DEFAULT_TIMEOUT

VECTOR_DIMENSION

SUPPORTED_EXTENSIONS
```

Always use uppercase with underscores.

---

### Private Members

```python
_validate_request()

_load_configuration()

_internal_state
```

Prefix internal members with a single underscore.

---

## 6. Type Hints

All public methods should include type hints.

Example:

```python
def search(
    query: str,
    top_k: int
) -> list[SearchResult]:
    ...
```

Avoid using `Any` unless absolutely necessary.

---

## 7. Documentation

Every public class should include a docstring.

Example:

```python
class DocumentService:
    """
    Handles document ingestion and retrieval.
    """
```

Every public method should explain:

- Purpose
- Parameters
- Return value
- Exceptions (if applicable)

---

## 8. Function Design

Functions should:

- Perform one task.
- Be easy to understand.
- Avoid deeply nested logic.
- Return early when appropriate.
- Minimize side effects.

Prefer:

```python
if not document:
    return None
```

instead of deeply nested conditionals.

---

## 9. Class Design

Classes should:

- Have a single responsibility.
- Be small and cohesive.
- Depend on abstractions.
- Avoid excessive constructor parameters.

Prefer dependency injection over creating dependencies internally.

---

## 10. Error Handling

Raise meaningful exceptions.

Example:

```python
raise DocumentNotFoundException(document_id)
```

Avoid:

```python
raise Exception("Something went wrong")
```

Catch exceptions only when they can be handled appropriately.

---

## 11. Logging

Use structured logging.

Example:

```python
logger.info(
    "Document indexed successfully",
    extra={
        "document_id": document_id,
        "chunk_count": chunk_count
    }
)
```

Do not use:

```python
print("Debug")
```

Never log:

- Passwords
- Tokens
- Secrets
- Personally identifiable information (PII)

---

## 12. Configuration

Never hardcode configuration.

Incorrect:

```python
HOST = "localhost"
```

Correct:

```python
settings.qdrant_host
```

Configuration should be loaded through the Configuration Service.

---

## 13. Dependency Injection

Dependencies should be injected.

Avoid:

```python
service = FirestoreService()
```

Prefer:

```python
class ChatService:

    def __init__(
        self,
        firestore_service: FirestoreService
    ):
        self.firestore_service = firestore_service
```

---

## 14. API Development

API endpoints should:

- Validate input.
- Return appropriate HTTP status codes.
- Delegate business logic to application services.
- Avoid database access.

Controllers should remain thin.

---

## 15. Testing Expectations

New functionality should include:

- Unit tests.
- Integration tests (where appropriate).
- Edge case coverage.
- Error scenario validation.

Critical business logic should not be merged without tests.

---

## 16. Code Review Checklist

Reviewers should verify:

- Naming conventions.
- Type hints.
- Docstrings.
- Unit tests.
- Logging.
- Error handling.
- Architecture compliance.
- Security considerations.

---

## 17. Common Anti-Patterns

Avoid:

- God classes.
- Long methods.
- Circular dependencies.
- Copy-and-paste code.
- Magic numbers.
- Hardcoded credentials.
- Business logic in API controllers.
- Infrastructure access from the domain layer.

---

## 18. Example

Good:

```python
class SearchService:

    def search(
        self,
        query: str
    ) -> SearchResponse:

        documents = self.repository.search(query)

        return SearchResponse(documents)
```

Poor:

```python
class Search:

    def doEverything(self, q):

        # many unrelated responsibilities

        ...
```

---

## 19. Related Documents

- DEV-002 – Project Structure
- DEV-004 – Dependency Injection
- DEV-005 – Error Handling
- DEV-006 – Testing Strategy
- SERVICE-007 – Configuration Service
- SERVICE-008 – Logging Service

---

## Metadata

| Property | Value |
|----------|-------|
| Document ID | DEV-003 |
| Title | Coding Standards |
| Category | Developer Documentation |
| Audience | Software Developers |
| Version | 1.0 |
| Status | Active |