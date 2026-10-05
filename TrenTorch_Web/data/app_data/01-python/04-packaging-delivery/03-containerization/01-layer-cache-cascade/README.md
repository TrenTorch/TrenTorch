---
name: python-layer-cache-cascade
title: Which Layers Does Docker Rebuild?
tags: [python-packaging, containerization, docker, build-cache]
difficulty: Intermediate
---

## Statement

Write `rebuilt_steps(previous, current)`, which simulates Docker's layer cache and returns the indexes of the build steps that have to be re-executed.

## Theory

A Docker image is a **stack of layers**, one per Dockerfile instruction. Docker's [build cache documentation](https://docs.docker.com/build/cache/) gives the two rules that decide what gets rebuilt:

1. **A layer is reused only if nothing it depends on changed.** For `COPY`, that means the copied files; for `RUN`, the command text and everything below it.
2. **Cascading invalidation**: "Once a layer changes, then all downstream layers need to be rebuilt as well. Even if they wouldn't build anything differently, they still need to re-run."

So the cache behaves like a prefix match. Walk the steps top to bottom; the first step that differs from the previous build is rebuilt, and **so is every step after it**, even steps that are identical to last time.

Here each step is a pair `(instruction, input_digest)`, where the digest stands for whatever the step's cache key depends on (for a `COPY`, a hash of the files). Two builds produce the same cached layer for step _i_ only if all steps _0..i_ are equal.

## Explanation

The `cached` flag captures the cascade: once any step misses, it flips to `False` for good, so every later step is rebuilt regardless of whether it matches. Steps beyond the length of the previous build have nothing to reuse, so they naturally fall into the rebuilt list. Steps removed from the end of the file cost nothing because nothing is built for them.
