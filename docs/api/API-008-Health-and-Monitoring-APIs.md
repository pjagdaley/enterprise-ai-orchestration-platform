# API-008 – Health and Monitoring APIs

## 1. Purpose

This document describes the Health and Monitoring APIs exposed by the Enterprise AI Orchestration Platform.

These APIs provide operational visibility into platform health, infrastructure dependencies, application metrics, and runtime diagnostics.

The APIs enable:

- Platform health monitoring
- Kubernetes/Cloud Run health checks
- Dependency validation
- Metrics collection
- Service diagnostics
- Version discovery
- Operational dashboards

These APIs are intended for operations teams, monitoring systems, and infrastructure components.

---

# 2. Scope

The Health and Monitoring APIs support:

- Liveness checks
- Readiness checks
- Platform health
- Dependency health
- Metrics
- Runtime diagnostics
- Version information

---

# 3. Monitoring Architecture

```text
                  Monitoring Systems
        (Prometheus, Grafana, Cloud Monitoring)
                        │
                        ▼
                Health Monitoring APIs
                        │
                        ▼
               Monitoring Service
                        │
     ┌───────────┬───────────┬────────────┐
     ▼           ▼           ▼            ▼
 Platform     Dependencies  Metrics   Diagnostics
     │
     ▼
FastAPI Application
     │
     ▼
 Gemini • Firestore • Qdrant • OpenSearch • GCS
```

---

# 4. Monitoring Workflow

```text
Monitoring System
        │
        ▼
Health API Request
        │
        ▼
Health Controller
        │
        ▼
Health Service
        │
        ▼
Check Dependencies
        │
        ▼
Aggregate Results
        │
        ▼
Return Health Status
```

---

# 5. API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /health | Overall platform health |
| GET | /health/live | Liveness probe |
| GET | /health/ready | Readiness probe |
| GET | /health/dependencies | Dependency health |
| GET | /metrics | Prometheus metrics |
| GET | /diagnostics | Runtime diagnostics |
| GET | /version | Platform version |

---

# 6. Platform Health

## Endpoint

```http
GET /health
```

### Description

Returns the overall health of the platform.

### Response

```json
{
  "status": "UP",
  "timestamp": "2026-08-30T10:15:42Z",
  "services": {
    "firestore": "UP",
    "qdrant": "UP",
    "opensearch": "UP",
    "gcs": "UP",
    "gemini": "UP"
  }
}
```

---

# 7. Liveness Probe

## Endpoint

```http
GET /health/live
```

### Description

Determines whether the application process is alive.

### Response

```json
{
  "status": "UP"
}
```

This endpoint should only verify that the application is running and should not check external dependencies.

---

# 8. Readiness Probe

## Endpoint

```http
GET /health/ready
```

### Description

Determines whether the application is ready to receive traffic.

### Response

```json
{
  "status": "READY"
}
```

Readiness checks should validate required dependencies before accepting requests.

---

# 9. Dependency Health

## Endpoint

```http
GET /health/dependencies
```

### Description

Returns the health of external platform dependencies.

### Response

```json
{
  "dependencies": [
    {
      "name": "Firestore",
      "status": "UP",
      "latencyMs": 42
    },
    {
      "name": "Qdrant",
      "status": "UP",
      "latencyMs": 27
    },
    {
      "name": "OpenSearch",
      "status": "UP",
      "latencyMs": 35
    },
    {
      "name": "Google Cloud Storage",
      "status": "UP",
      "latencyMs": 31
    },
    {
      "name": "Gemini API",
      "status": "UP",
      "latencyMs": 182
    }
  ]
}
```

---

# 10. Metrics Endpoint

## Endpoint

```http
GET /metrics
```

### Description

Exposes application metrics in Prometheus format.

### Example

```text
http_requests_total 14253
http_request_duration_seconds 0.153
chat_requests_total 5210
workflow_executions_total 610
agent_executions_total 931
tool_executions_total 1640
```

---

# 11. Runtime Diagnostics

## Endpoint

```http
GET /diagnostics
```

### Description

Returns runtime diagnostic information.

### Response

```json
{
  "uptimeSeconds": 86230,
  "memoryUsageMb": 512,
  "cpuUsagePercent": 18,
  "activeSessions": 42,
  "activeWorkflows": 6
}
```

---

# 12. Version Information

## Endpoint

```http
GET /version
```

### Response

```json
{
  "application": "Enterprise AI Orchestration Platform",
  "version": "1.0.0",
  "build": "20260830.1",
  "commit": "9f43a1d",
  "environment": "production"
}
```

---

# 13. Health Status Values

| Status | Description |
|---------|-------------|
| UP | Service operating normally |
| READY | Ready to receive traffic |
| DEGRADED | Functional with reduced capability |
| DOWN | Unavailable |
| UNKNOWN | Health cannot be determined |

---

# 14. Authentication

| Endpoint | Authentication |
|----------|----------------|
| /health/live | Not Required |
| /health/ready | Not Required |
| /health | Required |
| /health/dependencies | Required |
| /metrics | Restricted |
| /diagnostics | Administrator Only |
| /version | Required |

---

# 15. HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

---

# 16. Error Response

```json
{
  "success": false,
  "error": {
    "code": "DEPENDENCY_UNAVAILABLE",
    "message": "One or more required services are unavailable."
  }
}
```

---

# 17. Security Considerations

Health APIs should:

- Expose only minimal information publicly.
- Restrict diagnostics to administrators.
- Protect metrics endpoints from unauthorized access.
- Avoid exposing sensitive configuration.
- Log health check failures.
- Apply rate limiting where appropriate.

---

# 18. Performance Considerations

To optimize monitoring:

- Keep liveness checks lightweight.
- Cache expensive dependency checks.
- Avoid blocking application threads.
- Execute dependency checks in parallel.
- Publish metrics asynchronously.
- Minimize response payload sizes.

---

# 19. Best Practices

- Separate liveness and readiness logic.
- Continuously monitor dependency latency.
- Export Prometheus-compatible metrics.
- Record service uptime.
- Alert on degraded dependencies.
- Include build metadata for traceability.
- Monitor health trends over time.

---

# 20. Related Documents

- OPS-002 – Monitoring and Alerting
- OPS-004 – Incident Management
- SERVICE-001 – Gemini Service
- SERVICE-003 – Qdrant Service
- SERVICE-004 – Firestore Service
- SERVICE-005 – OpenSearch Service
- SERVICE-006 – Google Cloud Storage Service

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | API-008 |
| Title | Health and Monitoring APIs |
| Category | API Documentation |
| Audience | DevOps Engineers, Platform Engineers, SREs |
| Version | 1.0 |
| Status | Active |