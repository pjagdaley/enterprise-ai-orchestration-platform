# AI-002 – Retrieval-Augmented Generation (RAG) Architecture

## 1. Purpose

This document describes the Retrieval-Augmented Generation (RAG) architecture implemented by the Enterprise AI Orchestration Platform.

The platform combines semantic search, lexical search, reranking, AI agents, and Large Language Models (LLMs) to generate accurate, grounded, and context-aware responses using enterprise knowledge.

Unlike traditional LLM interactions that rely solely on model knowledge, the platform retrieves relevant enterprise content at query time to improve accuracy, reduce hallucinations, and ensure responses reflect the latest organizational information.

---

# 2. Objectives

The RAG architecture aims to:

- Ground responses in enterprise knowledge
- Minimize hallucinations
- Support large document collections
- Enable scalable retrieval
- Improve answer relevance
- Support enterprise security
- Enable document-level citations
- Reduce LLM token usage
- Support multi-format documents
- Scale independently of the LLM

---

# 3. Scope

The RAG architecture includes:

- Document ingestion
- Document parsing
- Chunking
- Metadata extraction
- Embedding generation
- Vector indexing
- Lexical indexing
- Hybrid retrieval
- Reranking
- Context construction
- Prompt generation
- LLM response generation
- Citation generation

---

# 4. High-Level Architecture

```text
                    Enterprise Documents
                             │
                             ▼
                  Document Ingestion Service
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
      Parser            Metadata Extractor    Registry
         │                   │                 Firestore
         ▼                   │
      Chunking               │
         │                   │
         ▼                   ▼
 Embedding Generation   Metadata Enrichment
         │
         ▼
 ┌───────────────┬─────────────────┐
 ▼               ▼                 ▼
Qdrant      OpenSearch      Object Storage
(Vector DB) (BM25 Index)         (GCS)
        │            │
        └──────┬─────┘
               ▼
        Hybrid Retrieval
               │
               ▼
          Reranking
               │
               ▼
      Context Construction
               │
               ▼
      Prompt Construction
               │
               ▼
          Gemini 2.5
               │
               ▼
      Grounded Response
```

---

# 5. RAG Workflow

```text
User Query
      │
      ▼
Query Understanding
      │
      ▼
Hybrid Search
      │
      ▼
Candidate Documents
      │
      ▼
CrossEncoder Reranking
      │
      ▼
Top Ranked Chunks
      │
      ▼
Prompt Assembly
      │
      ▼
Gemini
      │
      ▼
Validated Response
```

---

# 6. Document Ingestion

The ingestion pipeline prepares enterprise documents for retrieval.

Supported document types include:

- PDF
- DOCX
- TXT
- JSON
- XLSX
- Markdown

Each document passes through:

1. Parsing
2. Metadata extraction
3. Chunk generation
4. Embedding generation
5. Vector indexing
6. Lexical indexing
7. Registry update

---

# 7. Document Parsing

The parser extracts textual content while preserving logical structure.

Typical extracted information includes:

- Titles
- Headings
- Paragraphs
- Lists
- Tables
- Sheet names (Excel)
- JSON paths
- File metadata

Unsupported content should be reported during ingestion.

---

# 8. Chunking

Documents are divided into manageable chunks suitable for embedding and retrieval.

Design goals include:

- Preserve semantic meaning
- Avoid oversized chunks
- Minimize context fragmentation
- Improve retrieval precision

Chunk metadata should include:

- Document ID
- Chunk ID
- Source file
- Section
- Page number (where applicable)
- Chunk index

---

# 9. Metadata Enrichment

Each chunk should include metadata to improve retrieval quality.

Typical metadata:

| Metadata | Purpose |
|----------|---------|
| Document ID | Traceability |
| File Name | Citation |
| File Type | Filtering |
| Department | Access control |
| Business Domain | Search relevance |
| Tags | Classification |
| Version | Document governance |
| Created Date | Freshness |
| Modified Date | Freshness |

Metadata supports filtering, authorization, and governance.

---

# 10. Embedding Generation

Each chunk is converted into a vector representation.

Platform implementation:

