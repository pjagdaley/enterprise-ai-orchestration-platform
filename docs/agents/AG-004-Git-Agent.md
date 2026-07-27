# AG-004 – Git Agent

## 1. Purpose

The Git Agent is responsible for analyzing Git repositories and providing intelligent insights about source code, project structure, commit history, branches, pull requests, and software architecture.

The Git Agent enables developers and architects to interact with source code repositories using natural language instead of manually searching through files or Git history.

---

## 2. Responsibilities

The Git Agent is responsible for:

- Accessing Git repositories.
- Analyzing repository structure.
- Searching source code.
- Retrieving commit history.
- Reviewing branches and tags.
- Inspecting pull requests.
- Identifying contributors.
- Retrieving project documentation.
- Generating architecture explanations.

The Git Agent delegates repository operations to Git tools and services rather than interacting directly with Git repositories.

---

## 3. Position within the Architecture

```text
                   User
                     │
                     ▼
              Supervisor Agent
                     │
                     ▼
                 Git Agent
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
   Git Service            Tool Registry
         │                       │
         ▼                       ▼
   Git Repository          MCP Server
         │
         ▼
    Gemini LLM
         │
         ▼
 Repository Analysis
```

---

## 4. Business Responsibilities

Typical requests include:

- Explain this repository.
- Describe the project architecture.
- Find a specific class.
- Show where authentication is implemented.
- Explain the deployment pipeline.
- List recent commits.
- Identify affected modules.
- Summarize recent code changes.

---

## 5. Inputs

| Parameter | Description |
|-----------|-------------|
| User Query | Natural language request |
| Repository URL | Git repository location |
| Branch | Target branch |
| Conversation Context | Previous chat history |

---

## 6. Outputs

Example response:

```json
{
  "repository": "enterprise-ai-orchestration-platform",
  "summary": "...",
  "files_analyzed": 42,
  "commits_reviewed": 18
}
```

---

## 7. Processing Pipeline

```text
Receive Request
      │
      ▼
Validate Repository
      │
      ▼
Select Git Operation
      │
      ▼
Retrieve Repository Data
      │
      ▼
Analyze Source Code
      │
      ▼
Build Context
      │
      ▼
Gemini Analysis
      │
      ▼
Repository Insight
```

---

## 8. Supported Operations

The Git Agent supports:

| Operation | Description |
|-----------|-------------|
| Repository Summary | High-level overview |
| Code Search | Locate classes, methods, or files |
| Commit History | Review recent commits |
| Branch Analysis | Inspect branches |
| Pull Request Review | Analyze PRs |
| Architecture Discovery | Explain system structure |
| Dependency Analysis | Identify module dependencies |

---

## 9. Interaction with Other Components

| Component | Interaction |
|-----------|-------------|
| Supervisor Agent | Receives routing decisions |
| WorkflowGraph | Executes workflow |
| Git Service | Performs repository operations |
| Tool Registry | Resolves Git tools |
| MCP Server | Invokes external Git services |
| Gemini LLM | Generates explanations |

---

## 10. Prompt Strategy

Example system prompt:

```text
You are an expert Software Architect.

Analyze the supplied repository information and answer using only the retrieved repository data.

Explain architectural decisions clearly.

Do not invent repository contents.
```

---

## 11. Error Handling

| Failure | Behaviour |
|----------|-----------|
| Repository unavailable | Return repository access error |
| Repository not found | Return validation error |
| Permission denied | Return authorization error |
| Tool unavailable | Retry or return service unavailable |
| Empty repository | Inform the user |

---

## 12. Security Considerations

The Git Agent:

- Uses authenticated repository access.
- Honors repository permissions.
- Does not expose private repositories.
- Audits repository access.
- Sanitizes repository metadata.

---

## 13. Performance Considerations

- Cache repository metadata.
- Reuse cloned repositories.
- Retrieve only required files.
- Limit commit history.
- Optimize source code indexing.

---

## 14. Technology Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | API layer |
| LangGraph | Workflow orchestration |
| Git | Source control |
| MCP | Tool integration |
| Gemini 2.5 Flash | Code analysis |
| Qdrant | Indexed source code retrieval (optional) |

---

## 15. Future Enhancements

Future enhancements may include:

- Pull request generation.
- Automated code review.
- Security vulnerability analysis.
- Code quality metrics.
- Architecture diagram generation.
- Repository comparison.

---

## 16. Sequence Diagram

```text
User
 │
 ▼
Supervisor Agent
 │
 ▼
Git Agent
 │
 ├────────► Git Service
 │
 ├────────► Tool Registry
 │
 ├────────► MCP Server
 │
 ▼
Gemini
 │
 ▼
Repository Analysis
```

---

## 17. Design Principles

The Git Agent follows these architectural principles:

- Read-only repository access.
- Separation of analysis and retrieval.
- Stateless execution.
- Tool abstraction through MCP.
- Extensible repository operations.

---

## 18. Success Criteria

The Git Agent is considered successful when:

- Repository access is validated.
- Requested repository information is retrieved.
- Analysis is accurate and grounded in repository data.
- Results are returned within the configured service-level objective (SLO).

---

## Metadata

| Property | Value |
|----------|-------|
| Agent ID | AG-004 |
| Agent Name | Git Agent |
| Type | Specialized AI Agent |
| Category | Source Code Analysis |
| Owner | Enterprise AI Orchestration Platform |
| Version | 1.0 |
| Status | Planned (Version 2.0) |