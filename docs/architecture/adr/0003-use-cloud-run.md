# ADR-0003: Adopt Google Cloud Run for Stateless Application Services

## Status

**Accepted**

---

## Date

2025-07-13

---

## Decision Makers

- Enterprise Architect
- Solution Architect
- Technical Lead

---

# Context

The Enterprise AI Orchestration Platform consists of several stateless application services including:

- FastAPI Backend
- Document Ingestion Service
- Query Service
- Agent Orchestration Service
- Administration APIs
- REST APIs

These services require a deployment platform capable of:

- Automatic scaling
- High availability
- Container-based deployment
- Secure integration with Google Cloud services
- Minimal operational overhead
- Cost-efficient execution
- Cloud-native architecture

The platform also includes stateful components such as Qdrant, which require persistent storage and therefore cannot be deployed on Cloud Run.

---

# Decision

Google Cloud Run has been selected as the primary compute platform for all stateless application services.

The following services will be deployed on Cloud Run:

- FastAPI Backend
- AI Query Service
- Document Ingestion Service
- Administration APIs
- Health Check APIs

Stateful services such as Qdrant will remain on Google Compute Engine.

---

# Decision Drivers

The following factors influenced the decision:

- Fully managed serverless platform
- Automatic horizontal scaling
- Scale-to-zero capability
- Native container support
- Simple deployment model
- Integrated Cloud IAM
- Integrated Cloud Logging
- Integrated Cloud Monitoring
- Direct integration with Vertex AI
- Cost optimization for variable workloads

---

# Alternatives Considered

## Google Kubernetes Engine (GKE)

### Advantages

- Full Kubernetes flexibility
- Advanced networking
- Fine-grained resource control
- Supports both stateless and stateful workloads

### Disadvantages

- Higher operational complexity
- Cluster management overhead
- More expensive for small and medium workloads
- Requires Kubernetes expertise

---

## Google Compute Engine

### Advantages

- Complete infrastructure control
- Supports any workload
- Flexible operating system configuration

### Disadvantages

- Manual scaling
- Manual patching
- Higher operational effort
- Infrastructure maintenance responsibility

---

## App Engine

### Advantages

- Fully managed deployment
- Simple developer experience

### Disadvantages

- Less flexibility
- Limited container customization
- Less suitable for modern AI workloads

---

# Consequences

## Positive

- Automatic scaling
- Pay-per-use pricing
- Managed infrastructure
- Fast deployments
- Built-in HTTPS
- Integrated monitoring
- Simplified DevOps
- Reduced operational cost

---

## Negative

- Stateless execution only
- Cold starts after inactivity
- Maximum request duration limits
- Persistent storage not supported

---

# Architecture Impact

This decision affects:

- Solution Architecture
- Deployment Architecture
- Operations Architecture
- Network Architecture
- Security Architecture

---

# Risks

| Risk | Mitigation |
|------|------------|
| Cold start latency | Configure minimum instances for production |
| Long-running tasks | Use Cloud Run Jobs or background workers |
| Stateful workloads | Deploy on Compute Engine |
| Vendor dependency | Containerized architecture enables future portability |

---

# Implementation Notes

Cloud Run will host:

- FastAPI Backend
- AI Query Service
- Agent Runtime
- Administration APIs

Cloud Run integrates with:

- Vertex AI
- Firestore
- Google Cloud Storage
- Secret Manager
- Cloud IAM
- Cloud Logging
- Cloud Monitoring

Cloud Run connects to the private Qdrant VM using **Direct VPC Egress**.

---

# Architecture Principles Supported

This decision aligns with the following architecture principles:

- Cloud Native
- Serverless First
- Scalability by Design
- Operational Simplicity
- Security by Design
- Cost Optimization
- High Availability

---

# Related Architecture Documents

- ARCHITECTURE.md
- 09 Technology Architecture.md
- 10 Deployment Architecture.md
- 11 Security Architecture.md

---

# Related Diagrams

- GCP Production Deployment Architecture
- Cloud Run Runtime Architecture
- VPC Topology
- Private Connectivity
- Operations Architecture

---

# References

- Google Cloud Run Documentation
- Google Cloud Architecture Framework
- Cloud Run Best Practices
- Google Cloud Well-Architected Framework