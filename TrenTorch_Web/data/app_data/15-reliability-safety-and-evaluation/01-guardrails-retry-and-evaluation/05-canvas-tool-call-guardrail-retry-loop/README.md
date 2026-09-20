---
name: agentic-guardrails-canvas-tool-call-guardrail-loop
title: Tool-Call Guardrail and Retry Loop
tags: [agentic-systems, guardrails, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A guardrail that only ever blocks a bad tool call, with no path back to a corrected one, wastes an otherwise-recoverable situation — the same principle behind *Retry a Malformed Tool Call With Model-Guided Correction*, applied to guardrail failures instead of schema-validation failures. And just like every other retry loop in this curriculum, it needs a real exit: retrying forever isn't actually safer than not retrying at all.

### The task

Wire the guardrail-check-then-retry cycle so a failing call gets one more chance with feedback, and repeated failure eventually aborts — never retries without limit, and never executes despite a failed check.

## Theory

### The simple version

Every proposed tool call passes through a guardrail check before execution. Passing goes straight to execution. Failing goes to a retry step that feeds the guardrail's specific objection back into a new proposal — which then goes through the same check again. That retry step also has its own exit: after enough failed attempts, abort instead of looping forever.

### Why unlimited retries aren't actually safer

A guardrail that keeps retrying indefinitely on a call that keeps failing the same check isn't providing safety — it's providing an infinite loop that never actually stops the bad call, just delays it, while burning unbounded time and tokens in the process. A bounded retry with an explicit abort path is what makes "the guardrail caught something" end in an honest, finite outcome (a corrected call, or a clean failure) rather than a run that simply never terminates.

### How this shows up in real systems

This mirrors the exact same retry-with-budget shape used throughout this curriculum (tool-call retries, JSON-repair retries, re-query loops) applied specifically to a safety check rather than a syntactic one — the pattern is identical because the underlying reliability problem (partial failures deserve a bounded second chance, not an unbounded one) is the same regardless of what kind of check is failing.

## Explanation

The cycle runs propose -> guardrail-check -> (execute | retry-with-feedback), with `retry_with_feedback` looping back into `tool_call_proposed` for another attempt, but also connecting forward to `abort` — the second edge is what gives the loop a real exit instead of only ever looping. Neither distractor connects to anything: retrying with no bound at all removes the exit this topology deliberately provides, and executing despite a failed guardrail check throws away the entire point of checking in the first place.
