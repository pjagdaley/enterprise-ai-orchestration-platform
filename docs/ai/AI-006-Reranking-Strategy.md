# AI-006 – Reranking Strategy

## 1. Purpose

This document defines the reranking strategy used by the Enterprise AI Orchestration Platform.

Reranking is the process of evaluating candidate documents returned by the retrieval layer and ordering them according to their relevance to the user's query.

Unlike vector search and lexical search, which retrieve candidate documents independently, reranking jointly evaluates the query and each candidate chunk to identify the most relevant context for Large Language Models (LLMs).

The reranking stage significantly improves response quality while reducing hallucinations and unnecessary prompt tokens.

---

# 2. Objectives

The reranking strategy aims to:

- Improve retrieval precision
- Reduce irrelevant context
- Improve grounded responses
- Reduce hallucinations
- Optimize prompt size
- Improve citation quality
- Increase answer consistency
- Improve enterprise search quality
- Support scalable AI workloads
- Maintain predictable latency

---

# 3. Scope

Reranking applies to:

- User queries
- AI agent retrieval
- Hybrid Search
- RAG workflows
- Prompt construction
- Enterprise search
- Knowledge retrieval

---

# 4. High-Level Architecture

```text
                  User Query
                       │
                       ▼
               Hybrid Retrieval
          (Qdrant + OpenSearch)
                       │
                       ▼
             Candidate Chunks
                 (Top N)
                       │
                       ▼
              CrossEncoder Model
                       │
                       ▼
             Relevance Scores
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

# 5. Why Reranking?

Hybrid retrieval favors **recall**, returning many potentially relevant chunks.

However:

- Some chunks are only partially relevant.
- Some contain unrelated context.
- Similar terminology may produce false positives.
- Semantic retrieval may retrieve conceptually similar but incorrect information.

Reranking improves precision before the LLM generates a response.

---

# 6. CrossEncoder vs BiEncoder

### BiEncoder

Used during retrieval.

Characteristics:

- Independent embeddings
- Very fast
- Scalable
- Approximate similarity

Example:

```text
Query Vector

↓

Vector Similarity

↓

Candidate Results
```

---

### CrossEncoder

Used during reranking.

Characteristics:

- Query and document evaluated together
- Better understanding of context
- Higher accuracy
- Higher computational cost

Example:

```text
Query

+

Candidate Chunk

↓

CrossEncoder

↓

Relevance Score
```

---

# 7. Platform Implementation

Current implementation:

| Component | Technology |
|-----------|------------|
| Retrieval | Qdrant |
| Keyword Search | OpenSearch |
| Reranker | BAAI BGE CrossEncoder |
| Input | Query + Candidate Chunk |
| Output | Relevance Score |

The reranker executes after Hybrid Search and before prompt construction.

---

# 8. Reranking Workflow

```text
User Query
      │
      ▼
Hybrid Search
      │
      ▼
Top 30 Candidate Chunks
      │
      ▼
CrossEncoder Evaluation
      │
      ▼
Relevance Scores
      │
      ▼
Top 5 Chunks
      │
      ▼
Prompt Builder
```

The number of candidate chunks and the final selected chunks should be configurable.

---

# 9. Candidate Selection

The retrieval layer should prioritize recall.

Example:

| Stage | Count |
|---------|------:|
| Semantic Search | 20 |
| Lexical Search | 20 |
| Combined Candidates | 35 |
| After Deduplication | 28 |
| After Reranking | 5 |

Selecting too few candidates may reduce answer quality, while selecting too many increases reranking latency.

---

# 10. Relevance Scoring

The CrossEncoder evaluates:

- Query intent
- Semantic similarity
- Contextual relevance
- Phrase relationships
- Sentence meaning

Output:

```text
Query

+

Chunk

↓

Score = 0.97
```

Higher scores indicate stronger relevance.

---

# 11. Prompt Context Selection

Only the highest-ranked chunks are included.

Example:

```text
Rank 1

Authentication Architecture

Rank 2

OAuth Flow

Rank 3

JWT Validation

Rank 4

API Security

Rank 5

Identity Management
```

This minimizes irrelevant context while maximizing evidence quality.

---

# 12. Latency Considerations

CrossEncoder inference is significantly slower than vector search.

Latency depends on:

- Candidate count
- Model size
- Hardware
- Batch size
- Input length

The reranking stage should be monitored independently.

---

# 13. Batch Processing

Candidate chunks should be evaluated in batches.

Benefits:

- Better CPU utilization
- Better GPU utilization
- Lower overhead
- Improved throughput

Batch size should be configurable based on available resources.

---

# 14. Deployment Considerations

Deployment options include:

### CPU

Advantages:

- Lower infrastructure cost
- Simpler deployment

Limitations:

- Higher latency
- Lower throughput

---

### GPU

Advantages:

- Faster inference
- Higher throughput
- Better scalability

Limitations:

- Higher operational cost
- Increased infrastructure complexity

Deployment should be selected based on expected workload and response time objectives.

---

# 15. Monitoring

Monitor:

- Candidate count
- Reranking latency
- Average relevance score
- Top-K distribution
- Batch size
- Throughput
- CPU utilization
- GPU utilization
- Failure rate

These metrics help identify performance bottlenecks and retrieval quality issues.

---

# 16. Evaluation Metrics

Retrieval quality should be measured using:

| Metric | Purpose |
|---------|---------|
| Precision@K | Relevant results in Top-K |
| Recall@K | Retrieval completeness |
| Mean Reciprocal Rank (MRR) | First relevant result ranking |
| NDCG | Ranking quality |
| MAP | Mean Average Precision |

Evaluation datasets should represent real enterprise queries.

---

# 17. Failure Handling

If the reranker is unavailable:

1. Log the failure.
2. Return the hybrid retrieval results.
3. Mark the response as generated without reranking.
4. Continue serving requests where appropriate.

This fallback maintains platform availability while acknowledging reduced retrieval precision.

---

# 18. Security Considerations

The reranking stage should:

- Respect metadata-based authorization
- Process only retrieved candidates
- Prevent unauthorized document inclusion
- Log reranking operations
- Avoid exposing internal model details
- Validate candidate integrity

Security filtering must occur before prompt construction.

---

# 19. Future Enhancements

Potential improvements include:

- Domain-specific rerankers
- Multilingual reranking
- Learning-to-rank models
- Adaptive Top-K selection
- Intent-aware reranking
- Personalized ranking
- Lightweight rerankers for low-latency workloads
- Distributed reranking services

---

# 20. Best Practices

- Retrieve broadly and rerank narrowly.
- Evaluate reranking quality using production queries.
- Tune candidate count independently from final Top-K.
- Batch reranking requests efficiently.
- Monitor reranking latency separately.
- Preserve retrieval metadata through reranking.
- Implement graceful fallback behavior.
- Reassess reranking models as retrieval requirements evolve.

---

# 21. Related Documents

- README – AI Documentation
- AI-002 – RAG Architecture
- AI-004 – Embedding Strategy
- AI-005 – Hybrid Search
- AI-007 – Agent Architecture
- AI-010 – AI Evaluation and Observability
- TEST-006 – AI and RAG Testing

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | AI-006 |
| Title | Reranking Strategy |
| Category | AI Documentation |
| Audience | AI Engineers, Search Engineers, Platform Engineers, Architects |
| Version | 1.0 |
| Status | Active |