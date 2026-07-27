# AG-006 – Database Agent

## 1. Purpose

The Database Agent is responsible for retrieving, analyzing, and presenting information stored in enterprise relational databases using natural language requests.

The agent converts business questions into secure database operations, executes validated queries, processes structured results, and collaborates with the Large Language Model (LLM) to generate business-friendly responses.

The Database Agent enables users to interact with enterprise databases without requiring SQL expertise.

---

## 2. Responsibilities

The Database Agent is responsible for:

- Understanding natural language database requests.
- Identifying relevant database schemas.
- Generating secure SQL statements.
- Validating SQL before execution.
- Executing read-only database queries.
- Formatting structured results.
- Summarizing query results.
- Returning structured and natural language responses.

The Database Agent never performs schema modifications or data updates unless explicitly configured to support write operations.

---

## 3. Position within the Architecture

```text
                    User
                      │
                      ▼
              Supervisor Agent
                      │
                      ▼
               Database Agent
                      │
          ┌───────────┴────────────┐
          ▼                        ▼
      SQL Generator         Tool Registry
          │                        │
          ▼                        ▼
   Database Service          MCP Server
          │
          ▼
 Relational Database
(PostgreSQL / MySQL / Oracle)
          │
          ▼
      Gemini LLM
          │
          ▼
 Business Response
```

---

## 4. Business Responsibilities

Typical requests include:

- Show today's orders.
- List active customers.
- Display monthly sales.
- Find invoices for a customer.
- Show employee information.
- Retrieve product inventory.
- Explain database records.
- Generate business summaries.

---

## 5. Inputs

| Parameter | Description |
|-----------|-------------|
| User Query | Natural language request |
| Database Metadata | Schemas, tables, relationships |
| Conversation Context | Previous interactions |
| User Permissions | Database access privileges |

---

## 6. Outputs

Example response:

```json
{
  "query": "SELECT customer_name, revenue FROM sales LIMIT 10;",
  "rows_returned": 10,
  "summary": "The top customer this month is ABC Corporation."
}
```

---

## 7. Processing Pipeline

```text
Receive Request
      │
      ▼
Understand Intent
      │
      ▼
Generate SQL
      │
      ▼
Validate SQL
      │
      ▼
Execute Query
      │
      ▼
Process Results
      │
      ▼
Generate Summary
      │
      ▼
Return Response
```

---

## 8. Supported Operations

| Operation | Description |
|-----------|-------------|
| SELECT | Retrieve data |
| Aggregate Queries | COUNT, SUM, AVG, MIN, MAX |
| Filtering | WHERE conditions |
| Sorting | ORDER BY |
| Pagination | LIMIT / OFFSET |
| Joins | Multi-table retrieval |
| Metadata Discovery | Schema inspection |

---

## 9. Interaction with Other Components

| Component | Interaction |
|-----------|-------------|
| Supervisor Agent | Receives routing decision |
| WorkflowGraph | Executes workflow |
| SQL Generator | Produces SQL statements |
| Database Service | Executes validated SQL |
| Tool Registry | Resolves database tools |
| MCP Server | External database integration |
| Gemini LLM | Explains structured results |

---

## 10. Prompt Strategy

Example system prompt:

```text
You are an Enterprise Database Agent.

Generate safe, read-only SQL based on the user's request.

Use only approved schemas and tables.

Never generate UPDATE, INSERT, DELETE, DROP, ALTER, or TRUNCATE statements.

Return only validated SQL.
```

---

## 11. Security Considerations

The Database Agent:

- Uses read-only database credentials by default.
- Validates generated SQL.
- Prevents SQL injection.
- Uses parameterized queries.
- Enforces row-level security where applicable.
- Audits database access.

---

## 12. Error Handling

| Failure | Behaviour |
|----------|-----------|
| Invalid SQL | Reject and regenerate |
| Connection failure | Return service unavailable |
| Query timeout | Cancel execution |
| Permission denied | Return authorization error |
| Empty result | Inform the user |

---

## 13. Performance Considerations

- Use connection pooling.
- Limit returned rows.
- Optimize SQL execution plans.
- Cache metadata.
- Monitor query latency.
- Avoid full table scans where possible.

---

## 14. Technology Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | API layer |
| LangGraph | Workflow orchestration |
| SQLAlchemy | Database abstraction |
| PostgreSQL | Primary relational database |
| MCP | External database integration |
| Gemini 2.5 Flash | Natural language generation |

---

## 15. Future Enhancements

Future improvements may include:

- Multi-database federation.
- Automatic schema discovery.
- Query optimization.
- Data visualization.
- Business intelligence dashboards.
- Stored procedure support.
- Cross-database analytics.

---

## 16. Sequence Diagram

```text
User
 │
 ▼
Supervisor Agent
 │
 ▼
Database Agent
 │
 ├────────► SQL Generator
 │
 ├────────► Database Service
 │
 ├────────► Tool Registry
 │
 ├────────► MCP Server
 │
 ▼
Gemini
 │
 ▼
Business Response
```

---

## 17. Design Principles

The Database Agent follows these architectural principles:

- Read-only by default.
- Secure SQL generation.
- Least privilege.
- Separation of query generation and execution.
- Stateless execution.
- Extensible database connectivity.

---

## 18. Success Criteria

The Database Agent is considered successful when:

- The user's intent is correctly translated into SQL.
- The SQL passes validation.
- The query executes successfully.
- Results are summarized accurately.
- Responses are returned within the configured service-level objective (SLO).

---

## Metadata

| Property | Value |
|----------|-------|
| Agent ID | AG-006 |
| Agent Name | Database Agent |
| Type | Specialized AI Agent |
| Category | Structured Data Retrieval |
| Owner | Enterprise AI Orchestration Platform |
| Version | 1.0 |
| Status | Planned (Version 2.0) |