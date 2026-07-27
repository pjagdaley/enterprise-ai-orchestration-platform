# API-010 – Error Codes and Response Models

## 1. Purpose

This document defines the standard request and response models used throughout the Enterprise AI Orchestration Platform.

The objectives are to:

- Standardize API responses
- Simplify client integrations
- Provide consistent error handling
- Support observability through correlation IDs
- Standardize pagination
- Define streaming response formats
- Establish enterprise-wide error codes

All REST APIs in the platform shall conform to these standards.

---

# 2. Scope

This document covers:

- Success responses
- Error responses
- Validation errors
- Pagination
- Streaming responses
- Correlation IDs
- Error codes
- Retry guidance

---

# 3. Standard Response Model

Every successful API should return the following structure.

```json
{
  "success": true,
  "data": {},
  "metadata": {
    "correlationId": "5c13b761-9af8-4388-8611-f498efca58b5",
    "timestamp": "2026-09-05T10:15:42Z"
  }
}
```

---

# 4. Success Response Model

```json
{
  "success": true,
  "data": {
    "...": "..."
  },
  "metadata": {
    "correlationId": "5c13b761-9af8-4388-8611-f498efca58b5",
    "timestamp": "2026-09-05T10:15:42Z"
  }
}
```

---

# 5. Error Response Model

```json
{
  "success": false,
  "error": {
    "code": "DOCUMENT_NOT_FOUND",
    "message": "Requested document does not exist.",
    "details": []
  },
  "metadata": {
    "correlationId": "5c13b761-9af8-4388-8611-f498efca58b5",
    "timestamp": "2026-09-05T10:15:42Z"
  }
}
```

---

# 6. Validation Error Model

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more validation errors occurred.",
    "details": [
      {
        "field": "query",
        "message": "Query must not be empty."
      },
      {
        "field": "topK",
        "message": "Value must be greater than zero."
      }
    ]
  },
  "metadata": {
    "correlationId": "5c13b761-9af8-4388-8611-f498efca58b5"
  }
}
```

---

# 7. Pagination Response

```json
{
  "success": true,
  "data": [
    {}
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "totalItems": 156,
    "totalPages": 8,
    "hasNext": true,
    "hasPrevious": false
  },
  "metadata": {
    "correlationId": "5c13b761-9af8-4388-8611-f498efca58b5"
  }
}
```

---

# 8. Streaming Response

Streaming APIs should use Server-Sent Events (SSE).

Example:

```text
event: message
data: Searching enterprise knowledge...

event: message
data: Running hybrid retrieval...

event: message
data: Generating AI response...

