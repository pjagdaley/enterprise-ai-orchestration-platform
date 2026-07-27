# OPS-001 – Production Deployment

## 1. Purpose

This document describes the production deployment architecture and operational procedures for the Enterprise AI Orchestration Platform.

It provides guidance for deploying, configuring, validating, and operating the platform in a production environment on Google Cloud Platform (GCP).

The deployment architecture is designed to achieve:

- High Availability
- Scalability
- Reliability
- Security
- Maintainability
- Observability

---

# 2. Scope

This document covers:

- Production infrastructure
- Cloud services
- Container deployment
- Configuration management
- Secrets management
- Network architecture
- Deployment workflow
- Validation
- Rollback
- Production readiness

---

# 3. Production Architecture

```text
                        Internet
                            │
                            ▼
                    HTTPS Load Balancer
                            │
                            ▼
                     Cloud Run Service
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
        ▼                   ▼                    ▼
   LangGraph Engine     Tool Registry      Monitoring
        │
        ▼
   AI Agent Framework
        │
        ▼
  Infrastructure Services
        │
 ┌──────┼──────────────┬──────────────┬───────────────┐
 ▼      ▼              ▼              ▼               ▼
Gemini Firestore    Qdrant      OpenSearch      Cloud Storage
Vertex AI
```

---

# 4. Infrastructure Components

| Component | Purpose |
|-----------|---------|
| Cloud Run | Hosts the FastAPI application |
| Artifact Registry | Stores Docker images |
| Vertex AI | Embedding and LLM services |
| Firestore | Metadata and chat history |
| Qdrant | Semantic vector search |
| OpenSearch | Keyword/BM25 search |
| Cloud Storage | Document repository |
| Secret Manager | Secure secrets storage |
| Cloud Logging | Centralized logging |
| Cloud Monitoring | Metrics and alerting |

---

# 5. Deployment Topology

```text
Production

Cloud Run
    │
    ├── FastAPI
    ├── LangGraph
    ├── Agents
    ├── Tool Registry
    └── Workflow Engine

Shared Services

Vertex AI
Firestore
Cloud Storage
Qdrant Cluster
OpenSearch Cluster
```

Application services remain stateless, while data services are externalized.

---

# 6. Networking

Production traffic flows as follows:

```text
Client
   │
HTTPS
   │
Load Balancer
   │
Cloud Run
   │
Private Service Calls
   │
Google Cloud Services
```

All external communication should use HTTPS.

---

# 7. Identity and Access Management

The platform follows the principle of least privilege.

Recommended service accounts:

| Service Account | Responsibility |
|-----------------|----------------|
| API Service | Invoke Vertex AI, Firestore, GCS |
| Ingestion Service | Read documents and index content |
| CI/CD Pipeline | Deploy Cloud Run services |
| Operations | Monitoring and maintenance |

Permissions should be scoped to the minimum required resources.

---

# 8. Secrets Management

Sensitive information must never be stored in source code.

Use Secret Manager for:

- API keys
- Service account credentials
- Database passwords
- OAuth client secrets
- Encryption keys

Secrets should be injected at deployment time.

---

# 9. Configuration Management

Runtime configuration is supplied through environment variables.

Examples:

```text
PROJECT_ID
LOCATION
GEMINI_MODEL
EMBEDDING_MODEL
QDRANT_HOST
QDRANT_PORT
QDRANT_COLLECTION
OPENSEARCH_HOST
GCS_BUCKET
FIRESTORE_DATABASE
LOG_LEVEL
```

Configuration should be environment-specific.

---

# 10. Container Deployment

Application packaging uses Docker.

Deployment flow:

```text
Source Code
     │
     ▼
Docker Build
     │
     ▼
Artifact Registry
     │
     ▼
Cloud Run
```

Container images should be immutable and versioned.

---

# 11. Deployment Pipeline

```text
Developer Commit
        │
        ▼
Git Repository
        │
        ▼
CI Pipeline
        │
        ▼
Unit Tests
        │
        ▼
Integration Tests
        │
        ▼
Docker Build
        │
        ▼
Artifact Registry
        │
        ▼
Production Deployment
```

Deployments should be automated and repeatable.

---

# 12. Autoscaling

Cloud Run automatically scales based on incoming requests.

Scaling considerations:

- Maximum instances
- Minimum instances
- Request concurrency
- CPU allocation
- Memory allocation
- Request timeout

Capacity planning should be reviewed periodically.

---

# 13. Health Checks

Health endpoints should verify:

- API availability
- Firestore connectivity
- Vertex AI connectivity
- Qdrant availability
- OpenSearch availability
- Cloud Storage access

Deployment is considered successful only after all health checks pass.

---

# 14. Logging

All services should emit structured logs.

Log categories include:

- Application logs
- Access logs
- Security logs
- Audit logs
- Error logs

Logs should include correlation identifiers for request tracing.

---

# 15. Monitoring

Monitor:

- Request rate
- Error rate
- Response latency
- CPU utilization
- Memory utilization
- Container restarts
- Vertex AI latency
- Search latency
- Storage usage

Critical metrics should generate alerts.

---

# 16. Deployment Validation

After deployment verify:

- API is reachable.
- Authentication works.
- Documents can be uploaded.
- Ingestion completes successfully.
- Hybrid search returns results.
- AI responses are generated.
- Monitoring dashboards show healthy services.

---

# 17. Rollback Strategy

If a deployment introduces critical issues:

1. Stop traffic to the new revision.
2. Route traffic to the previous stable revision.
3. Investigate the failure.
4. Apply corrective changes.
5. Redeploy after validation.

Rollback procedures should be documented and rehearsed.

---

# 18. Production Readiness Checklist

Before production release:

- Infrastructure provisioned
- Secrets configured
- IAM permissions verified
- Monitoring enabled
- Logging enabled
- Health checks validated
- Backup strategy implemented
- Disaster recovery reviewed
- Security assessment completed
- Documentation updated

---

# 19. Best Practices

- Keep application services stateless.
- Use immutable container images.
- Version every deployment.
- Automate deployments.
- Avoid manual production changes.
- Monitor continuously.
- Validate every release.
- Perform regular recovery drills.

---

# 20. Related Documents

- Deployment Architecture
- Security Architecture
- DEV-008 – Build and Deployment
- OPS-002 – Monitoring and Alerting
- OPS-003 – Backup and Recovery
- OPS-005 – Disaster Recovery

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | OPS-001 |
| Title | Production Deployment |
| Category | Operations Documentation |
| Audience | DevOps Engineers, Platform Engineers, SREs |
| Version | 1.0 |
| Status | Active |