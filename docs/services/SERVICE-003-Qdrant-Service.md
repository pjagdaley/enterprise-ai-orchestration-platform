# SERVICE-003 – Qdrant Service

## 1. Purpose

The Qdrant Service provides centralized vector database operations for the Enterprise AI Orchestration Platform.

It is responsible for storing, indexing, retrieving, updating, and deleting vector embeddings generated from enterprise documents. The service enables high-performance semantic search by comparing vector similarity between user queries and indexed document chunks.

The Qdrant Service abstracts all interactions with the Qdrant Vector Database and provides a consistent interface to the platform.

---

## 2. Responsibilities

The Qdrant Service is responsible for:

- Creating collections.
- Managing vector indexes.
- Storing document embeddings.
- Batch upsert operations.
- Semantic similarity search.
- Metadata filtering.
- Document deletion.
- Collection management.
- Health monitoring.
- Search optimization.

The Qdrant Service does not generate embeddings or rerank search results.

---

## 3. Position within the Architecture

```text
                 Enterprise RAG Tool
                         │
                         ▼
                  Qdrant Service
                         │
                         ▼
                  Qdrant Database
                         │
           ┌─────────────┴─────────────┐
           ▼                           ▼
     Vector Storage             Vector Search
```

---

## 4. Business Responsibilities

The Qdrant Service enables:

- Enterprise knowledge search.
- Semantic document retrieval.
- Vector indexing.
- Similarity search.
- Metadata filtering.
- Hybrid retrieval support.
- Enterprise knowledge management.

Typical operations include:

- Store document vectors.
- Retrieve similar documents.
- Delete document embeddings.
- Filter documents by metadata.
- Search within document categories.

---

## 5. Public Interface

| Operation | Description |
|-----------|-------------|
| create_collection() | Create vector collection |
| collection_exists() | Verify collection |
| upsert_vectors() | Store vectors |
| search() | Semantic similarity search |
| scroll() | Retrieve vectors |
| delete() | Delete vectors |
| delete_by_document() | Delete all chunks for a document |
| health() | Service health |

---

## 6. Configuration

| Property | Description |
|----------|-------------|
| Host | Qdrant server |
| Port | API port |
| Collection | Collection name |
| Vector Dimension | Embedding dimension |
| Distance Metric | Similarity algorithm |
| Batch Size | Upsert batch size |

Example:

```text
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=enterprise_documents
VECTOR_DIMENSION=768
DISTANCE=COSINE
QDRANT_BATCH_SIZE=200
```

---

## 7. Collection Schema

| Property | Value |
|----------|------|
| Vector Size | 768 |
| Distance Metric | Cosine Similarity |
| Storage | Persistent |
| Payload | JSON Metadata |

---

## 8. Payload Schema

Each vector stores associated metadata.

Example:

```json
{
    "document_id": "uuid",
    "chunk_id": "uuid",
    "chunk_number": 12,
    "filename": "Architecture.pdf",
    "extension": ".pdf",
    "folder": "Architecture",
    "source_path": "Architecture/Architecture.pdf",
    "page": 18,
    "text": "...",
    "created_at": "2026-07-26T12:00:00Z"
}
```

---

## 9. Processing Flow

### Document Indexing

```text
Embedding Tool
      │
      ▼
Receive Vectors
      │
      ▼
Validate Payload
      │
      ▼
Batch Upsert
      │
      ▼
Qdrant Collection
```

### Semantic Search

```text
Receive Query Vector
       │
       ▼
Apply Metadata Filter
       │
       ▼
Vector Similarity Search
       │
       ▼
Return Top-K Results
```

---

## 10. Interaction with Other Components

| Component | Interaction |
|-----------|-------------|
| Embedding Tool | Supplies vectors |
| Enterprise RAG Tool | Executes search |
| Reranker Tool | Reranks retrieved chunks |
| Firestore Service | Retrieves metadata |
| OpenSearch Service | Supports hybrid retrieval |

---

## 11. Metadata Filtering

Supported filters include:

- Folder
- Document ID
- File Extension
- Source Path
- Document Type
- Tags
- Custom Metadata

Example:

```text
folder = "Policies"

extension = ".pdf"

document_type = "Architecture"
```

---

## 12. Search Strategy

The service supports:

### Semantic Search

Vector similarity using cosine distance.

### Metadata Search

Restrict search using payload filters.

### Priority Folder Search

The platform supports sequential folder-based search.

Example:

```text
Folder 1
    ↓
No Results

Folder 2
    ↓
No Results

Folder 3
    ↓
Relevant Results

Stop Search
```

This minimizes unnecessary searches while supporting prioritized enterprise knowledge retrieval.

---

## 13. Error Handling

| Failure | Behaviour |
|----------|-----------|
| Collection missing | Create automatically |
| Connection failure | Retry |
| Invalid vector size | Reject request |
| Search timeout | Return retryable error |
| Payload validation failure | Reject document |

---

## 14. Security Considerations

The Qdrant Service:

- Validates payload metadata.
- Supports tenant isolation (future).
- Restricts collection access.
- Logs search operations.
- Prevents invalid payload insertion.

---

## 15. Performance Considerations

- Batch upserts.
- Connection reuse.
- Optimized Top-K retrieval.
- Metadata indexing.
- Efficient payload storage.
- Configurable batch size.
- Parallel ingestion.

---

## 16. Technology Stack

| Technology | Purpose |
|------------|---------|
| Qdrant | Vector Database |
| qdrant-client | Python client |
| FastAPI | Application framework |
| Python | Service implementation |

---

## 17. Monitoring & Observability

The Qdrant Service records:

- Collection size
- Stored vectors
- Search latency
- Upsert latency
- Failed requests
- Search throughput
- Connection status

Logs include:

- Collection name
- Request ID
- Search duration
- Top-K requested
- Error details

---

## 18. Future Enhancements

Future improvements may include:

- Distributed Qdrant clusters.
- Automatic sharding.
- Payload indexing optimization.
- Quantization.
- Snapshot management.
- Cross-region replication.
- Multi-tenant collections.

---

## 19. Sequence Diagram

```text
Enterprise RAG Tool
        │
        ▼
Qdrant Service
        │
        ▼
Qdrant Database
        │
        ▼
Vector Search
        │
        ▼
Top-K Documents
        │
        ▼
Enterprise RAG Tool
```

---

## 20. Design Principles

The Qdrant Service follows these principles:

- Stateless execution.
- High-performance retrieval.
- Metadata-driven filtering.
- Provider abstraction.
- Scalable indexing.
- Configuration-driven behavior.

---

## 21. Success Criteria

The Qdrant Service is considered successful when:

- Collections are initialized automatically.
- Document vectors are indexed successfully.
- Semantic searches return relevant results.
- Metadata filters are applied correctly.
- Batch operations complete successfully.
- Performance objectives are achieved.

---

## Metadata

| Property | Value |
|----------|-------|
| Service ID | SERVICE-003 |
| Service Name | Qdrant Service |
| Type | Infrastructure Service |
| Category | Vector Database |
| Provider | Qdrant |
| Owner | Enterprise AI Orchestration Platform |
| Version | 1.0 |
| Status | Implemented |