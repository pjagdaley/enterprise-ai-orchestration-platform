# WF-009 – Structured Data Query

## 1. Purpose

The Structured Data Query workflow enables users to retrieve and analyze information stored in relational databases using natural language.

The platform translates business questions into structured database queries, executes them securely, and generates business-friendly responses using AI.

This workflow allows business users and technical teams to access enterprise data without writing SQL.

---

## 2. Business Scenario

Enterprise information is often stored in relational databases such as:

- PostgreSQL
- MySQL
- Oracle Database
- Microsoft SQL Server

Instead of manually writing SQL, users can ask questions such as:

- How many active customers do we have?
- Show the top 10 products by revenue.
- List all open incidents assigned to Team A.
- What were yesterday's sales?

The platform retrieves the required information and presents it in natural language.

---

## 3. Trigger

A user submits a natural language query that requires structured data.

### Example

```text
Show the top 10 customers by revenue this month.
```

---

## 4. Preconditions

The following conditions must be satisfied:

- User is authenticated.
- Database connection is available.
- Required schemas are accessible.
- Database Agent is registered.
- Tool Registry is initialized.
- User has permission to access the requested data.

---

## 5. Actors

### Primary Actor

- Business User
- Data Analyst
- Enterprise Architect

### System Components

- Chat API
- Chat Service
- WorkflowGraph
- Supervisor Agent
- Database Agent
- SQL Generator
- Database Service
- Gemini LLM

---

## 6. Workflow Overview

```text
+----------------------+
|        User          |
+----------+-----------+
           |
           v
+----------------------+
|      Chat API        |
+----------+-----------+
           |
           v
+----------------------+
|    Chat Service      |
+----------+-----------+
           |
           v
+----------------------+
|    WorkflowGraph     |
+----------+-----------+
           |
           v
+----------------------+
|  Supervisor Agent    |
+----------+-----------+
           |
           v
+----------------------+
|   Database Agent     |
+----------+-----------+
           |
           v
+----------------------+
|   SQL Generator      |
+----------+-----------+
           |
           v
+----------------------+
| Database Service     |
+----------+-----------+
           |
           v
+----------------------+
| Relational Database  |
+----------+-----------+
           |
           v
+----------------------+
|     Gemini LLM       |
+----------+-----------+
           |
           v
+----------------------+
| Business Response    |
+----------------------+
```

---

## 7. Detailed Execution Flow

### Step 1 – Receive Request

The Chat API receives a natural language database query.

---

### Step 2 – Supervisor Classification

The Supervisor Agent classifies the request as a structured data query and invokes the Database Agent.

---

### Step 3 – SQL Generation

The Database Agent converts the user's request into a parameterized SQL statement.

---

### Step 4 – Query Validation

The generated SQL is validated to ensure it complies with security policies.

Examples:

- Read-only operations
- Allowed schemas
- Row limits
- Parameterized queries

---

### Step 5 – Database Execution

The Database Service executes the validated SQL query.

---

### Step 6 – Result Processing

The returned rows are formatted into structured data.

---

### Step 7 – AI Response Generation

Gemini converts the structured results into a concise, business-friendly explanation.

---

### Step 8 – Response Delivery

The final response is returned to the user.

---

## 8. Component Responsibilities

| Component | Responsibility |
|------------|----------------|
| Chat API | Receives requests |
| Chat Service | Initiates workflow |
| WorkflowGraph | Coordinates execution |
| Supervisor Agent | Selects Database Agent |
| Database Agent | Generates SQL |
| SQL Generator | Creates parameterized SQL |
| Database Service | Executes queries |
| Gemini LLM | Explains query results |

---

## 9. Error Handling

| Failure | System Behaviour |
|----------|------------------|
| Invalid SQL | Reject query |
| Permission denied | Return authorization error |
| Database unavailable | Return service unavailable |
| Query timeout | Cancel execution |
| Empty result | Return "No matching records found." |

---

## 10. Security Considerations

- Enforce authentication.
- Apply role-based access control (RBAC).
- Allow only read-only operations by default.
- Validate generated SQL.
- Use parameterized queries.
- Audit all database access.

---

## 11. Performance Considerations

- Optimize SQL execution plans.
- Limit maximum returned rows.
- Use connection pooling.
- Cache frequently executed metadata queries.
- Monitor database latency.

---

## 12. Future Enhancements

- Multi-database support.
- Cross-database joins.
- Federated queries.
- Natural language analytics.
- Data visualization.
- Scheduled reports.

---

## 13. Success Criteria

The workflow is considered successful when:

- The Supervisor selects the Database Agent.
- SQL is generated correctly.
- The database query executes successfully.
- Results are summarized accurately.
- The response is returned within the configured service-level objective (SLO).

---

## Workflow Summary

```text
User
    │
    ▼
Chat API
    │
    ▼
Chat Service
    │
    ▼
WorkflowGraph
    │
    ▼
Supervisor Agent
    │
    ▼
Database Agent
    │
    ▼
SQL Generator
    │
    ▼
Database Service
    │
    ▼
Relational Database
    │
    ▼
Gemini
    │
    ▼
Business Response
```

---

**Workflow ID:** WF-009

**Workflow Name:** Structured Data Query

**Version:** 1.0

**Status:** Planned (Version 2.0)

**Owner:** Enterprise AI Orchestration Platform