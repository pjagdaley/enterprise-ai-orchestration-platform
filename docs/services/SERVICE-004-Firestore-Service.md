# SERVICE-004 – Firestore Service

## 1. Purpose

The Firestore Service provides centralized access to Google Cloud Firestore for persistent storage and retrieval of application metadata.

Within the Enterprise AI Orchestration Platform, the service manages conversation history, document metadata, ingestion status, and other operational information required by the platform.

The Firestore Service abstracts all interactions with Firestore and provides a consistent persistence interface for the application.

---

## 2. Responsibilities

The Firestore Service is responsible for:

- Managing Firestore client initialization.
- Retrieving conversation history.
- Managing document metadata.
- Maintaining document registry information.
- Supporting session-based chat history.
- Executing CRUD operations.
- Managing timestamps.
- Handling retry logic.
- Monitoring database availability.

The Firestore Service does not perform vector search or document storage.

---

## 3. Position within the Architecture

```text
                Enterprise RAG Tool
                        │
                        ▼
               Firestore Service
                        │
                        ▼
             Google Cloud Firestore
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
 Conversation History         Document Registry
```

---

## 4. Business Responsibilities

The Firestore Service enables:

- Conversation persistence.
- Context-aware chat.
- Session management.
- Document registry.
- Metadata storage.
- Audit information.
- Operational state tracking.

Typical use cases include:

- Retrieve previous conversation.
- Store document metadata.
- Update ingestion status.
- Retrieve document information.
- Maintain processing history.

---

## 5. Public Interface

| Operation | Description |
|-----------|-------------|
| get_chat_history() | Retrieve conversation |
| format_chat_history() | Build LLM context |
| get_document() | Retrieve document metadata |
| save_document() | Save registry information |
| update_document() | Update metadata |
| delete_document() | Delete registry entry |
| health() | Verify service availability |

---

## 6. Configuration

| Property | Description |
|----------|-------------|
| Project ID | GCP project |
| Database | Firestore database |
| Credentials | Service account |
| Timeout | Request timeout |

Example:

```text
PROJECT_ID=enterprise-ai-platform
FIRESTORE_DATABASE=(default)
GOOGLE_APPLICATION_CREDENTIALS=config/firebase-reader.json
```

---

## 7. Firestore Collections

### Chat History

```text
chat_sessions
    └── session_id
            └── messages
```

Each message contains:

- role
- content
- createdAt
- userId
- sessionId

---

### Document Registry

```text
documents
    └── document_id
```

Each document stores:

- document_id
- filename
- source_path
- extension
- chunk_count
- status
- created_at
- updated_at
- last_error

---

## 8. Processing Flow

### Chat Context Retrieval

```text
Receive Session ID
        │
        ▼
Query Firestore
        │
        ▼
Sort by Timestamp
        │
        ▼
Keep Last N Messages
        │
        ▼
Format Conversation
        │
        ▼
Return Context
```

### Document Metadata

```text
Receive Document ID
        │
        ▼
Retrieve Metadata
        │
        ▼
Return Document
```

---

## 9. Interaction with Other Components

| Component | Interaction |
|-----------|-------------|
| Enterprise RAG Tool | Retrieves chat context |
| Ingestion Service | Stores document registry |
| Document Service | Updates metadata |
| Gemini Service | Consumes formatted context |

---

## 10. Chat Context Management

Conversation history is retrieved using:

- User ID
- Session ID

Messages are:

- Ordered chronologically.
- Limited to the configured history size.
- Formatted into conversational context.
- Included in the LLM prompt.

Example:

```text
User:
What is Kubernetes?

Assistant:
Kubernetes is...

User:
How does autoscaling work?
```

---

## 11. Document Registry Schema

Each registry record contains:

| Field | Description |
|--------|-------------|
| document_id | Unique identifier |
| filename | Original filename |
| source_path | GCS source |
| extension | File extension |
| chunk_count | Number of generated chunks |
| status | Processing status |
| created_at | Creation timestamp |
| updated_at | Last modification |
| last_error | Processing error |

---

## 12. Error Handling

| Failure | Behaviour |
|----------|-----------|
| Authentication failure | Return service error |
| Document missing | Return not found |
| Session missing | Return empty conversation |
| Timeout | Retry |
| Firestore unavailable | Return service unavailable |

---

## 13. Security Considerations

The Firestore Service:

- Uses Google Cloud IAM authentication.
- Restricts collection access.
- Validates document identifiers.
- Logs database failures.
- Prevents unauthorized updates.

---

## 14. Performance Considerations

- Reuse Firestore client.
- Retrieve only required documents.
- Limit chat history.
- Minimize read operations.
- Use indexed fields.
- Cache frequently accessed metadata where appropriate.

---

## 15. Technology Stack

| Technology | Purpose |
|------------|---------|
| Google Cloud Firestore | NoSQL database |
| firebase-admin | Firestore client |
| Python | Service implementation |
| FastAPI | Application framework |

---

## 16. Monitoring & Observability

The Firestore Service records:

- Read operations
- Write operations
- Failed operations
- Average response time
- Retry count
- Active sessions

Logs include:

- Session ID
- Document ID
- Request duration
- Error details

---

## 17. Future Enhancements

Future improvements may include:

- Conversation summarization.
- Long-term memory.
- Metadata versioning.
- Multi-tenant support.
- Soft deletes.
- Automatic cleanup.
- Session archival.

---

## 18. Sequence Diagram

```text
Enterprise RAG Tool
        │
        ▼
Firestore Service
        │
        ▼
Cloud Firestore
        │
        ▼
Conversation History
        │
        ▼
Enterprise RAG Tool
```

---

## 19. Design Principles

The Firestore Service follows these principles:

- Stateless service layer.
- Centralized persistence.
- Configuration-driven behavior.
- Secure authentication.
- Efficient data access.
- Consistent data model.

---

## 20. Success Criteria

The Firestore Service is considered successful when:

- Conversation history is retrieved correctly.
- Document metadata is stored accurately.
- Registry updates complete successfully.
- Configured chat history limits are respected.
- Service meets configured availability and latency objectives.

---

## Metadata

| Property | Value |
|----------|-------|
| Service ID | SERVICE-004 |
| Service Name | Firestore Service |
| Type | Infrastructure Service |
| Category | NoSQL Database |
| Provider | Google Cloud Firestore |
| Owner | Enterprise AI Orchestration Platform |
| Version | 1.0 |
| Status | Implemented |