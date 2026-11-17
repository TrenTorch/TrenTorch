---
name: agentic-tool-permission-policy
title: Tool Permission Policies
tags: [agentic-systems, safety, permissions, guardrails]
difficulty: Beginner
---

## Statement

### The problem, from first principles

An agent that can run shell commands, send emails and delete files is only as safe as the rules that stand between a model's output and the real world. A **permission policy** is the simplest effective guardrail: a list of patterns saying which tool calls are allowed outright, which are forbidden and which need a human to approve first. Two design rules make it robust. **Deny beats allow**: an explicit prohibition cannot be overridden by a broad allowance. And the default is **deny**: anything the policy does not mention is blocked, so forgetting a rule fails safe instead of open.

### From theory to code

Implement `check_permission`.

### Constraints

- `call` is a string such as `'bash:rm -rf /tmp/x'` or `'email:send'`. `policy` is a dict with keys `deny`, `ask` and `allow`, each a list of glob patterns (use `fnmatch.fnmatchcase`).
- Return `'deny'` if any `deny` pattern matches. Else return `'ask'` if any `ask` pattern matches. Else return `'allow'` if any `allow` pattern matches. Otherwise return `'deny'`.
- Missing keys in `policy` mean an empty list.

### Hints

<details>
<summary>Hint 1</summary>

Test the three lists in priority order and return at the first hit.

</details>

<details>
<summary>Hint 2</summary>

`fnmatchcase('bash:rm -rf /', 'bash:rm *')` is `True`, since `*` matches any characters including spaces and slashes.

</details>

## Theory

### The simple version

A building's door policy: banned visitors are never let in, some visitors must be escorted, listed visitors enter freely and everyone else waits outside.

### The formula

$$
\text{decision}(c) = \begin{cases} \text{deny} & c \in D \\ \text{ask} & c \in A \\ \text{allow} & c \in L \\ \text{deny} & \text{otherwise}\end{cases}
$$

### How this is done in practice

Claude Code's permission rules, GitHub Actions' token permissions and cloud IAM policies all follow the same ordering of deny, then ask or allow, then default deny. Patterns on commands are a first line of defence and are paired with sandboxing, because string matching cannot catch every dangerous command.

## Explanation

A priority-ordered match. The tests focus on precedence, the property that most often breaks in real policy engines.
