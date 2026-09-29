---
name: agentic-security-audit-log
title: Build an Audit Log of Agent Actions
tags: [agentic-systems, agent-security, observability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

When an agent has been given real permissions -- to read files, call tools, edit records -- the question "what did it actually do, and when" needs a real answer, not a best guess reconstructed after the fact. An audit log is the plain, append-only record of every action an agent took, in the order it took them.

### The task

Write `build_audit_log(actions)` that turns a list of `(timestamp, actor, description)` tuples into formatted lines of the form `"[timestamp] actor: description"`, preserving order.

## Theory

### The simple version

Every action an agent takes gets one line: when, who, what. No filtering, no summarizing, no reordering -- an audit log's entire value comes from being a faithful, literal record.

### Why this is a security control, not just logging

If a tool-permission policy or a least-privilege boundary is ever bypassed -- a bug, a successful injection, a misconfigured grant -- the audit log is what lets someone reconstruct exactly what happened afterward: which agent, which action, at what time. A system with real permissions but no audit trail can be compromised without anyone finding out until the damage is already visible elsewhere.

### How this shows up in real systems

This is the same discipline behind any compliance-grade audit trail: an admin action in a cloud console, a database write with row-level history, a financial ledger entry. The format differs, but the property that matters is the same -- append-only, ordered, and attributable to a specific actor.

## Explanation

The function maps each `(timestamp, actor, description)` tuple straight into `f"[{timestamp}] {actor}: {description}"`, in the order the actions were given -- an audit log's job is to record faithfully, not to interpret or reorder, so there's nothing here beyond a direct format-and-collect.
