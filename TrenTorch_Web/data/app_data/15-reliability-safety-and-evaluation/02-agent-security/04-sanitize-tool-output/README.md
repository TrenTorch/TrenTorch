---
name: agentic-security-sanitize-tool-output
title: Sanitize a Tool's Output Before It Reaches the Model
tags: [agentic-systems, agent-security, guardrails]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A tool call often returns more than the agent needs: a database query might return a customer's full record including a card number, a shell command's output might echo an API key from an environment variable. That raw output usually flows straight back into the model's context, and from there it can end up quoted in a response, logged, or forwarded to another agent.

### The task

Write `sanitize_tool_output(output, forbidden_patterns)` that replaces every occurrence of every string in `forbidden_patterns` with `"[REDACTED]"`, checking patterns in the order given, and returns the result.

## Theory

### The simple version

Before a tool's raw output is handed to the model (or logged, or passed to another agent), pattern-match it against a list of things that must never leak, and strip them out. It's the same idea as scrubbing PII from logs, applied to the boundary between a tool and the agent that called it.

### Why this has to happen at the boundary, not "later"

Once forbidden content is inside the model's context, it can be echoed back in a response, summarized into a downstream message, or persisted in a trace -- there's no reliable way to guarantee it never resurfaces. Redacting at the moment the tool output arrives is the only point where you can be sure it's caught before it propagates anywhere else.

### Why pattern order matters

If one forbidden pattern is a substring of another (or overlaps with it), redacting in one order can consume the text a later pattern would have matched, while the reverse order might not. This function follows the order it's given rather than picking one for you, since which order is "right" depends on which patterns the caller considers more specific.

## Explanation

The function walks `forbidden_patterns` in order and calls `.replace()` for each one against the running (already partially sanitized) string, so a pattern that has already been redacted by an earlier, broader pattern won't be found again by a later, narrower one -- which is exactly the behavior the "ab" then "a" test case is checking for.
