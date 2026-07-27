# WF-004 – Filesystem Analysis

## 1. Purpose

The Filesystem Analysis workflow enables users to analyze files and directories using natural language queries.

The platform traverses the enterprise file system, identifies relevant files, extracts content, and generates intelligent responses using AI agents.

This workflow assists developers, architects, operations teams, and support engineers in locating information, understanding project structures, and analyzing enterprise documents stored within local or network file systems.

---

## 2. Business Scenario

Enterprise projects often contain thousands of files distributed across multiple directories.

Users frequently need to answer questions such as:

- Summarize this project.
- Which configuration files exist?
- Explain the deployment scripts.
- Find all YAML files.
- Show all Dockerfiles.
- Which documents mention Kubernetes?
- Find all Java classes implementing a specific interface.

Instead of manually browsing folders, users can ask natural language questions and receive context-aware answers.

---

## 3. Trigger

A user submits a filesystem analysis request.

### Example

```text
Analyze the project structure.
```

---

## 4. Preconditions

Before executing this workflow:

- Filesystem access has been configured.
- Required directories are accessible.
- Files have been indexed.
- File metadata has been collected.
- Embeddings have been generated for supported file types.
- Qdrant contains indexed file content.
- WorkflowGraph is initialized.
- Supervisor Agent is available.

---

## 5. Actors

### Primary Actor

- Developer
- Solution Architect
- Enterprise Architect
- DevOps Engineer

### System Components

- Chat API
- Chat Service
- WorkflowGraph
- Supervisor Agent
- Filesystem Agent
- Filesystem Service
- Document Parser
- Embedding Service
- Qdrant
- Reranker
- Gemini LLM

---

## 6. Workflow Overview

```text
+----------------------+
|        User          |
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
|  Filesystem Agent    |
+----------+-----------+
           |
           v
+----------------------+
| Filesystem Service   |
+----------+-----------+
           |
           v
+----------------------+
| Document Parser      |
+----------+-----------+
           |
           v
+----------------------+
| Embedding Service    |
+----------+-----------+
           |
           v
+----------------------+
| Qdrant Vector Search |
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
| Filesystem Analysis  |
+----------------------+
```

---

## 7. Detailed Execution Flow

### Step 1 – User Request

The user submits a filesystem-related question.

---

### Step 2 – Supervisor Decision

The Supervisor Agent classifies the request and selects the Filesystem Agent.

Example:

```json
{
    "agent": "filesystem",
    "user_input": "Analyze the project structure.",
    "parameters": {}
}
```

---

### Step 3 – Filesystem Agent

The Filesystem Agent validates the requested path and prepares the analysis.

---

### Step 4 – File Discovery

The Filesystem Service scans directories and identifies relevant files.

Supported examples include:

- PDF
- DOCX
- TXT
- Markdown
- JSON
- YAML
- XML
- Java
- Python
- JavaScript

---

### Step 5 – Content Retrieval

Relevant file content is retrieved from the indexed knowledge base.

---

### Step 6 – Semantic Search

The user's query is converted into an embedding and submitted to Qdrant.

Relevant file chunks are retrieved.

---

### Step 7 – Reranking

The retrieved chunks are reranked according to semantic relevance.

---

### Step 8 – Context Construction

The selected file content is assembled into a context window.

---

### Step 9 – AI Analysis

Gemini analyzes the retrieved information and generates a comprehensive response.

---

### Step 10 – Response Delivery

The analysis is returned to the user.

---

## 8. Component Responsibilities

| Component | Responsibility |
|------------|----------------|
| Chat API | Receives user requests |
| Chat Service | Initiates workflow |
| WorkflowGraph | Coordinates workflow execution |
| Supervisor Agent | Selects Filesystem Agent |
| Filesystem Agent | Coordinates filesystem analysis |
| Filesystem Service | Reads directories and files |
| Document Parser | Extracts textual content |
| Embedding Service | Generates embeddings |
| Qdrant | Retrieves relevant content |
| Reranker | Improves retrieval quality |
| Gemini LLM | Generates intelligent responses |

---

## 9. Error Handling

| Failure | System Behaviour |
|----------|------------------|
| Directory not found | Return validation error |
| Permission denied | Return authorization error |
| Unsupported file type | Skip file |
| Parsing failure | Log error and continue |
| Embedding failure | Abort workflow |
| Qdrant unavailable | Return service unavailable |
| Gemini unavailable | Return AI service unavailable |

---

## 10. Security Considerations

- Validate filesystem paths.
- Prevent directory traversal attacks.
- Restrict access to authorized directories.
- Enforce role-based authorization.
- Audit filesystem access.
- Protect confidential files.

---

## 11. Performance Considerations

- Cache directory metadata.
- Process files asynchronously.
- Skip unchanged files.
- Retrieve only relevant chunks.
- Monitor filesystem latency.

---

## 12. Future Enhancements

- Real-time filesystem monitoring.
- Incremental indexing.
- Duplicate file detection.
- File comparison.
- Automatic documentation generation.
- Architecture extraction.

---

## 13. Success Criteria

The workflow is considered successful when:

- The Supervisor selects the Filesystem Agent.
- Relevant files are located.
- Indexed content is retrieved successfully.
- Gemini generates an accurate analysis.
- The response is returned within the configured service-level objective (SLO).

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
Filesystem Agent
    │
    ▼
Filesystem Service
    │
    ▼
Document Parser
    │
    ▼
Embedding Service
    │
    ▼
Qdrant
    │
    ▼
Reranker
    │
    ▼
Gemini
    │
    ▼
Filesystem Analysis
```

---

**Workflow ID:** WF-004

**Workflow Name:** Filesystem Analysis

**Version:** 1.0

**Status:** Planned (Version 1.1)

**Owner:** Enterprise AI Orchestration Platform