| Component | Technology |
|-----------|------------|
| Embedding Model | Vertex AI text-embedding-005 |
| Vector Dimensions | Model-defined |
| Batch Processing | Supported |
| Retry Strategy | Exponential Backoff |

Embedding generation should be repeatable and version-aware.

---

# 11. Vector Index (Qdrant)

Qdrant stores semantic vector representations.

Responsibilities:

- Vector similarity search
- Metadata filtering
- High-performance nearest-neighbor search
- Collection management
- Scalability

Semantic search identifies conceptually related content.

---

# 12. Lexical Index (OpenSearch)

OpenSearch complements semantic search.

Responsibilities include:

- Keyword search
- Exact phrase matching
- Acronym matching
- Numeric lookups
- Structured field search

Lexical retrieval performs well for identifiers, codes, filenames, and technical terms.

---

# 13. Hybrid Retrieval

The platform combines semantic and lexical retrieval.

```text
                User Query
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 Semantic Search           Keyword Search
   (Qdrant)                 (OpenSearch)
         │                       │
         └───────────┬───────────┘
                     ▼
            Candidate Results
```

Benefits include:

- Better recall
- Better precision
- Reduced missed documents
- Stronger handling of enterprise terminology

---

# 14. Reranking

Hybrid retrieval returns candidate chunks that are reranked before being sent to the LLM.

Platform implementation:

| Component | Technology |
|-----------|------------|
| Reranker | BGE CrossEncoder |
| Input | Query + Candidate Chunks |
| Output | Relevance Score |

Only the highest-ranked chunks are included in the prompt.

---

# 15. Context Construction

Selected chunks are assembled into a structured context.

Typical structure:

```text
Document A
Section 2.1
Relevant Content

----------------------

Document B
Section 5.3
Relevant Content

----------------------

Document C
Appendix
Relevant Content
```

Context should preserve document boundaries and source attribution.

---

# 16. Prompt Construction

The prompt combines:

- System prompt
- Conversation history
- Retrieved context
- User request
- Response instructions

The LLM is instructed to prioritize retrieved enterprise knowledge over its pre-trained knowledge whenever relevant.

---

# 17. Response Generation

Gemini generates a response using:

- User intent
- Retrieved evidence
- Conversation history
- System instructions

Responses should remain grounded in retrieved documents.

---

# 18. Citation Strategy

Responses should reference supporting documents whenever possible.

Citation metadata may include:

- Document name
- Section
- Page number
- Chunk identifier

This improves traceability and user confidence.

---

# 19. Security Considerations

The RAG pipeline should enforce:

- Metadata-based authorization
- Document-level access control
- Retrieval filtering
- Prompt injection protection
- Secure prompt construction
- Confidential data protection

Unauthorized documents must never be retrieved or included in prompts.

---

# 20. Performance Considerations

Performance should be monitored for:

- Ingestion throughput
- Embedding latency
- Vector search latency
- Keyword search latency
- Reranking latency
- Prompt construction time
- LLM latency
- End-to-end response time

Each stage should expose operational metrics.

---

# 21. Scalability

The architecture supports independent scaling of:

- Ingestion services
- Embedding generation
- Qdrant
- OpenSearch
- FastAPI
- LangGraph workflows
- AI agents

This allows ingestion and query workloads to evolve independently.

---

# 22. Best Practices

- Keep retrieval separate from generation.
- Preserve metadata throughout the pipeline.
- Combine semantic and lexical retrieval.
- Rerank before prompt construction.
- Minimize unnecessary prompt context.
- Continuously evaluate retrieval quality.
- Monitor latency for every stage.
- Treat retrieval as a first-class AI capability.

---

# 23. Related Documents

- README – AI Documentation
- AI-001 – Prompt Engineering
- AI-003 – Chunking Strategy
- AI-004 – Embedding Strategy
- AI-005 – Hybrid Search
- AI-006 – Reranking Strategy
- AI-007 – Agent Architecture
- TEST-006 – AI and RAG Testing
- SEC-006 – AI and LLM Security

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | AI-002 |
| Title | Retrieval-Augmented Generation (RAG) Architecture |
| Category | AI Documentation |
| Audience | AI Engineers, Architects, Developers, Platform Engineers |
| Version | 1.0 |
| Status | Active |