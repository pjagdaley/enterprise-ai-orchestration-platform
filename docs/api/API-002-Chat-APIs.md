# API-002 – Chat APIs

## 1. Purpose

This document describes the Chat APIs provided by the Enterprise AI Orchestration Platform.

The Chat APIs enable client applications to:

- Submit natural language requests
- Receive AI-generated responses
- Execute agent workflows
- Retrieve contextual information
- Maintain conversation history
- Stream responses
- Support Retrieval-Augmented Generation (RAG)

The Chat API is the primary interface between users and the AI platform.

---

# 2. Scope

The Chat APIs support:

- Conversational AI
- Multi-turn conversations
- Session management
- Context-aware responses
- Streaming responses
- Conversation history
- Agent orchestration
- Hybrid retrieval

---

# 3. Chat Architecture

```text
                Client Application
                        │
                        ▼
                 POST /api/v1/chat
                        │
                        ▼
                 Chat Controller
                        │
                        ▼
                  Chat Service
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Conversation      WorkflowGraph      Search Service
    History              │                 │
        │                ▼                 ▼
    Firestore      Supervisor Agent   Qdrant/OpenSearch
                           │
                           ▼
                    Gemini Response
                           │
                           ▼
                       Client
```

---

# 4. Conversation Flow

```text
User
 │
 ▼
Submit Prompt
 │
 ▼
Authentication
 │
 ▼
Load Conversation Context
 │
 ▼
Hybrid Search
 │
 ▼
WorkflowGraph
 │
 ▼
Supervisor Agent
 │
 ▼
Tool Execution (Optional)
 │
 ▼
Gemini Response
 │
 ▼
Save Conversation
 │
 ▼
Return Response
```

---

# 5. API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/chat | Generate AI response |
| POST | /api/v1/chat/stream | Stream AI response |
| GET | /api/v1/chat/history/{sessionId} | Retrieve conversation history |
| DELETE | /api/v1/chat/history/{sessionId} | Delete conversation history |
| POST | /api/v1/chat/session | Create conversation session |

---

# 6. Generate Chat Response

## Endpoint

```http
POST /api/v1/chat
```

### Description

Processes a user prompt and returns an AI-generated response using the platform's orchestration workflow.

---

### Request

```json
{
  "sessionId": "session-123",
  "userId": "user-456",
  "query": "Explain Retrieval-Augmented Generation.",
  "stream": false
}
```

---

### Request Fields

| Field | Type | Required | Description |
|------|------|:--------:|-------------|
| sessionId | String | Yes | Conversation session identifier |
| userId | String | Yes | Authenticated user identifier |
| query | String | Yes | User prompt |
| stream | Boolean | No | Enable streaming response |

---

### Successful Response

HTTP 200

```json
{
  "success": true,
  "data": {
    "answer": "Retrieval-Augmented Generation (RAG) combines information retrieval with large language models...",
    "sessionId": "session-123",
    "citations": [
      {
        "documentId": "DOC-1001",
        "title": "RAG Architecture Guide"
      }
    ]
  }
}
```

---

# 7. Streaming Chat Response

## Endpoint

```http
POST /api/v1/chat/stream
```

### Description

Streams the AI response incrementally using Server-Sent Events (SSE).

---

### Request

```json
{
  "sessionId": "session-123",
  "query": "Summarize the uploaded architecture documents."
}
```

---

### Response

```text
data: Retrieval...
data: Searching...
data: Generating response...
data: Complete.
```

Streaming improves perceived responsiveness for longer AI responses.

---

# 8. Create Chat Session

## Endpoint

```http
POST /api/v1/chat/session
```

### Description

Creates a new conversation session.

---

### Response

```json
{
  "sessionId": "session-123",
  "createdAt": "2026-08-01T09:00:00Z"
}
```

---

# 9. Retrieve Conversation History

## Endpoint

```http
GET /api/v1/chat/history/{sessionId}
```

### Description

Returns the conversation history for a specified session.

---

### Response

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is RAG?"
    },
    {
      "role": "assistant",
      "content": "Retrieval-Augmented Generation..."
    }
  ]
}
```

Conversation history is retrieved from Firestore.

---

# 10. Delete Conversation History

## Endpoint

```http
DELETE /api/v1/chat/history/{sessionId}
```

### Description

Deletes all messages associated with the specified session.

---

### Response

HTTP 204

No response body.

---

# 11. Chat Processing Pipeline

```text
Receive Request
        │
        ▼
Authenticate User
        │
        ▼
Load Conversation Context
        │
        ▼
Hybrid Search
        │
        ▼
WorkflowGraph Execution
        │
        ▼
Supervisor Agent
        │
        ▼
Execute Tools (if required)
        │
        ▼
Generate Gemini Response
        │
        ▼
Persist Conversation
        │
        ▼
Return Response
```

---

# 12. Authentication

All Chat APIs require a valid JWT access token.

```http
Authorization: Bearer <access_token>
```

Unauthorized requests return HTTP 401.

---

# 13. HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Session Created |
| 204 | History Deleted |
| 400 | Invalid Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Session Not Found |
| 429 | Rate Limited |
| 500 | Internal Server Error |
| 503 | AI Service Unavailable |

---

# 14. Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "Conversation session does not exist."
  },
  "correlationId": "2bc6d24f-5d8d-4af2-9e6f-cc2a0f8b2d47"
}
```

---

# 15. Security Considerations

The Chat APIs should:

- Require authenticated users.
- Validate all request payloads.
- Enforce authorization for conversation access.
- Prevent prompt injection.
- Filter retrieved content based on user permissions.
- Log requests using correlation IDs.
- Apply rate limiting.

---

# 16. Performance Considerations

To optimize performance:

- Cache reusable conversation context.
- Limit retrieved history to the most recent messages.
- Optimize hybrid retrieval parameters.
- Stream long-running responses.
- Monitor AI response latency.
- Measure token usage.

---

# 17. Best Practices

- Keep prompts focused.
- Reuse conversation sessions.
- Enable streaming for long responses.
- Limit retained conversation history where appropriate.
- Monitor retrieval quality.
- Validate citations before presenting results.

---

# 18. Related Documents

- API-001 – Authentication APIs
- API-004 – Search APIs
- AG-001 – Supervisor Agent
- WF-001 – Chat Workflow
- SERVICE-001 – Gemini Service
- SERVICE-003 – Qdrant Service
- SERVICE-004 – Firestore Service

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | API-002 |
| Title | Chat APIs |
| Category | API Documentation |
| Audience | Frontend Developers, Backend Developers, Integration Engineers |
| Version | 1.0 |
| Status | Active |