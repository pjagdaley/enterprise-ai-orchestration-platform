# API-004 – Search APIs

## 1. Purpose

This document describes the Search APIs exposed by the Enterprise AI Orchestration Platform.

The Search APIs provide enterprise-grade retrieval capabilities for Retrieval-Augmented Generation (RAG), enabling client applications to locate relevant information across the enterprise knowledge base using semantic search, keyword search, or hybrid retrieval.

The APIs support:

- Semantic vector search
- Keyword (BM25) search
- Hybrid search
- Metadata filtering
- Cross-encoder reranking
- Citation generation
- Search result pagination

---

# 2. Scope

The Search APIs support:

- Enterprise document retrieval
- AI-assisted search
- Hybrid retrieval
- Search filtering
- Search suggestions
- Search analytics
- Relevance scoring

---

# 3. Search Architecture

```text
                 Client Application
                         │
                         ▼
              POST /api/v1/search
                         │
                         ▼
                 Search Controller
                         │
                         ▼
                  Search Service
                         │
         ┌───────────────┼────────────────┐
         ▼               ▼                ▼
    Query Analyzer   Metadata Filter   Query Builder
         │
         ▼
     Hybrid Retriever
         │
   ┌─────┴───────────┐
   ▼                 ▼
Qdrant          OpenSearch
   │                 │
   └──────┬──────────┘
          ▼
   Result Aggregator
          │
          ▼
 Cross-Encoder Reranker
          │
          ▼
 Citation Generator
          │
          ▼
     Search Response
```

---

# 4. Search Workflow

```text
Receive Query
      │
      ▼
Validate Request
      │
      ▼
Generate Embedding
      │
      ▼
Semantic Search (Qdrant)
      │
      ├──────────────┐
      ▼              ▼
Keyword Search   Metadata Filter
(OpenSearch)
      │
      ▼
Merge Results
      │
      ▼
Cross-Encoder Reranking
      │
      ▼
Generate Citations
      │
      ▼
Return Results
```

---

# 5. API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/search | Hybrid search |
| POST | /api/v1/search/semantic | Semantic search |
| POST | /api/v1/search/keyword | BM25 keyword search |
| POST | /api/v1/search/suggestions | Search suggestions |
| GET | /api/v1/search/filters | Available metadata filters |

---

# 6. Hybrid Search

## Endpoint

```http
POST /api/v1/search
```

### Description

Executes hybrid retrieval using semantic vector search and keyword search, followed by reranking.

---

### Request

```json
{
  "query": "Explain enterprise architecture governance.",
  "topK": 10,
  "filters": {
    "department": "Architecture",
    "documentType": "PDF"
  }
}
```

---

### Request Fields

| Field | Type | Required | Description |
|------|------|:--------:|-------------|
| query | String | Yes | Search query |
| topK | Integer | No | Maximum results |
| filters | Object | No | Metadata filters |

---

### Successful Response

```json
{
  "success": true,
  "results": [
    {
      "documentId": "DOC-101",
      "title": "Enterprise Architecture Guide",
      "score": 0.982,
      "snippet": "Architecture governance ensures...",
      "citation": {
        "page": 12,
        "section": "Governance"
      }
    }
  ]
}
```

---

# 7. Semantic Search

## Endpoint

```http
POST /api/v1/search/semantic
```

### Description

Performs vector similarity search using Qdrant.

---

### Request

```json
{
  "query": "What is LangGraph?"
}
```

### Response

```json
{
  "results": [
    {
      "documentId": "DOC-220",
      "score": 0.97
    }
  ]
}
```

Semantic search retrieves conceptually similar content even when exact keywords are absent.

---

# 8. Keyword Search

## Endpoint

```http
POST /api/v1/search/keyword
```

### Description

Executes BM25 keyword search using OpenSearch.

---

### Request

```json
{
  "query": "TOGAF governance framework"
}
```

### Response

```json
{
  "results": [
    {
      "documentId": "DOC-410",
      "score": 18.3
    }
  ]
}
```

Keyword search is particularly effective for structured data, exact terms, identifiers, and acronyms.

---

# 9. Search Suggestions

## Endpoint

```http
POST /api/v1/search/suggestions
```

### Description

Returns suggested search queries based on partial user input.

---

### Request

```json
{
  "text": "Enterpri"
}
```

### Response

```json
{
  "suggestions": [
    "Enterprise Architecture",
    "Enterprise AI",
    "Enterprise Governance"
  ]
}
```

---

# 10. Metadata Filters

## Endpoint

```http
GET /api/v1/search/filters
```

### Description

Returns available metadata filters.

---

### Response

```json
{
  "documentTypes": [
    "PDF",
    "DOCX",
    "JSON",
    "XLSX"
  ],
  "departments": [
    "Architecture",
    "Finance",
    "HR"
  ]
}
```

---

# 11. Supported Filters

Supported metadata filters include:

| Filter | Description |
|---------|-------------|
| Folder | Source folder |
| Department | Business unit |
| Document Type | File format |
| Author | Document owner |
| Tags | Classification |
| Created Date | Upload date |
| Updated Date | Last modification |
| Language | Document language |

Multiple filters may be combined within a single request.

---

# 12. Search Processing Pipeline

```text
Receive Request
      │
      ▼
Validate Query
      │
      ▼
Generate Embedding
      │
      ▼
Qdrant Search
      │
      ▼
OpenSearch Search
      │
      ▼
Merge Results
      │
      ▼
Metadata Filtering
      │
      ▼
Cross-Encoder Reranking
      │
      ▼
Generate Citations
      │
      ▼
Return Results
```

---

# 13. Authentication

All Search APIs require a valid JWT access token.

```http
Authorization: Bearer <access_token>
```

---

# 14. HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Invalid request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | No matching results |
| 422 | Validation error |
| 429 | Rate limited |
| 500 | Internal server error |
| 503 | Search service unavailable |

---

# 15. Error Response

```json
{
  "success": false,
  "error": {
    "code": "SEARCH_SERVICE_UNAVAILABLE",
    "message": "Search service is temporarily unavailable."
  }
}
```

---

# 16. Security Considerations

The Search APIs should:

- Require authentication.
- Apply authorization filters before retrieval.
- Restrict access to protected documents.
- Prevent query injection attacks.
- Validate metadata filters.
- Log search activity for auditing.
- Enforce rate limits.

---

# 17. Performance Considerations

Performance recommendations:

- Cache embeddings for repeated queries where appropriate.
- Execute semantic and keyword searches in parallel.
- Limit reranking to the highest-scoring candidates.
- Paginate large result sets.
- Monitor search latency and relevance metrics.
- Optimize metadata indexes.

---

# 18. Best Practices

- Prefer hybrid search for general knowledge retrieval.
- Use semantic search for conceptual questions.
- Use keyword search for identifiers, codes, and exact phrases.
- Apply metadata filters to narrow search scope.
- Tune `topK` based on the use case.
- Monitor search quality and reranker effectiveness.

---

# 19. Related Documents

- API-002 – Chat APIs
- API-003 – Document Management APIs
- SERVICE-002 – Vertex AI Embedding Service
- SERVICE-003 – Qdrant Service
- SERVICE-005 – OpenSearch Service
- WF-005 – Hybrid Search Workflow
- AG-003 – Knowledge Retrieval Agent

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | API-004 |
| Title | Search APIs |
| Category | API Documentation |
| Audience | Backend Developers, AI Engineers, Integration Engineers |
| Version | 1.0 |
| Status | Active |