# AI-005 – Hybrid Search Strategy

## 1. Purpose

This document defines the Hybrid Search strategy used by the Enterprise AI Orchestration Platform.

Hybrid Search combines semantic vector search with lexical keyword search to maximize retrieval quality across enterprise knowledge bases.

Semantic search identifies conceptually related information, while lexical search excels at exact keyword, identifier, acronym, code, filename, and numeric searches. By combining both approaches, the platform achieves higher recall, higher precision, and better grounding for Retrieval-Augmented Generation (RAG).

---

# 2. Objectives

The Hybrid Search strategy aims to:

- Improve retrieval accuracy
- Increase document recall
- Improve search precision
- Reduce missed documents
- Support enterprise terminology
- Support structured identifiers
- Improve RAG quality
- Reduce hallucinations
- Support metadata filtering
- Scale independently of AI models

---

# 3. Scope

Hybrid Search applies to:

- User queries
- AI agent retrieval
- RAG workflows
- Enterprise search
- Metadata filtering
- Context construction
- Prompt generation

---

# 4. High-Level Architecture

```text
                    User Query
                         │
                         ▼
                Query Processing
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   Semantic Search                Lexical Search
      (Qdrant)                    (OpenSearch)
          │                             │
          ▼                             ▼
 Semantic Candidates           Keyword Candidates
          │                             │
          └──────────────┬──────────────┘
                         ▼
                  Result Fusion
                         │
                         ▼
               Metadata Filtering
                         │
                         ▼
               CrossEncoder Reranker
                         │
                         ▼
                 Top Ranked Chunks
                         │
                         ▼
                Context Construction
                         │
                         ▼
                     Gemini 2.5
```

---

# 5. Why Hybrid Search?

No single retrieval strategy performs well for every query.

### Semantic Search excels at:

- Meaning
- Intent
- Synonyms
- Concept similarity
- Natural language questions

### Lexical Search excels at:

- Product codes
- Error messages
- Filenames
- IDs
- Version numbers
- Acronyms
- Exact phrases

Combining both produces more complete search results.

---

# 6. Semantic Search

Semantic search converts the user query into an embedding vector.

```text
User Query
      │
      ▼
Embedding Service
      │
      ▼
Query Vector
      │
      ▼
Qdrant Similarity Search
      │
      ▼
Candidate Chunks
```

Advantages:

- Understands meaning
- Handles paraphrasing
- Supports natural language
- Finds related concepts

Limitations:

- Weak for exact identifiers
- May miss rare terminology
- May confuse similar concepts

---

# 7. Lexical Search

Lexical search uses BM25 indexing.

```text
User Query
      │
      ▼
OpenSearch
      │
      ▼
Keyword Ranking
      │
      ▼
Candidate Chunks
```

Advantages:

- Exact matching
- Excellent for enterprise identifiers
- Fast
- Deterministic

Limitations:

- Does not understand meaning
- Poor synonym handling
- Sensitive to wording

---

# 8. Retrieval Workflow

```text
User Query
      │
      ▼
Normalize Query
      │
      ▼
Execute Searches in Parallel
      │
 ┌────┴─────┐
 ▼          ▼
Qdrant   OpenSearch
 │          │
 └────┬─────┘
      ▼
Merge Results
      │
      ▼
Remove Duplicates
      │
      ▼
Metadata Filtering
      │
      ▼
Reranking
      │
      ▼
Prompt Construction
```

Parallel execution minimizes overall latency.

---

# 9. Result Fusion

The platform merges candidate results from both retrieval systems.

Typical process:

1. Execute semantic search.
2. Execute lexical search.
3. Combine candidates.
4. Remove duplicates.
5. Preserve source scores.
6. Apply metadata filters.
7. Pass candidates to the reranker.

Fusion should maximize recall before reranking.

---

# 10. Metadata Filtering

Metadata filtering ensures only authorized and relevant documents are considered.

Example filters include:

- Department
- Business unit
- Project
- Document type
- Version
- Language
- Security classification
- Tenant
- Region

Filtering should occur before reranking whenever possible.

---

# 11. Score Normalization

Semantic and lexical scores use different scales.

Before combining results, scores should be normalized.

Example approaches:

- Min-Max normalization
- Z-score normalization
- Rank-based normalization
- Reciprocal Rank Fusion (RRF)

The platform should treat retrieval scores as inputs to reranking rather than final relevance indicators.

---

# 12. Query Routing

Some queries benefit from specialized retrieval.

Examples:

| Query Type | Preferred Strategy |
|------------|--------------------|
| Natural language | Semantic |
| Error code | Lexical |
| Product ID | Lexical |
| Policy question | Hybrid |
| Technical design | Hybrid |
| Configuration value | Lexical |
| General knowledge | Semantic |

Future versions may dynamically route queries based on intent classification.

---

# 13. Duplicate Elimination

The same chunk may be returned by both retrieval systems.

Duplicates should be removed using:

- Document ID
- Chunk ID
- Content hash

The highest confidence score should be retained for downstream processing.

---

# 14. Retrieval Service

The platform encapsulates retrieval behind a dedicated service.

Responsibilities include:

- Query normalization
- Parallel execution
- Metadata filtering
- Result fusion
- Duplicate removal
- Score normalization
- Reranker invocation
- Context assembly

This abstraction isolates LangGraph workflows from retrieval implementation details.

---

# 15. Performance Considerations

Monitor:

- Qdrant latency
- OpenSearch latency
- Fusion time
- Metadata filtering time
- Reranking latency
- End-to-end retrieval latency
- Recall
- Precision

Retrieval performance should be continuously evaluated.

---

# 16. Security Considerations

Hybrid Search should enforce:

- Access control
- Metadata authorization
- Tenant isolation
- Secure query handling
- Audit logging
- Prompt injection protection
- Retrieval authorization

Unauthorized content must never enter the LLM context.

---

# 17. Scalability

The architecture supports independent scaling of:

- Qdrant
- OpenSearch
- Retrieval Service
- Reranking Service

This allows indexing and retrieval capacity to grow without affecting LLM infrastructure.

---

# 18. Future Enhancements

Potential improvements include:

- Reciprocal Rank Fusion (RRF)
- Adaptive retrieval strategies
- Query intent classification
- Graph-based retrieval
- Knowledge graph integration
- Personalized retrieval
- Temporal ranking
- Multi-vector retrieval
- Multimodal retrieval

---

# 19. Best Practices

- Execute semantic and lexical searches in parallel.
- Apply metadata filtering before reranking.
- Normalize retrieval scores before fusion.
- Preserve retrieval metadata for auditing.
- Rerank candidate results before prompt construction.
- Continuously evaluate recall and precision.
- Monitor retrieval latency separately from LLM latency.
- Keep retrieval independent from generation.

---

# 20. Related Documents

- README – AI Documentation
- AI-002 – RAG Architecture
- AI-003 – Chunking Strategy
- AI-004 – Embedding Strategy
- AI-006 – Reranking Strategy
- AI-007 – Agent Architecture
- TEST-006 – AI and RAG Testing

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | AI-005 |
| Title | Hybrid Search Strategy |
| Category | AI Documentation |
| Audience | AI Engineers, Search Engineers, Platform Engineers, Architects |
| Version | 1.0 |
| Status | Active |