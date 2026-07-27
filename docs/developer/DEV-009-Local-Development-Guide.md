# DEV-009 – Local Development Guide

## 1. Purpose

This document describes the recommended workflow for local development of the Enterprise AI Orchestration Platform.

It provides guidance for setting up a productive development environment, running the application, testing new features, debugging issues, and validating changes before submitting them for review.

This guide should be used by all developers contributing to the platform.

---

# 2. Daily Development Workflow

The recommended workflow is:

```text
Pull Latest Code
        │
        ▼
Activate Virtual Environment
        │
        ▼
Start Infrastructure
        │
        ▼
Run Application
        │
        ▼
Develop Feature
        │
        ▼
Run Tests
        │
        ▼
Commit Changes
        │
        ▼
Create Pull Request
```

---

# 3. Update Local Repository

Fetch the latest changes.

```bash
git checkout main

git pull origin main
```

Switch to your feature branch.

```bash
git checkout feature/my-feature
```

---

# 4. Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Verify:

```bash
python --version
```

---

# 5. Start Infrastructure

Start required services.

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Typical services:

- Qdrant
- OpenSearch

---

# 6. Verify Environment

Ensure the following are configured:

- `.env`
- Google Cloud credentials
- Firestore access
- GCS bucket access
- Vertex AI access

---

# 7. Start the Application

```bash
uvicorn app.main:app --reload
```

Expected output:

```text
Application startup complete

Running on:

http://localhost:8000
```

---

# 8. Verify the API

Open:

```text
http://localhost:8000/docs
```

Verify:

- Health endpoint
- Chat endpoint
- Upload endpoint
- Search endpoint

---

# 9. Developing a Feature

Typical workflow:

```text
Create Branch
      │
      ▼
Implement Feature
      │
      ▼
Run Unit Tests
      │
      ▼
Verify APIs
      │
      ▼
Commit Changes
```

Keep commits focused on a single logical change.

---

# 10. Working with Sample Data

Place development documents under:

```text
sample-data/
```

Examples:

```text
sample-data/

policies/

architecture/

technical/

contracts/
```

Use representative documents for testing ingestion and retrieval.

---

# 11. Running Tests

Execute all tests.

```bash
pytest
```

Execute one test.

```bash
pytest tests/test_search.py
```

Coverage:

```bash
pytest --cov=app
```

---

# 12. Debugging

Use:

- VS Code debugger
- Breakpoints
- Structured logging
- Swagger UI
- Docker logs

Useful command:

```bash
docker logs <container_name>
```

---

# 13. Working with AI Components

When modifying AI functionality verify:

- Prompt construction
- Embedding generation
- Hybrid retrieval
- Reranking
- Context generation
- Gemini responses

Each stage should be validated independently.

---

# 14. Running Ingestion

Example:

```bash
python scripts/test_ingestion.py
```

Verify:

- Documents uploaded
- Chunks created
- Embeddings generated
- Qdrant indexed
- OpenSearch indexed
- Firestore updated

---

# 15. Running Search Tests

Example:

```bash
python scripts/test_search.py
```

Verify:

- Semantic search
- Keyword search
- Hybrid retrieval
- Reranker output

---

# 16. API Validation

Recommended tools:

- Swagger UI
- REST Client
- Postman

Verify:

- Status codes
- Request validation
- Error handling
- Response format

---

# 17. Before Committing

Checklist:

- Code compiles.
- Tests pass.
- Logging reviewed.
- No debug statements.
- Documentation updated.
- No credentials committed.
- Formatting completed.

---

# 18. Git Workflow

Recommended branch naming:

```text
feature/add-agent

feature/hybrid-search

bugfix/chat-history

hotfix/security-patch
```

Commit example:

```text
feat(search): implement hybrid retrieval

fix(chat): correct session history ordering

docs(services): update Firestore documentation
```

---

# 19. Local Development Checklist

Verify:

- Virtual environment active
- Docker running
- API starts successfully
- Swagger available
- Infrastructure reachable
- Tests passing
- Logs clean
- Documentation updated

---

# 20. Best Practices

Developers should:

- Pull latest changes daily.
- Commit small, focused changes.
- Test before committing.
- Keep documentation current.
- Use feature branches.
- Avoid committing generated files unless required.
- Review logs after major changes.

---

# 21. Related Documents

- DEV-001 – Development Environment Setup
- DEV-006 – Testing Strategy
- DEV-007 – Debugging Guide
- DEV-008 – Build and Deployment

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | DEV-009 |
| Title | Local Development Guide |
| Category | Developer Documentation |
| Audience | Software Developers |
| Version | 1.0 |
| Status | Active |