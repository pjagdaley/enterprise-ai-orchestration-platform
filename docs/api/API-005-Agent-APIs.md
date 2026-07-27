# API-005 – Agent APIs

## 1. Purpose

This document describes the Agent APIs exposed by the Enterprise AI Orchestration Platform.

The Agent APIs provide a standardized interface for discovering, executing, and monitoring AI agents.

Agents encapsulate specialized business capabilities and may:

- Answer user questions
- Execute workflows
- Invoke tools
- Retrieve enterprise knowledge
- Coordinate with other agents
- Perform reasoning tasks

The platform supports both single-agent execution and multi-agent orchestration through LangGraph.

---

# 2. Scope

The Agent APIs support:

- Agent discovery
- Agent execution
- Agent capability inspection
- Agent status
- Agent execution history
- Multi-agent orchestration
- Tool invocation

---

# 3. Agent Architecture

```text
                 Client Application
                         │
                         ▼
              POST /api/v1/agents/{id}/execute
                         │
                         ▼
                  Agent Controller
                         │
                         ▼
                  Agent Service
                         │
               WorkflowGraph Engine
                         │
        ┌────────────────┼─────────────────┐
        ▼                ▼                 ▼
 Supervisor Agent  Knowledge Agent   Planner Agent
        │
        ▼
   Tool Registry
        │
        ▼
 External Systems
```

---

# 4. Agent Execution Flow

```text
Receive Request
       │
       ▼
Authenticate User
       │
       ▼
Load Agent
       │
       ▼
Validate Permissions
       │
       ▼
Execute WorkflowGraph
       │
       ▼
Invoke Tools (Optional)
       │
       ▼
Generate Response
       │
       ▼
Persist Execution
       │
       ▼
Return Result
```

---

# 5. API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/agents | List available agents |
| GET | /api/v1/agents/{agentId} | Retrieve agent details |
| POST | /api/v1/agents/{agentId}/execute | Execute an agent |
| GET | /api/v1/agents/{agentId}/status | Retrieve current status |
| GET | /api/v1/agents/{agentId}/history | Retrieve execution history |
| GET | /api/v1/agents/{agentId}/capabilities | Retrieve supported capabilities |

---

# 6. List Agents

## Endpoint

```http
GET /api/v1/agents
```

### Description

Returns all registered agents.

### Response

```json
{
  "agents": [
    {
      "agentId": "knowledge-agent",
      "name": "Knowledge Agent",
      "type": "Knowledge Retrieval",
      "status": "ACTIVE"
    },
    {
      "agentId": "planner-agent",
      "name": "Planner Agent",
      "type": "Task Planning",
      "status": "ACTIVE"
    }
  ]
}
```

---

# 7. Get Agent Details

## Endpoint

```http
GET /api/v1/agents/{agentId}
```

### Response

```json
{
  "agentId": "knowledge-agent",
  "name": "Knowledge Agent",
  "description": "Retrieves enterprise knowledge.",
  "version": "1.0",
  "status": "ACTIVE",
  "owner": "AI Platform Team"
}
```

---

# 8. Execute Agent

## Endpoint

```http
POST /api/v1/agents/{agentId}/execute
```

### Description

Executes the specified agent.

### Request

```json
{
  "sessionId": "session-123",
  "input": {
    "query": "Summarize the enterprise architecture principles."
  }
}
```

### Response

```json
{
  "executionId": "EXEC-1001",
  "status": "COMPLETED",
  "result": {
    "answer": "Enterprise architecture principles..."
  }
}
```

---

# 9. Agent Status

## Endpoint

```http
GET /api/v1/agents/{agentId}/status
```

### Response

```json
{
  "agentId": "knowledge-agent",
  "status": "ACTIVE",
  "lastExecution": "2026-08-15T09:42:00Z",
  "health": "HEALTHY"
}
```

---

# 10. Agent Execution History

## Endpoint

```http
GET /api/v1/agents/{agentId}/history
```

### Response

```json
{
  "executions": [
    {
      "executionId": "EXEC-1001",
      "status": "COMPLETED",
      "startedAt": "2026-08-15T09:40:12Z",
      "durationMs": 2643
    }
  ]
}
```

---

# 11. Agent Capabilities

## Endpoint

```http
GET /api/v1/agents/{agentId}/capabilities
```

### Response

```json
{
  "agentId": "knowledge-agent",
  "capabilities": [
    "Knowledge Retrieval",
    "Hybrid Search",
    "Citation Generation",
    "Answer Summarization"
  ]
}
```

---

# 12. Agent States

| State | Description |
|--------|-------------|
| ACTIVE | Ready for execution |
| BUSY | Processing requests |
| DISABLED | Temporarily unavailable |
| MAINTENANCE | Under maintenance |
| ERROR | Execution unavailable |

---

# 13. Authentication

All Agent APIs require a valid JWT access token.

```http
Authorization: Bearer <access_token>
```

Administrative operations may require elevated permissions.

---

# 14. HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 202 | Execution accepted |
| 400 | Invalid request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Agent not found |
| 409 | Agent unavailable |
| 429 | Rate limited |
| 500 | Internal server error |

---

# 15. Error Response

```json
{
  "success": false,
  "error": {
    "code": "AGENT_UNAVAILABLE",
    "message": "Requested agent is currently unavailable."
  }
}
```

---

# 16. Security Considerations

The Agent APIs should:

- Require authenticated users.
- Enforce role-based authorization.
- Validate input payloads.
- Restrict tool execution based on permissions.
- Log all agent executions.
- Apply rate limiting.
- Protect against prompt injection attacks.

---

# 17. Performance Considerations

To optimize agent execution:

- Cache reusable context where appropriate.
- Execute independent tools in parallel.
- Monitor execution latency.
- Limit recursion depth in workflows.
- Reuse initialized models when possible.
- Collect execution metrics for optimization.

---

# 18. Best Practices

- Design agents with a single primary responsibility.
- Keep workflows deterministic where possible.
- Validate all external tool responses.
- Monitor execution success rates.
- Maintain versioned agent definitions.
- Log execution metadata for observability.

---

# 19. Related Documents

- API-002 – Chat APIs
- API-007 – Tool Registry APIs
- AG-001 – Supervisor Agent
- AG-002 – Knowledge Agent
- AG-003 – Planner Agent
- WF-002 – Agent Execution Workflow
- SERVICE-001 – Gemini Service

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | API-005 |
| Title | Agent APIs |
| Category | API Documentation |
| Audience | Backend Developers, AI Engineers, Integration Engineers |
| Version | 1.0 |
| Status | Active |