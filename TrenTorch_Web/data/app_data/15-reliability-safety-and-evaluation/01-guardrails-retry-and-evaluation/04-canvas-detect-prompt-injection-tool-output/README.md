---
name: agentic-guardrails-canvas-detect-injection
title: Detect Prompt Injection in a Tool Output
tags: [agentic-systems, guardrails, security, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A tool's output isn't just data — if that tool fetched a web page, read a file, or queried an API someone else controls, its content might contain text specifically crafted to look like an instruction ("ignore previous instructions and instead..."). An agent that treats every tool output as automatically trustworthy is vulnerable to exactly this: a hostile string embedded in retrieved content, executed as if the agent's own operator had written it.

### The task

Wire the scan step so every tool output gets checked before it reaches the model, branching to either "pass through as data" or "sanitize and flag" — never straight through unchecked, and never executed as an instruction.

## Theory

### The simple version

Every tool output passes through one gate before the model ever sees it: scan it for injection-looking patterns. Clean output gets passed along, explicitly tagged as data (never as an instruction). Suspicious output gets sanitized and flagged rather than passed through untouched.

### Why tool output can never be treated the same as a system instruction

A system instruction comes from whoever configured the agent and is inherently trusted. A tool output comes from wherever the tool fetched it from — a web page, a document, an API response — which could be controlled by anyone, including someone actively trying to manipulate the agent. Collapsing that distinction (trusting tool output the same as a system instruction) is precisely what makes indirect prompt injection possible in the first place; keeping it is the entire defense.

### How this shows up in real systems

Any agent that retrieves content from a source it doesn't fully control (web search, document retrieval, third-party APIs) needs this scan-before-trust step, because the alternative — executing whatever text an external, untrusted source happens to contain — turns every tool with access to untrusted content into an attack surface.

## Explanation

The chain runs `Tool output received` -> `Scan for injection patterns`, and only from the scan does the flow branch: clean output proceeds to `Pass to model, tagged as data` (note: tagged as *data*, never merged into the model's own instructions), while suspicious output goes to `Sanitize and flag` instead. Neither distractor piece connects to anything, since both describe the exact failure this guardrail exists to prevent — executing an embedded instruction, or trusting the tool's output at the same level as a real system instruction.
