---
name: production-streaming-detect-early-tool-call
title: Detect a Tool Call Marker as It Streams In
tags: [production-systems, streaming, real-time-agents]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A streaming model often signals a tool call with a special marker embedded in its output (e.g. `<tool_call>`), but that marker isn't guaranteed to land inside a single chunk -- streaming APIs split text at arbitrary byte or token boundaries, so the marker can easily be cut in half across two consecutive chunks.

### The task

Write `detect_early_tool_call(chunks, marker)` that returns the index of the first chunk after which the accumulated text contains `marker`, or `None` if it never appears.

## Theory

### The simple version

Checking each chunk in isolation for the marker will miss it whenever the marker spans a chunk boundary. Checking the _accumulated_ text after each chunk catches it regardless of where the split happened.

### Why detecting this matters for a real-time agent

The whole point of streaming a response to the user is showing it as it arrives. But if the model is mid-way through emitting a tool call, that raw markup shouldn't be shown as if it were part of the answer -- the UI needs to know the instant a tool call starts so it can switch to a "calling a tool..." indicator instead of rendering `<tool_call>` literally.

### How this shows up in real systems

This is why real streaming parsers buffer and re-check accumulated text rather than pattern-matching each chunk independently -- the same technique used to detect any multi-character delimiter (a closing code fence, a JSON key, a stop sequence) in a token-by-token or chunk-by-chunk stream.

## Explanation

The function accumulates chunks one at a time and checks the _growing_ string for `marker` after each addition, returning the index the moment it's found -- checking the accumulated text rather than each chunk alone is exactly what makes a split-across-chunks marker (like `<tool_` + `call>`) still detectable.
