# AG-002 – Planner Agent

## 1. Purpose

The Planner Agent is responsible for decomposing complex user requests into a sequence of executable tasks that can be performed by one or more specialized AI agents.

Unlike the Supervisor Agent, which decides **who** should execute a request, the Planner Agent determines **how** the request should be executed by creating an execution plan.

The Planner Agent is only invoked for requests that require multiple agents, multiple tools, or coordinated execution across enterprise systems.

---

## 2. Responsibilities

The Planner Agent is responsible for:

- Analyzing complex user requests.
- Breaking large tasks into smaller executable tasks.
- Identifying task dependencies.
- Selecting execution order.
- Identifying opportunities for parallel execution.
- Assigning tasks to specialized agents.
- Producing an execution plan for the Workflow Executor.

The Planner Agent does not execute business logic or invoke tools directly.

---

## 3. Position within the Architecture

```text
                   User
                     │
                     ▼
               Supervisor Agent
                     │
      requires_planning = true
                     │
                     ▼
               Planner Agent
                     │
                     ▼
             Execution Plan
                     │
                     ▼
            Workflow Executor
         ┌────────┼────────┐
         ▼        ▼        ▼
     Git Agent  RAG Agent Filesystem Agent
```

The Planner Agent is invoked only when the Supervisor Agent determines that a request cannot be completed by a single specialized agent.

---

## 4. Business Responsibilities

Typical planning scenarios include:

- Cross-system information retrieval.
- Enterprise architecture analysis.
- Release note generation.
- Root cause analysis.
- Compliance reporting.
- End-to-end documentation generation.
- Multi-source knowledge aggregation.

---

## 5. Inputs

The Planner Agent receives:

| Parameter | Description |
|-----------|-------------|
| User Request | Natural language request |
| Conversation Context | Previous messages |
| Routing Decision | Supervisor Agent output |
| Available Agents | Registered agents |
| Available Tools | Registered tools |
| Workflow Definitions | Workflow registry |

---

## 6. Outputs

The Planner Agent produces a structured execution plan.

Example:

```json
{
  "workflow_id": "WF-006",
  "execution_mode": "parallel",
  "tasks": [
    {
      "task_id": 1,
      "agent": "git",
      "description": "Retrieve recent commits"
    },
    {
      "task_id": 2,
      "agent": "rag",
      "description": "Retrieve sprint documentation"
    },
    {
      "task_id": 3,
      "agent": "filesystem",
      "description": "Retrieve deployment scripts"
    }
  ]
}
```

---

## 7. Planning Process

The Planner Agent follows this planning process.

```text
Receive Request
        │
        ▼
Understand Goal
        │
        ▼
Identify Tasks
        │
        ▼
Determine Dependencies
        │
        ▼
Assign Agents
        │
        ▼
Determine Parallelism
        │
        ▼
Generate Execution Plan
```

---

## 8. Planning Strategy

The Planner Agent applies the following principles:

- Minimize overall execution time.
- Execute independent tasks in parallel.
- Avoid duplicate work.
- Reuse previously retrieved information.
- Reduce unnecessary tool invocations.
- Preserve execution order where dependencies exist.

---

## 9. Interaction with Other Components

| Component | Interaction |
|-----------|-------------|
| Supervisor Agent | Receives planning request |
| Workflow Executor | Sends execution plan |
| Agent Registry | Discovers available agents |
| Tool Registry | Discovers available tools |
| Workflow Registry | Retrieves workflow definitions |
| Gemini LLM | Generates execution plan |

---

## 10. Prompt Strategy

The Planner Agent uses a structured planning prompt.

Example:

```text
You are the Planner Agent.

Your responsibility is to create an execution plan.

Break the user's request into executable tasks.

Assign each task to the most appropriate agent.

Return only valid JSON.
```

---

## 11. Execution Modes

The Planner Agent supports multiple execution strategies.

| Mode | Description |
|------|-------------|
| Sequential | Execute tasks one after another |
| Parallel | Execute independent tasks simultaneously |
| Hybrid | Combination of sequential and parallel execution |

---

## 12. Error Handling

| Failure | Behaviour |
|----------|-----------|
| Invalid execution plan | Regenerate plan |
| Unknown agent | Select alternative agent |
| Circular dependency | Reject plan |
| Planner timeout | Return planning failure |

---

## 13. Security Considerations

The Planner Agent:

- Never invokes enterprise tools directly.
- Never executes business operations.
- Produces read-only execution plans.
- Honors authorization rules.
- Logs planning decisions for auditing.

---

## 14. Performance Considerations

- Generate plans with minimal latency.
- Prefer parallel execution where possible.
- Cache workflow templates.
- Avoid unnecessary planning for simple requests.
- Target planning latency below 1 second.

---

## 15. Future Enhancements

Future improvements may include:

- Dynamic workflow optimization.
- Learning from previous executions.
- Cost-aware planning.
- SLA-aware planning.
- Automatic replanning after failures.
- Distributed workflow scheduling.

---

## 16. Sequence Diagram

```text
User
 │
 ▼
Supervisor Agent
 │
 ▼
Planner Agent
 │
 ▼
Execution Plan
 │
 ▼
Workflow Executor
 │
 ├────────► Git Agent
 ├────────► Enterprise RAG Agent
 ├────────► Filesystem Agent
 └────────► Database Agent
```

---

## 17. Design Principles

The Planner Agent follows these architectural principles:

- Separation of Concerns
- Stateless Planning
- Task Decomposition
- Dependency Awareness
- Extensibility
- Reusability

---

## 18. Success Criteria

The Planner Agent is considered successful when:

- Complex requests are correctly decomposed.
- Task dependencies are accurately identified.
- Appropriate agents are assigned.
- The execution plan is valid and executable.
- Independent tasks are optimized for parallel execution.

---

## Metadata

| Property | Value |
|----------|-------|
| Agent ID | AG-002 |
| Agent Name | Planner Agent |
| Type | Planning Agent |
| Category | Core Platform |
| Owner | Enterprise AI Orchestration Platform |
| Version | 1.0 |
| Status | Planned (Version 2.0) |