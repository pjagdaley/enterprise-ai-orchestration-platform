# WF-001 – Enterprise Knowledge Search

## 1. Purpose

The Enterprise Knowledge Search workflow enables users to ask natural language questions about enterprise knowledge stored within the platform. The system retrieves the most relevant information using Retrieval-Augmented Generation (RAG) and generates an accurate, context-aware response using a Large Language Model (LLM).

This workflow represents the primary interaction pattern of the Enterprise AI Orchestration Platform.

---

## 2. Business Scenario

Enterprise knowledge is typically distributed across multiple document repositories, including architecture documents, policies, technical specifications, operational procedures, and project documentation.

Instead of manually searching these repositories, users can ask questions in natural language. The platform retrieves the most relevant information and generates a concise, accurate response.

### Example Questions

- What is Retrieval-Augmented Generation (RAG)?
- What are the components of the Enterprise AI Platform?
- Explain the document ingestion pipeline.
- How does hybrid retrieval work?
- What is the role of the Supervisor Agent?

---

## 3. Trigger

A user submits a knowledge-related question through the Chat API.

### Example

```text
What is RAG?
```

---

## 4. Preconditions

Before executing this workflow, the following conditions must be satisfied:

- Enterprise documents have been uploaded.
- Documents have been parsed successfully.
- Documents have been chunked.
- Embeddings have been generated.
- Chunks have been indexed in Qdrant.
- OpenSearch index is available (optional).
- Gemini models are accessible.
- WorkflowGraph has been initialized.
- Supervisor Agent is running.

---

## 5. Actors

### Primary Actor

- End User

### System Components

- Chat API
- Chat Service
- WorkflowGraph
- Supervisor Agent
- Enterprise RAG Agent
- Embedding Service
- Qdrant Vector Database
- OpenSearch (Optional)
- Hybrid Retriever
- Reranker
- Gemini LLM

---

## 6. Workflow Overview

```text
+----------------------+
|       User           |
+----------+-----------+
           |
           v
+----------------------+
|      Chat API        |
+----------+-----------+
           |
           v
+----------------------+
|    Chat Service      |
+----------+-----------+
           |
           v
+----------------------+
|    WorkflowGraph     |
+----------+-----------+
           |
           v
+----------------------+
|  Supervisor Agent    |
+----------+-----------+
           |
           v
+----------------------+
| Enterprise RAG Agent |
+----------+-----------+
           |
           +-----------------------------+
           |                             |
           |                             |
           v                             v
+-------------------+        +----------------------+
| Embedding Service |        | OpenSearch (BM25)    |
+---------+---------+        +----------+-----------+
          |                             |
          |                             |
          v                             |
+-------------------+                   |
|      Qdrant       |<------------------+
+---------+---------+
          |
          v
+----------------------+
| Hybrid Retrieval     |
+----------+-----------+
           |
           v
+----------------------+
|      Reranker        |
+----------+-----------+
           |
           v
+----------------------+
|     Gemini LLM       |
+----------+-----------+
           |
           v
+----------------------+
|     User Response    |
+----------------------+
```

---

## 7. Detailed Execution Flow

### Step 1 – Receive Request

The Chat API receives the user's natural language query and forwards it to the Chat Service.

---

### Step 2 – Start Workflow

The Chat Service invokes the WorkflowGraph, which orchestrates the execution of AI workflows.

---

### Step 3 – Supervisor Decision

The Supervisor Agent analyzes the user's request and determines which agent should execute the request.

Example:

```json
{
  "agent": "rag",
  "user_input": "What is RAG?",
  "parameters": {}
}
```

---

### Step 4 – Enterprise RAG Agent

The Enterprise RAG Agent receives the request and begins the retrieval process.

---

### Step 5 – Query Embedding

The user's question is converted into a semantic vector using the configured embedding model.

Current Model:

- Gemini Text Embedding 005

---

### Step 6 – Semantic Search

