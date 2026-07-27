# DEV-007 – Debugging Guide

## 1. Purpose

This document provides guidelines, techniques, and best practices for debugging the Enterprise AI Orchestration Platform.

The objective is to help developers quickly identify, diagnose, and resolve issues across application logic, AI workflows, infrastructure services, and cloud integrations.

This guide covers debugging during local development, automated testing, and production support.

---

## 2. Debugging Principles

Developers should:

- Reproduce the issue consistently.
- Identify the failing component.
- Gather sufficient diagnostic information.
- Isolate the root cause.
- Apply the smallest possible fix.
- Verify the fix with tests.
- Prevent regressions.

Never make changes without understanding the underlying cause.

---

## 3. Debugging Workflow

```text
Issue Report
      │
      ▼
Reproduce Issue
      │
      ▼
Review Logs
      │
      ▼
Identify Component
      │
      ▼
Debug Root Cause
      │
      ▼
Implement Fix
      │
      ▼
Run Tests
      │
      ▼
Deploy
```

---

## 4. Debugging Tools

Recommended tools:

| Tool | Purpose |
|------|---------|
| Visual Studio Code Debugger | Interactive debugging |
| Python Debugger (pdb) | Command-line debugging |
| FastAPI Swagger UI | API testing |
| Postman | API validation |
| Docker Logs | Container diagnostics |
| Google Cloud Console | Cloud monitoring |
| Qdrant Dashboard | Vector inspection |
| OpenSearch Dashboard | Keyword search debugging |

---

## 5. Using the VS Code Debugger

Typical workflow:

1. Set breakpoints.
2. Start the debugger.
3. Trigger the API.
4. Inspect variables.
5. Step through execution.
6. Verify expected behavior.

Use breakpoints rather than excessive logging during development.

---

## 6. Logging for Debugging

Use application logs to investigate issues.

Review:

- Request ID
- API endpoint
- Execution time
- Service interactions
- Exceptions
- Warning messages

Example:

```text
INFO  Request received
INFO  Embedding generated
INFO  Qdrant search completed
INFO  OpenSearch search completed
INFO  Reranker completed
INFO  Gemini response generated
```

Logs should provide enough context to trace the execution path.

---

## 7. API Debugging

Verify:

- Request payload
- Headers
- Authentication
- HTTP status code
- Response body
- Validation errors

Swagger UI is recommended for endpoint verification during development.

---

## 8. AI Workflow Debugging

When debugging AI workflows, verify each stage independently.

```text
User Query
     │
     ▼
Prompt Construction
     │
     ▼
Embedding Generation
     │
     ▼
Vector Search
     │
     ▼
Keyword Search
     │
     ▼
Result Merging
     │
     ▼
Reranking
     │
     ▼
Context Assembly
     │
     ▼
Gemini Response
```

Do not assume the LLM is the source of every issue.

---

## 9. RAG Debugging Checklist

Verify:

- Document uploaded successfully.
- Parser extracted text correctly.
- Chunk count is reasonable.
- Embeddings generated successfully.
- Qdrant contains vectors.
- OpenSearch contains indexed text.
- Hybrid search returns relevant documents.
- Reranker produces expected ordering.
- Prompt contains expected context.
- Gemini returns grounded answers.

---

## 10. Infrastructure Debugging

### Firestore

Verify:

- Credentials
- Collection names
- Document IDs
- Read/write permissions
- Database availability

---

### Google Cloud Storage

Verify:

- Bucket exists
- Object path
- IAM permissions
- Upload status

---

### Qdrant

Verify:

- Collection exists
- Vector count
- Embedding dimension
- Metadata filters
- Search results

---

### OpenSearch

Verify:

- Index exists
- Documents indexed
- BM25 queries
- Cluster health

---

### Vertex AI

Verify:

- Project ID
- Region
- Authentication
- Quotas
- Model availability

---

## 11. Common Issues

### Empty Search Results

Possible causes:

- Missing embeddings
- Incorrect collection
- Metadata filter mismatch
- Empty index
- Incorrect folder priority

---

### Poor AI Responses

Verify:

- Prompt quality
- Retrieved context
- Search relevance
- Chunk size
- Reranker output

---

### Slow Response Time

Investigate:

- Embedding latency
- Search latency
- Network delays
- Large prompts
- Reranker performance

---

### Authentication Errors

Verify:

- Service Account
- IAM permissions
- Environment variables
- Credential files

---

## 12. Docker Debugging

View logs:

```bash
docker logs <container_name>
```

List containers:

```bash
docker ps
```

Restart a service:

```bash
docker compose restart
```

Inspect container:

```bash
docker exec -it <container_name> bash
```

---

## 13. Performance Debugging

Monitor:

- API latency
- Memory usage
- CPU usage
- Database latency
- Search latency
- AI inference time

Use logs and metrics to identify bottlenecks.

---

## 14. Production Debugging

In production:

- Never modify data directly.
- Preserve audit logs.
- Capture request IDs.
- Review monitoring dashboards.
- Reproduce issues in lower environments when possible.

Avoid debugging directly in production unless necessary.

---

## 15. Best Practices

Developers should:

- Reproduce issues before fixing them.
- Use structured logging.
- Keep debugging sessions focused.
- Validate assumptions with data.
- Add regression tests after fixing defects.
- Document recurring issues.

---

## 16. Related Documents

- DEV-005 – Error Handling
- DEV-006 – Testing Strategy
- SERVICE-008 – Logging Service
- Architecture Documentation
- Operations Runbooks

---

## Metadata

| Property | Value |
|----------|-------|
| Document ID | DEV-007 |
| Title | Debugging Guide |
| Category | Developer Documentation |
| Audience | Developers, DevOps Engineers, Support Engineers |
| Version | 1.0 |
| Status | Active |