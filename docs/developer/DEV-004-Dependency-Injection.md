# DEV-004 – Dependency Injection

## 1. Purpose

This document describes the Dependency Injection (DI) strategy used in the Enterprise AI Orchestration Platform.

Dependency Injection is a fundamental architectural principle that promotes loose coupling, improves testability, and enables components to be developed and maintained independently.

The platform uses constructor-based dependency injection together with a centralized application bootstrap process to create and manage application dependencies.

---

## 2. Objectives

The Dependency Injection architecture aims to:

- Reduce coupling between components.
- Improve unit testing.
- Centralize object creation.
- Improve maintainability.
- Simplify dependency management.
- Support future scalability.

---

## 3. Why Dependency Injection?

Without Dependency Injection:

```text
ChatService
     │
     ├── FirestoreService()
     ├── GeminiService()
     ├── QdrantService()
     └── OpenSearchService()
```

The service becomes tightly coupled to concrete implementations.

With Dependency Injection:

```text
ChatService
     ▲
     │
Application Bootstrap
     │
     ├── FirestoreService
     ├── GeminiService
     ├── QdrantService
     └── OpenSearchService
```

The service depends only on its required collaborators, not on how they are created.

---

## 4. Dependency Injection Principles

The platform follows these principles:

- Constructor Injection.
- Explicit dependencies.
- Single responsibility.
- Interface-oriented design.
- No hidden dependencies.
- Stateless services where practical.

---

## 5. Application Startup

Dependency creation occurs during application startup.

```text
Application Startup
        │
        ▼
Configuration Service
        │
        ▼
Application Factory
        │
        ▼
Create Infrastructure Services
        │
        ▼
Create Application Services
        │
        ▼
Register API Routes
        │
        ▼
Application Ready
```

---

## 6. Dependency Flow

The platform follows this dependency hierarchy.

```text
API Layer
      │
      ▼
Application Layer
      │
      ▼
Domain Layer
      │
      ▼
Infrastructure Layer
```

Dependencies flow in one direction only.

---

## 7. Constructor Injection

Preferred approach:

```python
class ChatService:

    def __init__(
        self,
        gemini_service: GeminiService,
        firestore_service: FirestoreService,
        qdrant_service: QdrantService,
        open_search_service: OpenSearchService
    ):
        self._gemini_service = gemini_service
        self._firestore_service = firestore_service
        self._qdrant_service = qdrant_service
        self._open_search_service = open_search_service
```

Dependencies are supplied externally rather than created inside the class.

---

## 8. Avoid Direct Instantiation

Avoid:

```python
class ChatService:

    def search(self):

        qdrant = QdrantService()

        return qdrant.search(...)
```

Problems:

- Difficult to test.
- Tight coupling.
- Hidden dependencies.
- Hard to replace implementations.

---

## 9. Application Factory

The Application Factory is responsible for:

- Loading configuration.
- Creating infrastructure services.
- Creating application services.
- Registering middleware.
- Registering exception handlers.
- Registering API routers.

Example:

```text
Application Factory
        │
        ├── Configuration
        ├── Logging
        ├── Firestore
        ├── Gemini
        ├── Qdrant
        ├── OpenSearch
        └── Chat Service
```

---

## 10. Service Lifetime

Most platform services are implemented as singletons.

Examples include:

- Configuration Service
- Logging Service
- Gemini Service
- Firestore Service
- Qdrant Service
- OpenSearch Service
- Google Cloud Storage Service

Stateless services can safely be reused across requests.

---

## 11. FastAPI Integration

FastAPI dependencies should be injected rather than created inside route handlers.

Example:

```python
@router.post("/chat")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    return await chat_service.chat(request)
```

This keeps controllers lightweight and focused on HTTP concerns.

---

## 12. Testing Benefits

Dependency Injection makes testing easier.

Example:

```text
ChatService
      │
      ├── Mock Gemini
      ├── Mock Firestore
      ├── Mock Qdrant
      └── Mock OpenSearch
```

Developers can replace real services with test doubles during unit tests.

---

## 13. Common Mistakes

Avoid:

- Creating services inside business logic.
- Using global mutable state.
- Passing configuration throughout the application.
- Hidden dependencies.
- Circular dependencies.
- Service locator patterns.

---

## 14. Best Practices

Developers should:

- Inject all external dependencies.
- Keep constructors explicit.
- Depend on abstractions where possible.
- Use immutable configuration.
- Keep services stateless.
- Register dependencies in one place.

---

## 15. Dependency Graph

```text
API Router
      │
      ▼
Chat Service
      │
      ├─────────────┐
      ▼             ▼
Gemini Service   Firestore Service
      │             │
      ▼             ▼
Vertex AI     Cloud Firestore

      │
      ▼
Qdrant Service
      │
      ▼
Qdrant

      │
      ▼
OpenSearch Service
      │
      ▼
OpenSearch
```

---

## 16. Related Documents

- DEV-002 – Project Structure
- DEV-003 – Coding Standards
- DEV-005 – Error Handling
- SERVICE-007 – Configuration Service
- SERVICE-008 – Logging Service

---

## Metadata

| Property | Value |
|----------|-------|
| Document ID | DEV-004 |
| Title | Dependency Injection |
| Category | Developer Documentation |
| Audience | Software Developers |
| Version | 1.0 |
| Status | Active |