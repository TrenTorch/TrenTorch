---
name: agentic-observability-compute-run-cost
title: Compute the Total Cost of an Agent Run
tags: [agentic-systems, agent-observability, tracing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

An agent run might make a dozen LLM calls before it finishes, each with its own input and output token count, and each possibly billed at a different rate if the agent switched models mid-run (a cheap model for routing, an expensive one for the final answer). "How much did this run cost" only has an answer if every one of those calls is accounted for.

### The task

Write `compute_run_cost(calls)` that takes a list of `(input_tokens, output_tokens, input_price_per_1k, output_price_per_1k)` tuples and returns a dict with the summed `total_input_tokens`, `total_output_tokens`, and `total_cost` across every call.

## Theory

### The simple version

Standard LLM pricing is per-1000-tokens, and input and output tokens are usually priced differently (output is typically pricier). Cost per call is `input_tokens/1000 * input_price + output_tokens/1000 * output_price`; the run's total cost is just the sum of that over every call.

### Why per-call prices, not one global price

A single run frequently isn't one model end to end -- routing, planning, and drafting might use a fast/cheap model while the final synthesis step uses a stronger, pricier one. Carrying the price alongside each call (rather than assuming one fixed rate for the whole run) is what makes the total correct when the model actually varies per call.

### How this shows up in real systems

This is exactly what a cost dashboard for an LLM application computes per request, per user, or per day -- the same per-call token-times-price arithmetic, just aggregated at a larger scale and over a longer window.

## Explanation

Token counts are summed directly; cost is accumulated call by call using each call's own prices, since a fixed global rate would silently produce the wrong total the moment two calls in the same run use different prices -- which real multi-model runs do routinely.
