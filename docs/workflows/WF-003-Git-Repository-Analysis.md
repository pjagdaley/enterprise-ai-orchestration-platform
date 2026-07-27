# WF-003 – Git Repository Analysis

## 1. Purpose

The Git Repository Analysis workflow enables users to analyze source code repositories using natural language queries.

The platform clones or accesses a Git repository, indexes the project, retrieves relevant source code, and generates intelligent responses using AI agents.

This workflow assists developers, architects, and engineering teams in understanding unfamiliar codebases, accelerating onboarding, and improving software maintenance.

---

## 2. Business Scenario

Modern enterprise applications often consist of thousands of source files distributed across multiple repositories.

Developers spend significant time locating business logic, understanding system architecture, and identifying dependencies.

Instead of manually browsing the repository, users can ask questions such as:

- Explain the architecture of this project.
- How is authentication implemented?
- Where is the RAG Agent implemented?
- Which APIs call Gemini?
- Show me the document ingestion pipeline.

The platform analyzes the repository and generates accurate, context-aware answers.

---

## 3. Trigger

A user submits a Git repository analysis request.

### Example

```text
Explain the architecture of this repository.
```

---

## 4. Preconditions

The following conditions must be satisfied:

- Git repository is accessible.
- Repository has been cloned or indexed.
- Source files have been parsed.
- Source code has been chunked.
- Embeddings have been generated.
- Source code has been indexed in Qdrant.
- WorkflowGraph is initialized.
- Supervisor Agent is available.

---

## 5. Actors

### Primary Actor

- Developer
- Software Architect
- Enterprise Architect

### System Components

- Chat API
- Chat Service
- WorkflowGraph
- Supervisor Agent
- Git Agent
- Git Service
- Source Code Parser
- Embedding Service
- Qdrant
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
|      Git Agent       |
+----------+-----------+
           |
           v
+----------------------+
|     Git Service      |
+----------+-----------+
           |
           v
+----------------------+
| Source Code Index    |
+----------+-----------+
           |
           v
+----------------------+
|      Qdrant          |
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
| Repository Analysis  |
+----------------------+
```

---

## 7. Detailed Execution Flow

### Step 1 – User Request

The user submits a natural language question about a Git repository.

---

### Step 2 – Supervisor Decision

The Supervisor Agent classifies the request and selects the Git Agent.

Example:

```json
{
  "agent": "git",
  "user_input": "Explain the repository architecture.",
  "parameters": {}
}
```

---

### Step 3 – Git Agent Execution

The Git Agent validates repository access and initiates source code analysis.

---

### Step 4 – Source Code Retrieval

Relevant source files are retrieved from the indexed repository.

---

### Step 5 – Semantic Search

The query embedding is generated and submitted to Qdrant to retrieve the most relevant code fragments.

---

### Step 6 – Reranking

Retrieved code snippets are reranked according to semantic relevance.

---

### Step 7 – Context Construction

The selected code fragments are combined into a structured context.

---

### Step 8 – AI Analysis

Gemini analyzes the retrieved source code and generates a natural language explanation.

---

### Step 9 – Response Delivery

The analysis is returned to the user.

---

## 8. Component Responsibilities

| Component | Responsibility |
|------------|----------------|
| Chat API | Receives requests |
| Chat Service | Starts workflow |
| WorkflowGraph | Orchestrates execution |
| Supervisor Agent | Selects Git Agent |
| Git Agent | Coordinates repository analysis |
| Git Service | Accesses repository |
| Embedding Service | Generates embeddings |
| Qdrant | Retrieves relevant code |
| Reranker | Improves retrieval quality |
| Gemini | Generates explanations |

---

## 9. Error Handling

| Failure | System Behaviour |
|----------|------------------|
| Repository unavailable | Return validation error |
| Repository access denied | Return authorization error |
| Embedding failure | Abort workflow |
| Qdrant unavailable | Return service unavailable |
| Gemini unavailable | Return AI service unavailable |

---

## 10. Security Considerations

- Authenticate users.
- Validate repository permissions.
- Restrict private repository access.
- Protect source code confidentiality.
- Audit repository access.

---

## 11. Performance Considerations

- Index repositories incrementally.
- Cache repository metadata.
- Limit retrieved source code chunks.
- Execute retrieval asynchronously.
- Monitor retrieval latency.

---

## 12. Future Enhancements

- Multi-repository analysis.
- Pull Request analysis.
- Code quality assessment.
- Security vulnerability detection.
- Architecture diagram generation.
- Dependency visualization.

---

## 13. Success Criteria

The workflow is considered successful when:

- The Supervisor selects the Git Agent.
- Relevant source code is retrieved.
- Gemini generates an accurate explanation.
- The response is delivered within the configured SLA.

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
Git Agent
    │
    ▼
Git Service
    │
    ▼
Source Code Retrieval
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
Repository Analysis
```

---

**Workflow ID:** WF-003

**Workflow Name:** Git Repository Analysis

**Version:** 1.0

**Status:** Planned (Version 1.1)

**Owner:** Enterprise AI Orchestration Platform