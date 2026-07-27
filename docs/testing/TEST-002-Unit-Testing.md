# TEST-002 – Unit Testing

## 1. Purpose

This document defines the unit testing standards, practices, and implementation guidelines for the Enterprise AI Orchestration Platform.

Unit testing verifies that individual software components function correctly in isolation. Each unit test should execute quickly, independently, deterministically, and without relying on external infrastructure.

The objective is to detect defects early, improve code quality, and provide confidence during refactoring.

---

# 2. Objectives

The unit testing strategy aims to:

- Verify correctness of individual components
- Detect regressions early
- Improve maintainability
- Support continuous integration
- Reduce production defects
- Encourage modular design
- Enable safe refactoring

---

# 3. Scope

Unit testing applies to all application components including:

- Domain Models
- Value Objects
- Domain Services
- Application Services
- FastAPI Controllers
- Business Rules
- Utility Classes
- Configuration
- Middleware
- Exception Handlers
- Dependency Injection
- Validators
- Mappers
- LangGraph Nodes
- Tool Adapters

External systems such as Firestore, Qdrant, OpenSearch, Gemini, and Google Cloud Storage must be mocked during unit tests.

---

# 4. Unit Testing Principles

The platform follows these principles:

- Test one behavior per test case
- Keep tests independent
- Avoid shared mutable state
- Mock external dependencies
- Prefer deterministic assertions
- Use descriptive test names
- Execute tests in any order
- Keep execution time low

---

# 5. Test Architecture

```text
                Unit Test
                    │
                    ▼
          Component Under Test
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
     Mock        Fake Data     Assertions
                    │
                    ▼
              Test Result
```

---

# 6. Recommended Tools

| Purpose | Tool |
|----------|------|
| Test Framework | Pytest |
| Mocking | unittest.mock |
| Fixtures | pytest fixtures |
| Coverage | pytest-cov |
| Async Testing | pytest-asyncio |
| HTTP Testing | FastAPI TestClient |
| Data Generation | Faker |

---

# 7. Project Structure

```text
tests/

unit/
│
├── api/
├── application/
├── bootstrap/
├── core/
├── domain/
├── infrastructure/
├── services/
└── utils/
```

Example:

```text
tests/unit/application/test_chat_service.py

tests/unit/domain/test_document.py

tests/unit/core/test_configuration.py
```

---

# 8. Naming Conventions

Test classes:

```text
TestChatService
TestDocumentParser
TestSearchService
```

Test methods:

```text
test_should_return_documents_when_query_exists()

test_should_raise_exception_when_document_missing()

test_should_generate_embeddings()
```

Test names should describe expected behavior rather than implementation details.

---

# 9. Arrange-Act-Assert Pattern

Every test should follow the Arrange-Act-Assert (AAA) pattern.

Example:

```python
def test_should_return_document():

    # Arrange
    service = DocumentService(mock_repository)

    # Act
    result = service.get_document("DOC-001")

    # Assert
    assert result.id == "DOC-001"
```

---

# 10. Mocking Strategy

External dependencies should always be mocked.

Examples:

- Firestore
- Qdrant
- OpenSearch
- Gemini
- Vertex AI
- Google Cloud Storage
- External REST APIs
- MCP Servers

Example:

```python
@patch("app.infrastructure.qdrant_service.QdrantService.search")
def test_search(mock_search):

    mock_search.return_value = []

    ...
```

---

# 11. Fixtures

Reusable fixtures should be stored in:

```text
tests/conftest.py
```

Typical fixtures include:

- Settings
- Fake users
- Documents
- Sessions
- Search results
- Authentication tokens

Example:

```python
@pytest.fixture
def sample_document():

    return Document(
        id="DOC-001",
        title="Architecture Guide"
    )
```

---

# 12. Testing FastAPI Services

Services should be tested independently from controllers.

Example:

```python
service = ChatService(
    repository=mock_repository,
    llm=mock_llm
)

response = service.chat(request)

assert response.answer is not None
```

The objective is to isolate business logic from HTTP concerns.

---

# 13. Testing Domain Models

Domain models should verify:

- Validation
- Invariants
- Business rules
- Equality
- Value object behavior

Example:

```python
document = Document(...)

assert document.status == DocumentStatus.READY
```

---

# 14. Testing LangGraph Nodes

Each workflow node should be tested independently.

Verify:

- Input state
- Output state
- State transitions
- Error handling
- Tool invocation decisions

Example:

```python
result = retrieval_node(state)

assert result.documents
```

---

# 15. Testing Utilities

Utility tests include:

- Date formatting
- JSON serialization
- File utilities
- Configuration loading
- String utilities
- Token counting
- Chunk generation

Utility functions should produce deterministic results.

---

# 16. Code Coverage

Minimum coverage expectations:

| Component | Target |
|-----------|--------|
| Domain | 95% |
| Services | 90% |
| Utilities | 90% |
| API Controllers | 80% |
| Overall | ≥80% |

Coverage should emphasize meaningful assertions rather than simply executing code.

---

# 17. Test Data

Unit tests should use:

- Small datasets
- Deterministic values
- Isolated fixtures
- No production data

Avoid:

- Shared databases
- Real cloud services
- Network access
- Time-dependent behavior

---

# 18. Common Anti-Patterns

Avoid:

- Sleeping during tests
- Real API calls
- Shared mutable fixtures
- Large datasets
- Hardcoded environment dependencies
- Testing multiple behaviors in one test
- Order-dependent execution

---

# 19. Continuous Integration

Unit tests should execute:

- On every commit
- On every pull request
- Before merges
- Before releases

A failed unit test must prevent the build from progressing.

---

# 20. Best Practices

- Keep tests simple.
- Mock external dependencies.
- Test behavior instead of implementation.
- Use meaningful assertions.
- Keep execution under a few seconds.
- Review tests during code reviews.
- Refactor tests as production code evolves.

---

# 21. Related Documents

- README – Testing Documentation
- TEST-001 – Testing Strategy
- TEST-003 – Integration Testing
- TEST-004 – API Testing
- Developer Documentation
- CI/CD Documentation

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | TEST-002 |
| Title | Unit Testing |
| Category | Testing Documentation |
| Audience | Developers, QA Engineers |
| Version | 1.0 |
| Status | Active |