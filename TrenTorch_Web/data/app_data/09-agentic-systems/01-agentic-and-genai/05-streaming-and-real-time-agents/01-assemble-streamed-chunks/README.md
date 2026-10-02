---
name: production-streaming-assemble-stream
title: Assemble a Streamed Response Into Display Snapshots
tags: [production-systems, streaming, real-time-agents]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A streamed LLM response doesn't arrive as one string -- it arrives as a sequence of small chunks, and a UI rendering it live needs to know, after each chunk, what the full text looks like so far. Storing only the raw chunks means recomputing that concatenation on every single render.

### The task

Write `assemble_stream(chunks)` that returns the list of cumulative text snapshots: `snapshots[i]` is everything received up through and including `chunks[i]`.

## Theory

### The simple version

Keep a running accumulated string. After each chunk arrives, append it, and record the accumulated string at that point. The result is a list the same length as the input, where each entry is "the text as it looked right after this chunk landed."

### Why precompute snapshots instead of concatenating chunks on demand

A live UI redraws on every chunk, and redraws are frequent (potentially dozens per second on a fast stream). Recomputing `"".join(chunks[:i+1])` on every redraw is wasted work that grows with the stream's length; keeping a single running accumulator and appending once per chunk does the same job in constant work per chunk.

### How this shows up in real systems

This is exactly the loop behind a typewriter-style streaming UI: each server-sent chunk triggers exactly one state update, and the displayed text is just the latest accumulated value -- never a fresh recomputation from the start of the stream.

## Explanation

A single running string is appended to once per chunk, and the accumulated value is snapshotted into the result list immediately after each append -- so the list's length always matches the chunk count, and each entry reflects exactly what had arrived by that point, no more and no less.
