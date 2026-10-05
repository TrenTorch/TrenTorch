---
name: agentic-observability-classify-failures
title: Classify Failures Into Categories
tags: [agentic-systems, agent-observability, evaluation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A hundred failed agent runs, each with its own raw error message, doesn't tell anyone what to fix. "17 timeouts, 12 auth errors, 3 rate limits, 68 uncategorized" does -- it turns a pile of unstructured text into a short list of where the real problems are.

### The task

Write `classify_failures(failures, categories)`, where `categories` maps a category name to a list of keywords. For each failure message, find the first category (in the order `categories` is given) whose keyword list has a match as a substring of the message, and count it there; a message matching nothing counts under `"UNCATEGORIZED"`. Return counts for every category plus `"UNCATEGORIZED"`, including zeros.

## Theory

### The simple version

This is keyword-based triage: cheap, deterministic, and good enough to sort the bulk of failures into buckets a person (or a more expensive process) can look at category by category instead of message by message.

### Why keyword order, and category order, both matter

A message can plausibly match more than one category's keywords (a timeout that also mentions a rate limit, say). Checking categories in a fixed order and stopping at the first match makes the classification deterministic and reproducible -- the same failure always lands in the same bucket, which matters when someone is tracking a category's count over time.

### How this shows up in real systems

This is the same triage a log-monitoring or error-tracking tool does automatically: bucket incoming errors by pattern so a dashboard can show "timeouts are up 3x this week" instead of a raw, unreadable stream of every individual error string.

## Explanation

Every category starts at zero (plus `"UNCATEGORIZED"`) so the result always reports every bucket, even ones with no matches. Each failure is checked against categories in their given order, and the loop's `else` clause (the for/else form) fires only when no `break` happened -- i.e. no category matched -- which is exactly the "count under UNCATEGORIZED" case.
