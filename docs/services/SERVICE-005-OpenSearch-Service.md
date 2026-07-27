# SERVICE-005 – OpenSearch Service

## 1. Purpose

The OpenSearch Service provides enterprise-grade lexical search capabilities for the Enterprise AI Orchestration Platform.

It is responsible for indexing document text and executing keyword-based searches using the BM25 ranking algorithm. The service complements semantic vector search performed by the Qdrant Service, enabling a Hybrid Search architecture that combines semantic understanding with precise keyword matching.

The OpenSearch Service abstracts all interactions with the OpenSearch cluster and provides a unified search interface for the platform.

---

## 2. Responsibilities

The OpenSearch Service is responsible for:

- Managing OpenSearch client initialization.
- Creating and maintaining search indexes.
- Indexing document chunks.
- Executing BM25 keyword searches.
- Supporting metadata filtering.
- Deleting indexed documents.
- Managing index lifecycle.
- Monitoring search performance.

The OpenSearch Service does not generate embeddings or perform semantic similarity search.

---

## 3. Position within the Architecture

```text
                Enterprise RAG Tool
                        │
                        ▼
               OpenSearch Service
                        │
                        ▼
                OpenSearch Cluster
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
      BM25 Search              Metadata Filters
```

---

## 4. Business Responsibilities

The OpenSearch Service enables:

- Keyword search.
- Exact phrase search.
- BM25 ranking.
- Metadata filtering.
- Enterprise document discovery.
- Hybrid retrieval.

Typical use cases include:

- Finding specific policy numbers.
- Searching configuration parameters.
- Retrieving JSON fields.
- Searching spreadsheet values.
- Locating exact error messages.
- Finding code snippets.

---

## 5. Public Interface

| Operation | Description |
|-----------|-------------|
| create_index() | Create search index |
| index_document() | Index document chunk |
| index_batch() | Batch indexing |
| search() | Execute BM25 search |
| delete_document() | Remove indexed document |
| delete_index() | Delete search index |
| health() | Verify service availability |

---

## 6. Configuration

| Property | Description |
|----------|-------------|
| Host | OpenSearch server |
| Port | REST API port |
| Index | Search index |
| Analyzer | Text analyzer |
| Batch Size | Bulk indexing size |

Example:

```text
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_INDEX=enterprise_documents
BATCH_SIZE=500
```

---

## 7. Index Schema

Each indexed document contains:

| Field | Description |
|--------|-------------|
| document_id | Document identifier |
| chunk_id | Chunk identifier |
| filename | Original filename |
| extension | File extension |
| folder | Source folder |
| source_path | Document path |
| page | Page number |
| text | Chunk content |
| metadata | Custom metadata |

---

## 8. Processing Flow

### Document Indexing

```text
Receive Chunk
      │
      ▼
Validate Metadata
      │
      ▼
Build Index Document
      │
      ▼
Bulk Index
      │
      ▼
OpenSearch
```

### Keyword Search

```text
Receive Query
      │
      ▼
Build BM25 Query
      │
      ▼
Execute Search
      │
      ▼
Apply Metadata Filters
      │
      ▼
Return Ranked Results
```

---

## 9. Interaction with Other Components

| Component | Interaction |
|-----------|-------------|
| Enterprise RAG Tool | Executes keyword search |
| Qdrant Service | Hybrid retrieval |
| Reranker Tool | Reorders combined results |
| Ingestion Service | Indexes document chunks |
| Document Parser Tool | Provides parsed text |

---

## 10. Search Capabilities

Supported search features include:

- BM25 ranking
- Exact phrase search
- Boolean queries
- Wildcard search
- Prefix search
- Metadata filtering
- Pagination
- Sorting

---

## 11. Hybrid Search

The OpenSearch Service works together with the Qdrant Service.

```text
User Query
      │
      ├───────────────┐
      ▼               ▼
Qdrant Search   OpenSearch
      │               │
      └──────┬────────┘
             ▼
       Merge Results
             ▼
      Reranker Tool
             ▼
      Gemini Service
```

This architecture combines:

- Semantic similarity (Qdrant)
- Keyword relevance (OpenSearch)
- CrossEncoder reranking

---

## 12. Error Handling

| Failure | Behaviour |
|----------|-----------|
| Index missing | Create automatically |
| Connection failure | Retry |
| Invalid query | Return validation error |
| Bulk indexing failure | Retry failed items |
| Timeout | Return retryable error |

---

## 13. Security Considerations

The OpenSearch Service:

- Restricts index access.
- Validates search requests.
- Supports authenticated access.
- Logs search activity.
- Prevents malformed queries.

---

## 14. Performance Considerations

- Bulk indexing.
- Connection pooling.
- Optimized BM25 queries.
- Efficient pagination.
- Index optimization.
- Metadata indexing.

---

## 15. Technology Stack

| Technology | Purpose |
|------------|---------|
| OpenSearch | Search engine |
| opensearch-py | Python client |
| BM25 | Ranking algorithm |
| FastAPI | Application framework |
| Python | Service implementation |

---

## 16. Monitoring & Observability

The OpenSearch Service records:

- Indexed documents
- Search requests
- Search latency
- Failed indexing operations
- Failed searches
- Cluster health
- Index size

Logs include:

- Request ID
- Search duration
- Query text
- Returned results
- Error details

---

## 17. Future Enhancements

Future improvements may include:

- Synonym dictionaries.
- Language-specific analyzers.
- Fuzzy search.
- Autocomplete.
- Highlighting.
- Multi-index search.
- Index lifecycle management.

---

## 18. Sequence Diagram

```text
Enterprise RAG Tool
        │
        ▼
OpenSearch Service
        │
        ▼
OpenSearch Cluster
        │
        ▼
BM25 Results
        │
        ▼
Enterprise RAG Tool
```

---

## 19. Design Principles

The OpenSearch Service follows these principles:

- Stateless execution.
- High-performance retrieval.
- Metadata-driven filtering.
- Bulk-first indexing.
- Hybrid search support.
- Configuration-driven behaviour.

---

## 20. Success Criteria

The OpenSearch Service is considered successful when:

- Documents are indexed successfully.
- BM25 searches return relevant results.
- Metadata filters are applied correctly.
- Hybrid retrieval integrates seamlessly with Qdrant.
- Bulk indexing completes efficiently.
- Service meets configured latency objectives.

---

## Metadata

| Property | Value |
|----------|-------|
| Service ID | SERVICE-005 |
| Service Name | OpenSearch Service |
| Type | Infrastructure Service |
| Category | Lexical Search Engine |
| Provider | OpenSearch |
| Owner | Enterprise AI Orchestration Platform |
| Version | 1.0 |
| Status | Implemented |