# API-006 – Workflow APIs

## 1. Purpose

This document describes the Workflow APIs exposed by the Enterprise AI Orchestration Platform.

Workflow APIs enable client applications to:

- Discover available workflows
- Execute workflows
- Monitor workflow execution
- Cancel running workflows
- Retrieve workflow execution history
- Inspect workflow state
- Support long-running AI workflows

The platform uses LangGraph to orchestrate workflow execution.

---

# 2. Scope

Workflow APIs support:

- Workflow discovery
- Workflow execution
- Workflow monitoring
- Workflow cancellation
- Workflow history
- Workflow state inspection
- Human approval workflows
- Multi-agent orchestration

---

# 3. Workflow Architecture

```text
              Client Application
                      │
                      ▼
      POST /api/v1/workflows/{workflowId}/execute
                      │
                      ▼
            Workflow Controller
                      │
                      ▼
             Workflow Service
                      │
                      ▼
               LangGraph Engine
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
Supervisor Agent  Planner Agent  Knowledge Agent
      │
      ▼
 Tool Registry
      │
      ▼
External Services
```

---

# 4. Workflow Execution Lifecycle

```text
Workflow Requested
         │
         ▼
Validate Request
         │
         ▼
Create Execution
         │
         ▼
Initialize LangGraph
         │
         ▼
Execute Workflow Nodes
         │
         ▼
Invoke Tools
         │
         ▼
Persist State
         │
         ▼
Workflow Completed
```

---

# 5. API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/workflows | List workflows |
| GET | /api/v1/workflows/{workflowId} | Workflow details |
| POST | /api/v1/workflows/{workflowId}/execute | Execute workflow |
| GET | /api/v1/workflows/executions/{executionId} | Execution status |
| POST | /api/v1/workflows/executions/{executionId}/cancel | Cancel execution |
| GET | /api/v1/workflows/history | Workflow history |

---

# 6. List Workflows

## Endpoint

```http
GET /api/v1/workflows
```

### Response

```json
{
  "workflows": [
    {
      "workflowId": "knowledge-workflow",
      "name": "Knowledge Retrieval Workflow",
      "version": "1.0",
      "status": "ACTIVE"
    },
    {
      "workflowId": "contract-review-workflow",
      "name": "Contract Review Workflow",
      "version": "1.2",
      "status": "ACTIVE"
    }
  ]
}
```

---

# 7. Workflow Details

## Endpoint

```http
GET /api/v1/workflows/{workflowId}
```

### Response

```json
{
  "workflowId": "knowledge-workflow",
  "name": "Knowledge Retrieval Workflow",
  "description": "Retrieves enterprise knowledge using hybrid search.",
  "version": "1.0",
  "status": "ACTIVE",
  "owner": "AI Platform Team"
}
```

---

# 8. Execute Workflow

## Endpoint

```http
POST /api/v1/workflows/{workflowId}/execute
```

### Request

```json
{
  "sessionId": "session-123",
  "input": {
    "query": "Summarize the Enterprise Architecture documentation."
  }
}
```

### Response

```json
{
  "executionId": "WF-EXEC-1001",
  "status": "RUNNING",
  "startedAt": "2026-08-20T10:15:00Z"
}
```

Workflow execution is asynchronous for long-running processes.

---

# 9. Workflow Execution Status

## Endpoint

```http
GET /api/v1/workflows/executions/{executionId}
```

### Response

```json
{
  "executionId": "WF-EXEC-1001",
  "workflowId": "knowledge-workflow",
  "status": "RUNNING",
  "currentNode": "Knowledge Retrieval",
  "progress": 65,
  "startedAt": "2026-08-20T10:15:00Z"
}
```

---

# 10. Cancel Workflow

## Endpoint

```http
POST /api/v1/workflows/executions/{executionId}/cancel
```

### Response

```json
{
  "executionId": "WF-EXEC-1001",
  "status": "CANCELLED"
}
```

Only workflows in a cancellable state may be cancelled.

---

# 11. Workflow History

## Endpoint

```http
GET /api/v1/workflows/history
```

### Query Parameters

| Parameter | Description |
|-----------|-------------|
| page | Page number |
| size | Page size |
| workflowId | Filter by workflow |
| status | Filter by execution status |

### Response

```json
{
  "page": 1,
  "size": 20,
  "total": 85,
  "executions": [
    {
      "executionId": "WF-EXEC-1001",
      "workflowId": "knowledge-workflow",
      "status": "COMPLETED",
      "durationMs": 2843
    }
  ]
}
```

---

# 12. Workflow States

| State | Description |
|--------|-------------|
| CREATED | Execution created |
| RUNNING | Workflow executing |
| WAITING | Waiting for external event or approval |
| COMPLETED | Successfully completed |
| FAILED | Execution failed |
| CANCELLED | Cancelled by user |
| TIMED_OUT | Execution exceeded timeout |

---

# 13. Human Approval Support

Certain workflows may pause awaiting manual approval.

Example response:

```json
{
  "executionId": "WF-EXEC-1005",
  "status": "WAITING",
  "approvalRequired": true,
  "approvalStep": "Legal Review"
}
```

Examples include:

- Contract approval
- High-risk AI actions
- Administrative changes
- External system updates

---

# 14. Workflow State Model

```text
CREATED
    │
    ▼
RUNNING
 ├─────────────┐
 ▼             ▼
WAITING     COMPLETED
 │
 ▼
RUNNING
 │
 ├─────────────┐
 ▼             ▼
FAILED    CANCELLED
```

---

# 15. Authentication

All Workflow APIs require a valid JWT access token.

```http
Authorization: Bearer <access_token>
```

Workflow execution permissions should be controlled using role-based access control (RBAC).

---

# 16. HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 202 | Workflow accepted |
| 400 | Invalid request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Workflow not found |
| 409 | Workflow already running |
| 422 | Validation error |
| 429 | Rate limited |
| 500 | Internal server error |

---

# 17. Error Response

```json
{
  "success": false,
  "error": {
    "code": "WORKFLOW_EXECUTION_FAILED",
    "message": "Workflow execution failed due to an internal error."
  }
}
```

---

# 18. Security Considerations

Workflow APIs should:

- Require authentication.
- Enforce RBAC.
- Validate workflow inputs.
- Restrict execution of privileged workflows.
- Log workflow state transitions.
- Record tool invocations.
- Protect against unauthorized cancellation.

---

# 19. Performance Considerations

To optimize workflow execution:

- Execute independent nodes concurrently where possible.
- Persist workflow state for long-running executions.
- Cache reusable context.
- Monitor execution duration.
- Configure appropriate timeout values.
- Collect execution metrics for optimization.

---

# 20. Best Practices

- Design workflows to be idempotent where practical.
- Keep workflow definitions versioned.
- Persist execution state for recovery.
- Minimize unnecessary agent invocations.
- Record audit information for every execution.
- Monitor workflow success and failure rates.

---

# 21. Related Documents

- API-005 – Agent APIs
- API-007 – Tool Registry APIs
- WF-001 – Chat Workflow
- WF-002 – Agent Execution Workflow
- WF-003 – Workflow Orchestration
- AG-001 – Supervisor Agent
- AG-003 – Planner Agent

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | API-006 |
| Title | Workflow APIs |
| Category | API Documentation |
| Audience | Backend Developers, AI Engineers, Integration Engineers |
| Version | 1.0 |
| Status | Active |