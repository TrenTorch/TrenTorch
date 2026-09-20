---
name: production-routing-canvas-cascade-cheap-to-expensive
title: A Cascade — Cheap Model First, Confidence Check, Escalate if Needed
tags: [production-systems, model-routing, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Most requests a cheap, fast model handles are actually easy enough that it gets them right. Paying for the expensive model on every single one, just to cover the minority it would get wrong, wastes money and latency on the majority it wouldn't have.

### The task

Wire a cascade: call the cheap model first, check its confidence, and only call the expensive model when that confidence is too low to trust -- returning the cheap model's own answer whenever it's confident enough.

## Theory

### The simple version

Try cheap first. If the cheap model seems sure of its answer, use it and stop there. If it doesn't, escalate to the expensive model and use that instead. Most requests never reach the expensive model at all.

### Why a confidence check, not just "always escalate" or "never escalate"

Calling both models on every request (defeating the entire point of having a cheap option) and skipping the cheap model entirely (defeating the entire point of the cascade) are the two ways to get this wrong. The confidence check is what makes the cascade selective: expensive-model cost is paid only on the subset of requests that actually need it, decided per request rather than by a fixed policy.

### How this shows up in real systems

This is a standard cost-optimization pattern for LLM applications with high request volume: a small model handles the bulk of traffic, and only the harder tail -- identified by low confidence, not by guessing in advance -- gets routed to a stronger, pricier model.

## Explanation

The cheap model runs first on every request; its confidence then branches the flow -- confident enough returns its own answer directly, not confident enough calls the expensive model and returns that answer instead. Calling both models unconditionally and skipping the cheap model are both distractors describing the two ways a cascade collapses back into either "always expensive" or "never verified."
