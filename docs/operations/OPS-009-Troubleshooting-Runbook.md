# OPS-009 – Troubleshooting Runbook

## 1. Purpose

This runbook provides standardized troubleshooting procedures for diagnosing and resolving operational issues within the Enterprise AI Orchestration Platform.

Its objectives are to:

- Reduce Mean Time to Recovery (MTTR)
- Provide repeatable diagnostic procedures
- Standardize operational responses
- Minimize service disruption
- Assist on-call engineers during incidents

This runbook complements the Incident Management process by focusing on technical diagnosis and resolution.

---

# 2. Troubleshooting Workflow

```text
Problem Reported
        │
        ▼
Verify Symptoms
        │
        ▼
Identify Affected Component
        │
        ▼
Collect Logs & Metrics
        │
        ▼
Identify Root Cause
        │
        ▼
Apply Resolution
        │
        ▼
Verify Recovery
        │
        ▼
Update Incident Record
```

---

# 3. Initial Assessment Checklist

Before troubleshooting:

- Identify affected users.
- Determine impacted services.
- Check monitoring dashboards.
- Review recent deployments.
- Review recent configuration changes.
- Verify cloud service status.
- Check active alerts.

---

# 4. API Service Issues

## Symptoms

- API unavailable
- HTTP 5xx responses
- Increased latency
- Timeout errors

### Diagnostics

- Verify Cloud Run service status.
- Check container logs.
- Review CPU and memory utilization.
- Verify health endpoint.
- Review deployment history.

### Resolution

- Restart affected revision if necessary.
- Roll back recent deployment.
- Increase resource allocation if required.
- Investigate dependency failures.

---

# 5. Authentication Issues

## Symptoms

- Login failures
- Unauthorized responses
- Token validation failures

### Diagnostics

- Verify OAuth provider availability.
- Check token expiration.
- Review IAM permissions.
- Validate service account configuration.

### Resolution

- Refresh credentials.
- Restore IAM permissions.
- Rotate compromised credentials.
- Redeploy updated configuration.

---

# 6. Vertex AI Issues

## Symptoms

- AI response failures
- Long response times
- Quota exceeded
- Model unavailable

### Diagnostics

- Verify Vertex AI service status.
- Review API error codes.
- Check quota usage.
- Verify model configuration.

### Resolution

- Retry transient failures.
- Reduce prompt size.
- Increase quotas if appropriate.
- Switch to approved fallback model if configured.

---

# 7. Embedding Service Issues

## Symptoms

- Embeddings not generated
- Ingestion failures
- Search failures

### Diagnostics

- Review embedding service logs.
- Validate embedding model configuration.
- Verify API connectivity.
- Check document parsing.

### Resolution

- Retry failed requests.
- Correct configuration.
- Reprocess failed documents.
- Verify supported document formats.

---

# 8. Qdrant Issues

## Symptoms

- No semantic search results
- Slow searches
- Collection unavailable
- Connection failures

### Diagnostics

- Verify Qdrant service health.
- Check collection existence.
- Review vector counts.
- Validate metadata filters.
- Review search latency.

### Resolution

- Restart Qdrant if required.
- Restore snapshot.
- Rebuild affected collection.
- Reingest missing documents.

---

# 9. OpenSearch Issues

## Symptoms

- Keyword search unavailable
- Slow search responses
- Missing indexes

### Diagnostics

- Verify cluster health.
- Review shard allocation.
- Check index status.
- Review query latency.

### Resolution

- Restore index.
- Rebuild affected indexes.
- Optimize cluster.
- Remove corrupted indexes.

---

# 10. Firestore Issues

## Symptoms

- Context retrieval failures
- Registry errors
- Slow queries

### Diagnostics

- Verify Firestore availability.
- Review indexes.
- Check permissions.
- Validate query performance.

### Resolution

- Restore permissions.
- Create missing indexes.
- Retry failed operations.
- Optimize queries.

---

# 11. Google Cloud Storage Issues

## Symptoms

- Upload failures
- Missing documents
- Permission errors

### Diagnostics

- Verify bucket availability.
- Check IAM permissions.
- Validate object paths.
- Review lifecycle rules.

### Resolution

- Restore permissions.
- Correct bucket configuration.
- Restore deleted objects if available.
- Retry uploads.

---

# 12. Document Ingestion Issues

## Symptoms

- Documents not indexed
- Parsing failures
- Missing embeddings

### Diagnostics

- Verify parser output.
- Check chunk generation.
- Review embedding logs.
- Validate ingestion pipeline.

### Resolution

- Correct parsing errors.
- Reprocess documents.
- Retry embedding generation.
- Verify registry status.

---

# 13. Hybrid Search Issues

## Symptoms

- Poor search quality
- Missing relevant documents
- Duplicate results

### Diagnostics

- Review semantic search results.
- Review BM25 search results.
- Validate metadata filters.
- Review reranking scores.

### Resolution

- Tune retrieval parameters.
- Rebuild indexes.
- Update metadata.
- Review reranking configuration.

---

# 14. LangGraph Workflow Issues

## Symptoms

- Agent workflow fails
- Graph execution stops
- Tool execution errors

### Diagnostics

- Review workflow logs.
- Identify failing node.
- Validate state transitions.
- Review tool responses.

### Resolution

- Restart workflow.
- Correct tool configuration.
- Update graph definition.
- Validate workflow state.

---

# 15. MCP Integration Issues

## Symptoms

- MCP server unavailable
- Tool execution timeout
- Invalid responses

### Diagnostics

- Verify MCP server connectivity.
- Review authentication.
- Check request timeout.
- Review server logs.

### Resolution

- Restart MCP service.
- Correct credentials.
- Increase timeout if appropriate.
- Validate tool registration.

---

# 16. Performance Issues

## Symptoms

- Slow responses
- High latency
- High CPU usage
- Memory pressure

### Diagnostics

- Review monitoring dashboards.
- Check Cloud Run metrics.
- Review search latency.
- Analyze AI response times.

### Resolution

- Scale infrastructure.
- Optimize queries.
- Reduce prompt size.
- Tune retrieval settings.

---

# 17. High Error Rate

Possible causes:

- External dependency failure
- Authentication problems
- Resource exhaustion
- Recent deployment

Recommended actions:

- Review logs.
- Roll back deployment if necessary.
- Verify infrastructure health.
- Escalate if unresolved.

---

# 18. Escalation Matrix

| Issue | Primary Team | Secondary Team |
|--------|--------------|----------------|
| API | Platform | DevOps |
| Vertex AI | AI Platform | Cloud Operations |
| Firestore | Platform | Cloud Operations |
| Qdrant | Search Platform | DevOps |
| OpenSearch | Search Platform | DevOps |
| Authentication | Security | Platform |
| Infrastructure | DevOps | Cloud Operations |

---

# 19. Best Practices

- Verify symptoms before applying fixes.
- Collect evidence before restarting services.
- Make one change at a time.
- Validate recovery after each action.
- Document all troubleshooting steps.
- Update the knowledge base after resolution.

---

# 20. Related Documents

- OPS-002 – Monitoring and Alerting
- OPS-004 – Incident Management
- OPS-005 – Disaster Recovery
- OPS-008 – Maintenance Runbook
- Security Architecture
- Deployment Architecture

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | OPS-009 |
| Title | Troubleshooting Runbook |
| Category | Operations Documentation |
| Audience | Operations Engineers, DevOps Engineers, SREs, Support Engineers |
| Version | 1.0 |
| Status | Active |