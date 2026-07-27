# SEC-004 – Secrets and Key Management

## 1. Purpose

This document defines the strategy for securely managing secrets, credentials, encryption keys, certificates, and API tokens throughout the Enterprise AI Orchestration Platform.

Secrets are among the most sensitive assets in the platform. Their compromise can lead to unauthorized access to cloud resources, AI services, enterprise knowledge repositories, and customer data.

The platform adopts centralized secrets management with strict access controls, automated rotation, auditing, and lifecycle management.

---

# 2. Objectives

The secrets management strategy aims to:

- Protect sensitive credentials
- Eliminate hard-coded secrets
- Centralize secret storage
- Support automated key rotation
- Reduce credential exposure
- Protect cloud resources
- Secure AI integrations
- Enable auditing
- Support regulatory compliance
- Simplify secret lifecycle management

---

# 3. Scope

This document applies to:

- API Keys
- OAuth Client Secrets
- JWT Signing Keys
- Encryption Keys
- Database Credentials
- Service Account Credentials
- TLS Certificates
- MCP Authentication Tokens
- CI/CD Secrets
- Third-Party Integration Credentials

---

# 4. Secrets Architecture

```text
                 Developers
                      │
                      ▼
              Google Secret Manager
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    Cloud Run      FastAPI      LangGraph
        │             │             │
        └─────────────┼─────────────┘
                      ▼
               AI Agents & Tools
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
   Gemini        Firestore        External APIs
   Vertex AI     GCS              MCP Servers
```

Secrets should never be stored in application source code.

---

# 5. Secret Categories

| Category | Examples |
|----------|----------|
| Cloud Credentials | Service Accounts |
| API Keys | Gemini API |
| OAuth Secrets | Client Secret |
| Database Credentials | Database Password |
| Encryption Keys | CMEK Keys |
| JWT Keys | Signing Keys |
| TLS Certificates | HTTPS Certificates |
| Third-Party Tokens | External APIs |

Each category should have dedicated access controls and rotation policies.

---

# 6. Secret Storage

All production secrets should be stored in a centralized secrets management solution.

Recommended implementation:

- Google Secret Manager
- Cloud KMS (for encryption keys)
- Enterprise HSM where required

Secrets must not be stored in:

- Source code
- Git repositories
- Docker images
- Configuration files
- Build artifacts
- Documentation

---

# 7. Environment Configuration

Applications should retrieve secrets at runtime.

Example:

```text
Cloud Run
      │
      ▼
Secret Manager
      │
      ▼
FastAPI Configuration
      │
      ▼
Application Services
```

Environment variables should reference secrets rather than embedding sensitive values.

---

# 8. Secret Access Control

Access to secrets should follow the principle of least privilege.

Access should be granted only to:

- Authorized applications
- Approved service accounts
- Platform administrators (where required)

Direct human access to production secrets should be minimized.

---

# 9. Service Account Management

Each workload should use a dedicated service account.

Examples:

| Component | Service Account |
|----------|-----------------|
| FastAPI | platform-api-sa |
| Ingestion Service | ingestion-sa |
| AI Workflow Engine | workflow-sa |
| Background Jobs | jobs-sa |
| CI/CD Pipeline | deployment-sa |

Service accounts should not be shared across unrelated workloads.

---

# 10. Key Rotation

Secrets should be rotated regularly.

Recommended events include:

- Scheduled rotation
- Personnel changes
- Credential compromise
- Infrastructure migration
- Compliance requirements

Applications should support secret rotation without requiring source code changes.

---

# 11. Encryption Key Management

Encryption keys should be:

- Centrally managed
- Versioned
- Rotated
- Access controlled
- Audited

Key types include:

- Customer-Managed Encryption Keys (CMEK)
- Cloud KMS Keys
- JWT Signing Keys
- TLS Private Keys

---

# 12. JWT Signing Keys

JWT signing keys should:

- Be stored securely
- Support key versioning
- Support key rotation
- Never be embedded in source code
- Be protected by strict IAM policies

Applications should validate tokens using trusted public keys or identity provider metadata.

---

# 13. Certificate Management

TLS certificates should be:

- Issued by trusted Certificate Authorities
- Renewed before expiration
- Automatically deployed where possible
- Monitored for expiration

Expired certificates should trigger operational alerts.

---

# 14. CI/CD Secrets

Build pipelines may require secrets for:

- Container Registry
- Cloud Deployment
- Artifact Storage
- Infrastructure Provisioning

CI/CD secrets should:

- Be centrally managed
- Be injected during pipeline execution
- Never be stored in pipeline definitions
- Be rotated regularly

---

# 15. AI Integration Secrets

AI services may require:

- Gemini API credentials
- Vertex AI authentication
- MCP server credentials
- External model provider tokens

AI credentials should be isolated from application credentials and granted only the permissions necessary for AI operations.

---

# 16. Secret Lifecycle

```text
Generate Secret
       │
       ▼
Store Securely
       │
       ▼
Grant Access
       │
       ▼
Monitor Usage
       │
       ▼
Rotate
       │
       ▼
Revoke
       │
       ▼
Destroy
```

Every stage of the lifecycle should be auditable.

---

# 17. Monitoring and Auditing

Monitor events including:

- Secret creation
- Secret access
- Secret updates
- Secret rotation
- Failed access attempts
- Secret deletion

Audit records should include:

- Identity
- Timestamp
- Secret identifier
- Operation
- Outcome

Secret values must never appear in audit logs.

---

# 18. Incident Response

If a secret is suspected to be compromised:

1. Revoke the secret immediately.
2. Generate a replacement.
3. Update dependent services.
4. Rotate related credentials.
5. Investigate audit logs.
6. Assess potential impact.
7. Document the incident.

Recovery procedures should be regularly exercised.

---

# 19. Best Practices

- Never hard-code secrets.
- Use a centralized secrets manager.
- Apply least privilege.
- Rotate secrets automatically where possible.
- Separate environments (development, test, production).
- Use dedicated service accounts.
- Protect encryption keys with Cloud KMS.
- Monitor all secret access.
- Remove unused secrets promptly.

---

# 20. Related Documents

- README – Security Documentation
- SEC-001 – Authentication and Authorization
- SEC-002 – Identity and Access Management
- SEC-003 – Data Protection and Encryption
- SEC-005 – API Security
- Operations Documentation
- Deployment Documentation

---

# Metadata

| Property | Value |
|----------|-------|
| Document ID | SEC-004 |
| Title | Secrets and Key Management |
| Category | Security Documentation |
| Audience | Security Engineers, DevOps Engineers, Developers, Platform Administrators |
| Version | 1.0 |
| Status | Active |