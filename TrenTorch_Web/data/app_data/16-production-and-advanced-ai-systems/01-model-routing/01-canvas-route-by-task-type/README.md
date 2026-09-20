---
name: production-routing-canvas-route-by-task-type
title: Route by Task Type
tags: [production-systems, model-routing, canvas, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Not every request an application handles needs the same model. Generating code, writing a story, and classifying a short piece of text all call for different strengths -- and, just as importantly, cost very different amounts if sent to the same oversized model regardless of the task.

### The task

Wire each task type to the model best suited for it: code generation to the strong coding model, creative writing to the creative-tuned model, and simple classification to the small, fast model.

## Theory

### The simple version

A model router looks at what kind of request just came in and picks the model whose strengths match that request, rather than sending every request through one fixed model.

### Why task type is a reasonable routing signal

Task type is usually knowable up front, before any expensive model call happens -- it doesn't require running the request through a model first to find out what it needs. That makes it a cheap, reliable first routing signal, distinct from routing on cost or on a model's own confidence (both covered by other questions in this track).

### How this shows up in real systems

Production LLM applications commonly maintain a small routing layer in front of several models -- one tuned for code, one general-purpose, one fast and cheap for lightweight classification -- and pick between them per request instead of paying the largest model's cost and latency for every single call.

## Explanation

Each task connects to the model type that actually matches it. Always routing to the largest model regardless of task, and picking a model at random, are both distractors representing the two failure modes a real router avoids: over-paying for tasks that don't need it, and routing with no signal at all.
