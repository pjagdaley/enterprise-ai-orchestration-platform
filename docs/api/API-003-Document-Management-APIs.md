# API-003 – Document Management APIs

## 1. Purpose

This document describes the Document Management APIs for the Enterprise AI Orchestration Platform.

The Document Management APIs enable client applications to:

- Upload knowledge documents
- Retrieve document metadata
- Monitor ingestion status
- List indexed documents
- Reprocess documents
- Delete documents
- Manage the enterprise knowledge base

These APIs provide the entry point for the Retrieval-Augmented Generation (RAG) ingestion pipeline.

---

# 2. Scope

The Document Management APIs support:

- Single document upload
- Batch document upload
- Document listing
- Document metadata retrieval
- Document deletion
- Document re-indexing
- Ingestion status monitoring

---

# 3. Document Processing Architecture

```text
               Client Application
                       │
                       ▼
          POST /api/v1/documents
                       │
                       ▼
            Document Controller
                       │
                       ▼
            Document Service
                       │
        ┌──────────────┼────────────────┐
        ▼              ▼                ▼
 Google Cloud     Firestore      Ingestion Queue
    Storage         Metadata             │
                                         ▼
                                  Parser Service
                                         │
                                         ▼
                                   Chunk Service
                                         │
                                         ▼
                               Embedding Service
                                         │
                              ┌──────────┴─────────┐
                              ▼                    ▼
                          Qdrant            OpenSearch
```

---

# 4. Document Lifecycle

```text
Upload
   │
   ▼
Store in GCS
   │
   ▼
Create Metadata
   │
   ▼
Parse Document
   │
   ▼
Chunk Document
   │
   ▼
Generate Embeddings
   │
   ▼
Index in Qdrant
   │
   ▼
Index in OpenSearch
   │
   ▼
Ready
```

---

# 5. Supported File Types

| Extension | Supported |
|-----------|-----------|
| PDF | Yes |
| DOCX | Yes |
| TXT | Yes |
| XLSX | Yes |
| JSON | Yes |
| CSV | Future |
| PPTX | Future |

Maximum file size should be configurable through platform settings.

---

# 6. API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/documents | Upload document |
| POST | /api/v1/documents/batch | Upload multiple documents |
| GET | /api/v1/documents | List documents |
| GET | /api/v1/documents/{documentId} | Get document metadata |
| GET | /api/v1/documents/{documentId}/status | Get ingestion status |
| POST | /api/v1/documents/{documentId}/reindex | Re-index document |
| DELETE | /api/v1/documents/{documentId} | Delete document |

---

# 7. Upload Document

## Endpoint

```http
POST /api/v1/documents
```

### Content Type

```text
multipart/form-data
```

### Request

| Field | Type | Required | Description |
|------|------|:--------:|-------------|
| file | Binary | Yes | Document |
| folder | String | No | Logical folder |
| tags | Array | No | Classification tags |

---

### Successful Response

HTTP 201

```json
{
  "documentId": "DOC-1001",
  "fileName": "architecture.pdf",
  "status": "UPLOADED",
  "uploadedAt": "2026-08-10T09:15:00Z"
}
```

---

# 8. Batch Upload

## Endpoint

```http
POST /api/v1/documents/batch
```

### Description

Uploads multiple documents within a single request.

### Response

```json
{
  "uploaded": 5,
  "failed": 0,
  "documents": [
    {
      "documentId": "DOC-1001"
    },
    {
      "documentId": "DOC-1002"
    }
  ]
}
```

Batch uploads should validate each file independently.

---

# 9. List Documents

## Endpoint

```http
GET /api/v1/documents
```

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| page | Page number |
| size | Page size |
| status | Filter by ingestion status |
| fileType | Filter by file type |
| folder | Filter by logical folder |

---

### Response

```json
{
  "page": 1,
  "size": 20,
  "total": 150,
  "documents": [
    {
      "documentId": "DOC-1001",
      "fileName": "architecture.pdf",
      "status": "READY"
    }
  ]
}
```

---

# 10. Get Document Metadata

## Endpoint

```http
GET /api/v1/documents/{documentId}
```

### Response

```json
{
  "documentId": "DOC-1001",
  "fileName": "architecture.pdf",
  "fileType": "PDF",
  "size": 1254634,
  "chunkCount": 182,
  "status": "READY",
  "uploadedBy": "user123",
  "uploadedAt": "2026-08-10T09:15:00Z"
}
```

---

# 11. Get Ingestion Status

## Endpoint

```http
GET /api/v1/documents/{documentId}/status
```

### Response

```json
{
  "status": "INDEXING",
  "progress": 72,
  "currentStage": "Embedding Generation"
}
```

---

# 12. Re-index Document

## Endpoint

```http
POST /api/v1/documents/{documentId}/reindex
```

### Description

Triggers a complete reprocessing of the document.

Stages include:

- Parsing
- Chunking
- Embedding generation
- Qdrant indexing
- OpenSearch indexing

### Response

```json
{
  "status": "REINDEX_STARTED"
}
```

---

# 13. Delete Document

## Endpoint

```http
DELETE /api/v1/documents/{documentId}
```

### Description

Deletes the document and all associated indexes.

The operation removes:

- Source document from Google Cloud Storage
- Firestore metadata
- Qdrant vectors
- OpenSearch index entries

### Response

HTTP 204

---

# 14. Processing Status

| Status | Description |
|---------|-------------|
| UPLOADED | File received |
| PARSING | Extracting content |
| CHUNKING | Splitting content |
| EMBEDDING | Generating embeddings |
| INDEXING | Updating search indexes |
| READY | Available for search |
| FAILED | Processing failed |

---

# 15. Authentication

All Document Management APIs require a valid JWT access token.

```http
Authorization: Bearer <access_token>
```

Administrative operations may require elevated privileges.

---

# 16. Error Responses

| HTTP | Description |
|------|-------------|
| 400 | Invalid request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Document not found |
| 409 | Duplicate document |
| 413 | File too large |
| 415 | Unsupported media type |
| 422 | Validation error |
| 500 | Internal server error |

Example:

```json
{
  "success": false,
  "error": {
    "code": "UNSUPPORTED_FILE_TYPE",
    "message": "The uploaded file type is not supported."
    }
}
```

---

# 17. Security Considerations

The Document Management APIs should:

- Validate file types.
- Scan uploaded files for malware.
- Enforce upload size limits.
- Restrict access using RBAC.
- Encrypt stored documents.
- Validate ownership before deletion.
- Log upload and deletion activities.

---

# 18. Performance Considerations

To improve throughput:

- Process ingestion asynchronously.
- Batch embedding requests.
- Parallelize indexing where appropriate.
- Use resumable uploads for large files.
- Monitor ingestion queue depth.
- Track average ingestion time.

---

# 19. Best Practices

- Validate files before upload.
- Store original documents unchanged.
- Keep metadata synchronized with indexes.
- Retry transient ingestion failures.
- Avoid duplicate uploads.
- Monitor ingestion metrics.
- Archive rather than permanently delete when required by retention policies.

---

# 20. Related Documents

- API-004 – Search APIs
- SERVICE-002 – Vertex AI Embedding Service
- SERVICE-003 – Qdrant Service
- SERVICE-004 – Firestore Service
- SERVICE-005 – OpenSearch Service
- SERVICE-006 – Google Cloud Storage Service
- WF-004 – Document Ingestion Workflow

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | API-003 |
| Title | Document Management APIs |
| Category | API Documentation |
| Audience | Backend Developers, Integration Engineers, Platform Engineers |
| Version | 1.0 |
| Status | Active |