# DEV-002 – Project Structure

## 1. Purpose

This document describes the project structure of the Enterprise AI Orchestration Platform.

It explains how the source code is organized, the responsibilities of each package, and the architectural principles governing the codebase. Understanding the project structure enables developers to locate functionality quickly, maintain separation of concerns, and implement new features consistently.

---

## 2. Architectural Principles

The project structure follows the principles of:

- Clean Architecture
- Domain-Driven Design (DDD)
- SOLID Principles
- Separation of Concerns
- Dependency Injection
- Modular Design
- API-First Development

The architecture separates business logic from infrastructure, ensuring the application remains maintainable, testable, and extensible.

---

## 3. High-Level Repository Structure

```text
enterprise-ai-orchestration-platform/

├── app/
├── config/
├── docs/
├── sample-data/
├── scripts/
├── tests/
│
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 4. Source Code Organization

The application's source code resides under the **app** directory.

```text
app/

├── api/
├── application/
├── bootstrap/
├── core/
├── domain/
├── infrastructure/
└── main.py
```

Each package has a single responsibility.

---

## 5. Package Responsibilities

### api

Responsible for exposing REST endpoints.

Contains:

- Routers
- Request models
- Response models
- API versioning
- Endpoint validation

Typical responsibilities:

- HTTP request processing
- Input validation
- Response generation
- Status codes

---

### application

Contains application use cases.

Responsibilities include:

- Workflow orchestration
- Application services
- Business use cases
- Coordination between domain and infrastructure

Application services do not directly interact with external systems.

---

### bootstrap

Responsible for application startup.

Contains:

- Application factory
- Dependency registration
- Middleware registration
- Exception handlers
- OpenAPI configuration
- Lifespan events

This package initializes the platform.

---

### core

Contains shared platform functionality.

Examples include:

- Configuration
- Logging
- Constants
- Exceptions
- Utility functions

The core package should remain independent of business domains.

---

### domain

Contains business rules.

Examples:

```text
domain/

agents/

models/

entities/

value_objects/

repositories/

services/
```

Responsibilities:

- Business entities
- Domain models
- Interfaces
- Domain services
- Business validation

The domain layer should not depend on infrastructure.

---

### infrastructure

Contains implementations of external integrations.

Examples:

```text
infrastructure/

services/

repositories/

clients/

storage/

vector/

search/

llm/
```

Responsibilities:

- Qdrant
- Firestore
- Vertex AI
- Gemini
- OpenSearch
- Google Cloud Storage
- External APIs

Infrastructure implements interfaces defined by the domain layer.

---

## 6. Layered Architecture

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
                    │
                    ▼
           External Services
```

Dependencies always point downward.

---

## 7. Dependency Rules

Allowed:

```text
API
 ↓
Application
 ↓
Domain
 ↓
Infrastructure
```

Not allowed:

```text
Infrastructure
      │
      ▼
Application

Domain
      │
      ▼
API
```

Business rules must remain independent of external technologies.

---

## 8. Feature Organization

Each feature should contain its own components.

Example:

```text
application/

chat/

documents/

ingestion/

search/
```

Each feature may include:

- Service
- DTOs
- Validators
- Commands
- Queries

This organization improves modularity.

---

## 9. Infrastructure Organization

Infrastructure components are grouped by responsibility.

Example:

```text
infrastructure/

llm/

search/

storage/

database/

messaging/
```

Each integration is isolated from the rest of the application.

---

## 10. Naming Conventions

Directories:

```text
snake_case
```

Python modules:

```text
snake_case.py
```

Classes:

```text
PascalCase
```

Functions:

```text
snake_case()
```

Constants:

```text
UPPER_CASE
```

Environment variables:

```text
UPPER_CASE
```

---

## 11. Where New Code Should Go

| Requirement | Package |
|------------|---------|
| REST Endpoint | api |
| Business Workflow | application |
| Business Rule | domain |
| External API | infrastructure |
| Shared Utility | core |
| Startup Configuration | bootstrap |

Developers should place new code in the appropriate layer to maintain architectural consistency.

---

## 12. Testing Structure

Tests mirror the application structure.

Example:

```text
tests/

api/

application/

domain/

infrastructure/
```

Each package should contain corresponding unit and integration tests.

---

## 13. Documentation Structure

Project documentation is organized as:

```text
docs/

architecture/

workflows/

agents/

tools/

services/

developer/

diagrams/
```

Documentation should evolve alongside the code.

---

## 14. Best Practices

Developers should:

- Keep modules focused.
- Avoid circular dependencies.
- Separate interfaces from implementations.
- Keep business logic out of controllers.
- Avoid direct infrastructure dependencies in the domain layer.
- Follow dependency injection principles.
- Write unit tests for new functionality.

---

## 15. Common Mistakes

Avoid:

- Business logic inside API controllers.
- Direct database access from API endpoints.
- Infrastructure dependencies in domain models.
- Large utility classes.
- Circular imports.
- Duplicate business rules.

---

## 16. Example Request Flow

```text
HTTP Request
      │
      ▼
API Router
      │
      ▼
Application Service
      │
      ▼
Domain Logic
      │
      ▼
Infrastructure Service
      │
      ▼
External System
      │
      ▼
Response
```

This flow illustrates the intended interaction between layers.

---

## 17. Related Documents

- DEV-001 – Development Environment Setup
- DEV-003 – Coding Standards
- DEV-004 – Dependency Injection
- Architecture Documentation
- Service Documentation

---

## Metadata

| Property | Value |
|----------|-------|
| Document ID | DEV-002 |
| Title | Project Structure |
| Category | Developer Documentation |
| Audience | Software Developers |
| Version | 1.0 |
| Status | Active |