The generated embedding is submitted to Qdrant.

Qdrant returns the most semantically relevant document chunks.

---

### Step 7 – Lexical Search (Optional)

If Hybrid Search is enabled, the same query is executed against OpenSearch using BM25.

If OpenSearch is unavailable, the platform gracefully falls back to semantic search without interrupting the workflow.

---

### Step 8 – Hybrid Retrieval

Semantic search results and lexical search results are merged into a unified candidate list.

---

### Step 9 – Reranking

The merged candidate list is reranked using the configured Cross-Encoder model.

The highest-ranked document chunks are selected.

---

### Step 10 – Prompt Construction

The selected document chunks are combined with the user's question to construct the final prompt supplied to the LLM.

---

### Step 11 – Answer Generation

Gemini generates a response using only the retrieved enterprise knowledge.

---

### Step 12 – Return Response

The generated response is returned to the Chat API and delivered to the user.

---

## 8. Component Responsibilities

| Component | Responsibility |
|------------|----------------|
| Chat API | Receives user requests |
| Chat Service | Initiates workflow execution |
| WorkflowGraph | Orchestrates AI workflows |
| Supervisor Agent | Determines the appropriate agent |
| Enterprise RAG Agent | Executes enterprise knowledge retrieval |
| Embedding Service | Generates semantic embeddings |
| Qdrant | Performs semantic vector search |
| OpenSearch | Performs lexical BM25 search |
| Hybrid Retriever | Merges semantic and lexical results |
| Reranker | Improves search relevance |
| Gemini LLM | Generates the final response |

---

## 9. Error Handling

| Failure Scenario | System Behaviour |
|------------------|------------------|
| Invalid user request | Return validation error |
| Embedding generation failure | Abort workflow |
| Qdrant unavailable | Return service unavailable |
| OpenSearch unavailable | Continue using semantic search only |
| Reranker failure | Use retrieved documents without reranking |
| Gemini unavailable | Return AI service unavailable |

---

## 10. Security Considerations

- Authenticate all API requests.
- Validate user input.
- Restrict document access based on authorization policies.
- Protect against prompt injection attacks.
- Log requests for auditing and monitoring.
- Encrypt data in transit using HTTPS.
- Encrypt sensitive data at rest.

---

## 11. Performance Considerations

- Cache frequently requested embeddings where appropriate.
- Execute semantic and lexical retrieval in parallel.
- Limit the number of retrieved chunks before reranking.
- Configure timeouts for external services.
- Use graceful fallback when optional services are unavailable.
- Monitor latency for embedding generation, retrieval, reranking, and LLM inference.

---

## 12. Future Enhancements

- Metadata-aware retrieval.
- Multi-collection search.
- Folder priority search.
- Query rewriting.
- Conversational memory integration.
- Multi-agent collaboration.
- Dynamic retrieval strategies.
- Response citation support.

---

## 13. Success Criteria

The workflow is considered successful when:

- The Supervisor selects the Enterprise RAG Agent.
- Relevant documents are retrieved from Qdrant.
- Hybrid retrieval executes successfully or falls back gracefully.
- Gemini generates a context-aware response.
- The response is returned to the user within the configured service-level objective (SLO).

---

## Workflow Summary

```text
User
    │
    ▼
Chat API
    │
    ▼
Chat Service
    │
    ▼
WorkflowGraph
    │
    ▼
Supervisor Agent
    │
    ▼
Enterprise RAG Agent
    │
    ├────────► Embedding Service
    │
    ├────────► Qdrant Vector Search
    │
    ├────────► OpenSearch (Optional)
    │
    ├────────► Hybrid Retrieval
    │
    ├────────► Reranker
    │
    ▼
Gemini LLM
    │
    ▼
User Response
```

---

**Workflow ID:** WF-001

**Workflow Name:** Enterprise Knowledge Search

**Version:** 1.0

**Status:** Implemented

**Owner:** Enterprise AI Orchestration Platform