---
name: production-routing-canvas-cost-aware-router
title: A Cost-Aware Router
tags: [production-systems, model-routing, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The same application often serves requests with very different stakes: a customer-facing response that a real user is waiting on, and an internal batch job summarizing yesterday's logs. Both could technically be handled by the same model, but paying premium-model prices for the batch job (which nobody is waiting on and won't notice the quality difference) is pure waste.

### The task

Route the customer-facing critical response to the premium model, and the internal batch job to the budget model.

## Theory

### The simple version

A cost-aware router weighs how much a request's outcome matters against how much a stronger model costs, and only pays the premium where the outcome actually justifies it.

### Why "always use the best" and "always use the cheapest" are both wrong

Always using the best model wastes money on requests where a cheaper model would have produced an indistinguishable result. Always using the cheapest model risks quality on requests where the difference genuinely matters to a real user. A cost-aware router isn't "cheap" or "expensive" as a fixed policy -- it's a decision made per request, based on what that specific request's stakes call for.

### How this shows up in real systems

This is standard practice in any LLM application handling a mix of interactive and background workloads: interactive, user-visible paths get the stronger (and pricier) model, while offline or low-stakes batch work runs on the cheaper one, often on a completely different budget line.

## Explanation

The critical customer-facing path routes to the premium model because its outcome is directly visible to a real user; the internal batch job routes to the budget model because nothing about its purpose requires premium accuracy. Both distractors describe the fixed, one-size-fits-all policies a genuinely cost-aware router replaces.
