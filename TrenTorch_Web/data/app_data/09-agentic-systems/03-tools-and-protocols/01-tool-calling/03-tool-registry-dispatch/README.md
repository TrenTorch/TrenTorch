---
name: agentic-tool-registry-dispatch
title: Tool Registry & Dispatch
tags: [agentic-systems, tools, mcp, dispatch]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Between the model's tool call and the actual function sits a **registry**: a table that knows which tools exist, describes them to the model, and dispatches calls by name. This is the core idea of protocols such as the Model Context Protocol (MCP), where a server _lists_ its tools and a client _calls_ them by name with arguments. The dispatcher must be defensive. An unknown tool name is a normal event (models hallucinate), and a tool that raises an exception must not crash the agent. Both should come back as a structured error result the model can read and react to.

### From theory to code

Implement the class `ToolRegistry`.

### Constraints

- `register(name, fn, description)` stores the tool. Registering an existing name raises `ValueError`.
- `list_tools()` returns a list of `{'name': ..., 'description': ...}` dicts sorted by name.
- `call(name, args)` returns `{'ok': True, 'result': fn(**args)}` on success.
- If `name` is not registered return `{'ok': False, 'error': 'unknown tool: {name}'}`. If the tool raises an exception `e`, return `{'ok': False, 'error': 'tool error: {e}'}` (using `str(e)`). Never let an exception escape `call`.

### Hints

<details>
<summary>Hint 1</summary>

Look the function up with `dict.get` and use `try/except Exception` around the invocation only.

</details>

<details>
<summary>Hint 2</summary>

A wrong argument name raises `TypeError` inside `fn(**args)`, and that is also reported as a tool error.

</details>

## Theory

### The simple version

A switchboard operator: the directory lists extensions, a connected call goes through, and a dead line or wrong number produces a polite message instead of the building catching fire.

### The formula

$$
\text{call}(n, a) = \begin{cases} (\text{ok}, f_n(a)) & n \in \text{registry},\ f_n \text{ returns}\\ (\text{error}, \text{unknown}) & n \notin \text{registry}\\ (\text{error}, \text{exception message}) & f_n \text{ raises}\end{cases}
$$

### How this is done in practice

MCP standardizes `tools/list` and `tools/call` over JSON-RPC so that any client can use any server's tools. Production registries add schemas, authorization, timeouts and result-size limits at exactly this chokepoint.

## Explanation

A dictionary and a guarded call. Structured error results (rather than exceptions) keep the agent loop simple: every call produces a result the model can observe.