event: complete
data: Done
```

---

# 9. Correlation IDs

Every request should include or generate a unique correlation ID.

Request header:

```http
X-Correlation-ID: 5c13b761-9af8-4388-8611-f498efca58b5
```

If not provided, the platform should generate one automatically.

Correlation IDs enable:

- Request tracing
- Distributed logging
- Incident investigation
- Performance analysis

---

# 10. HTTP Status Codes

| HTTP Code | Description |
|-----------|-------------|
| 200 | Success |
| 201 | Resource created |
| 202 | Accepted for processing |
| 204 | No content |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |
| 413 | Payload too large |
| 415 | Unsupported media type |
| 422 | Validation failed |
| 429 | Too many requests |
| 500 | Internal server error |
| 502 | Bad gateway |
| 503 | Service unavailable |
| 504 | Gateway timeout |

---

# 11. Error Code Categories

| Prefix | Category |
|----------|----------|
| AUTH | Authentication |
| USER | User |
| DOC | Documents |
| SEARCH | Search |
| AGENT | Agents |
| WORKFLOW | Workflows |
| TOOL | Tools |
| AI | AI Services |
| CONFIG | Configuration |
| SYSTEM | Platform |

---

# 12. Authentication Errors

| Error Code | Description |
|-------------|-------------|
| AUTH_001 | Invalid credentials |
| AUTH_002 | JWT token expired |
| AUTH_003 | JWT token invalid |
| AUTH_004 | Authentication required |
| AUTH_005 | Insufficient permissions |

---

# 13. Document Errors

| Error Code | Description |
|-------------|-------------|
| DOC_001 | Document not found |
| DOC_002 | Unsupported file type |
| DOC_003 | File too large |
| DOC_004 | Duplicate document |
| DOC_005 | Document processing failed |
| DOC_006 | Document indexing failed |
| DOC_007 | Metadata unavailable |

---

# 14. Search Errors

| Error Code | Description |
|-------------|-------------|
| SEARCH_001 | Invalid search request |
| SEARCH_002 | Search timeout |
| SEARCH_003 | No search results |
| SEARCH_004 | Search service unavailable |
| SEARCH_005 | Reranking failed |
| SEARCH_006 | Invalid search filter |

---

# 15. Agent Errors

| Error Code | Description |
|-------------|-------------|
| AGENT_001 | Agent unavailable |
| AGENT_002 | Agent execution failed |
| AGENT_003 | Agent timeout |
| AGENT_004 | Agent not found |
| AGENT_005 | Agent configuration error |

---

# 16. Workflow Errors

| Error Code | Description |
|-------------|-------------|
| WORKFLOW_001 | Workflow not found |
| WORKFLOW_002 | Workflow execution failed |
| WORKFLOW_003 | Workflow cancelled |
| WORKFLOW_004 | Workflow timeout |
| WORKFLOW_005 | Workflow waiting for approval |

---

# 17. Tool Errors

| Error Code | Description |
|-------------|-------------|
| TOOL_001 | Tool not found |
| TOOL_002 | Tool execution failed |
| TOOL_003 | Tool unavailable |
| TOOL_004 | Invalid tool input |
| TOOL_005 | Tool timeout |

---

# 18. AI Service Errors

| Error Code | Description |
|-------------|-------------|
| AI_001 | Model unavailable |
| AI_002 | Prompt rejected |
| AI_003 | Token limit exceeded |
| AI_004 | Embedding generation failed |
| AI_005 | Rate limit exceeded |
| AI_006 | Context window exceeded |

---

# 19. Platform Errors

| Error Code | Description |
|-------------|-------------|
| SYSTEM_001 | Internal server error |
| SYSTEM_002 | Configuration error |
| SYSTEM_003 | Dependency unavailable |
| SYSTEM_004 | Database unavailable |
| SYSTEM_005 | Storage unavailable |
| SYSTEM_006 | Service startup failure |

---

# 20. Retry Guidance

| Error | Retry? | Recommendation |
|--------|--------|----------------|
| 400 | No | Correct the request |
| 401 | No | Re-authenticate |
| 403 | No | Request additional permissions |
| 404 | No | Verify resource identifier |
| 409 | Depends | Retry after resolving conflict |
| 422 | No | Correct validation errors |
| 429 | Yes | Retry with exponential backoff |
| 500 | Yes | Retry after a short delay |
| 503 | Yes | Retry using exponential backoff |
| 504 | Yes | Retry the request |

---

# 21. API Design Conventions

The platform should follow these conventions:

- Use REST resource-oriented URIs.
- Use plural resource names.
- Use JSON for request and response bodies.
- Return consistent response structures.
- Include correlation IDs in every response.
- Use UTC timestamps in ISO 8601 format.
- Support pagination for collection resources.
- Version APIs using the URI (for example, `/api/v1/...`).

---

# 22. Best Practices

- Use descriptive error messages.
- Avoid exposing internal implementation details.
- Include correlation IDs in support requests.
- Return appropriate HTTP status codes.
- Keep response payloads consistent.
- Document all public error codes.
- Log all server-side exceptions with the correlation ID.

---

# 23. Related Documents

- API-001 – Authentication APIs
- API-002 – Chat APIs
- API-003 – Document Management APIs
- API-004 – Search APIs
- API-005 – Agent APIs
- API-006 – Workflow APIs
- API-007 – Tool Registry APIs
- API-008 – Health and Monitoring APIs
- API-009 – Administration APIs

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | API-010 |
| Title | Error Codes and Response Models |
| Category | API Documentation |
| Audience | Backend Developers, Frontend Developers, Integration Engineers |
| Version | 1.0 |
| Status | Active |