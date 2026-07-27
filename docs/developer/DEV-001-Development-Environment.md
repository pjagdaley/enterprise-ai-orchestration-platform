# DEV-001 – Development Environment Setup

## 1. Purpose

This document describes how to set up a complete local development environment for the Enterprise AI Orchestration Platform.

Following this guide ensures that all developers work with a consistent and reproducible development environment.

---

## 2. Prerequisites

The following software must be installed before beginning development.

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.12+ | Backend development |
| Git | Latest | Source control |
| Docker Desktop | Latest | Containerized services |
| Visual Studio Code | Latest | Recommended IDE |
| Google Cloud SDK | Latest | GCP access |
| Java | 17+ | PlantUML documentation |
| Graphviz | Latest | Diagram generation |

---

## 3. Required Accounts

Developers should have access to:

- GitHub repository
- Google Cloud Project
- Google Cloud Storage Bucket
- Vertex AI
- Firestore
- Qdrant Server
- OpenSearch Server

---

## 4. Clone the Repository

```bash
git clone https://github.com/<organization>/enterprise-ai-orchestration-platform.git

cd enterprise-ai-orchestration-platform
```

---

## 5. Create a Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 6. Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

Verify installation:

```bash
pip list
```

---

## 7. Configure Environment Variables

Create a local environment file.

```text
.env
```

Example configuration:

```text
APP_NAME=Enterprise AI Orchestration Platform

ENVIRONMENT=development

PROJECT_ID=vertex-ai-enterprise-rag

LOCATION=us-central1

GEMINI_MODEL=gemini-2.5-flash

EMBEDDING_MODEL=text-embedding-005

QDRANT_HOST=localhost

QDRANT_PORT=6333

QDRANT_COLLECTION=enterprise_documents

OPENSEARCH_HOST=localhost

OPENSEARCH_PORT=9200

GCS_BUCKET=enterprise-ai-orchestration-documents
```

Never commit the `.env` file to source control.

---

## 8. Configure Google Cloud Credentials

Download the required Service Account credentials.

Store them under:

```text
config/
    firebase-reader.json
    storage-service.json
```

Alternatively, configure Application Default Credentials.

```bash
gcloud auth application-default login
```

Verify:

```bash
gcloud auth list
```

---

## 9. Start Supporting Services

Start local infrastructure.

Example:

```bash
docker compose up -d
```

Typical services include:

- Qdrant
- OpenSearch

Verify running containers:

```bash
docker ps
```

---

## 10. Verify Project Structure

The repository should resemble:

```text
app/

config/

docs/

scripts/

tests/

requirements.txt

docker-compose.yml

README.md
```

---

## 11. Run the Application

Start the API server.

```bash
uvicorn app.main:app --reload
```

Expected output:

```text
Application startup complete.

Uvicorn running on:

http://localhost:8000
```

---

## 12. Verify Installation

Open:

```text
http://localhost:8000/docs
```

Swagger UI should load successfully.

Verify:

- Health endpoint
- API documentation
- OpenAPI specification

---

## 13. Running Tests

Execute all tests.

```bash
pytest
```

Execute a single test.

```bash
pytest tests/test_search.py
```

Generate coverage.

```bash
pytest --cov=app
```

---

## 14. Development Tools

Recommended VS Code extensions:

- Python
- Pylance
- Docker
- GitLens
- YAML
- Markdown All in One
- PlantUML
- REST Client

---

## 15. Common Issues

### Python Version

```text
Module not found
```

Verify:

```bash
python --version
```

---

### Virtual Environment

Ensure the virtual environment is activated before installing packages.

---

### Missing Credentials

Symptoms:

```text
Permission denied

Authentication failed
```

Verify:

- Service Account
- Google Cloud login
- IAM permissions

---

### Docker Services

Verify infrastructure:

```bash
docker ps
```

Restart services if required:

```bash
docker compose restart
```

---

### Port Already in Use

Find the process using the port.

Windows:

```bash
netstat -ano
```

Linux:

```bash
lsof -i :8000
```

---

## 16. Best Practices

Developers should:

- Always use a virtual environment.
- Keep dependencies updated.
- Never commit credentials.
- Use environment variables.
- Pull the latest changes before starting work.
- Run tests before committing code.

---

## 17. Verification Checklist

Before beginning development, verify:

- Python installed
- Virtual environment active
- Dependencies installed
- Google Cloud authenticated
- Docker services running
- Environment variables configured
- API starts successfully
- Swagger UI accessible
- Tests pass

---

## 18. Related Documents

- DEV-002 – Project Structure
- DEV-006 – Testing Strategy
- DEV-008 – Build and Deployment
- SERVICE-007 – Configuration Service
- SERVICE-009 – Authentication Service

---

## Metadata

| Property | Value |
|----------|-------|
| Document ID | DEV-001 |
| Title | Development Environment Setup |
| Category | Developer Documentation |
| Audience | Software Developers |
| Version | 1.0 |
| Status | Active |