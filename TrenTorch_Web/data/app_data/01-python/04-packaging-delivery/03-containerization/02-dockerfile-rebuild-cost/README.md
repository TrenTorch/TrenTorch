---
name: python-dockerfile-rebuild-cost
title: Order a Dockerfile for the Build Cache
tags: [python-packaging, containerization, docker, build-cache, optimization]
difficulty: Advanced
---

## Statement

Write `rebuild_cost(dockerfile, changed)`, which computes how long a rebuild takes given which source files changed, then use it to see why copying `requirements.txt` before the rest of the source makes rebuilds fast.

## Theory

Docker's [best practices](https://docs.docker.com/build/building/best-practices/) and [cache docs](https://docs.docker.com/build/cache/) combine into one habit: put **stable, expensive** instructions early and **frequently changing** ones late. Because invalidation cascades downward, a change near the top re-runs everything below it, including slow steps like `pip install`.

Compare two Dockerfiles for the same app:

```dockerfile
# Slow: any source edit invalidates the install
COPY . .
RUN pip install -r requirements.txt

# Fast: the install is only invalidated when requirements.txt changes
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

In the fast version, editing `app.py` only invalidates the final `COPY`. The install layer stays cached.

Model: a Dockerfile is a list of steps `{"cmd": "COPY", "files": [...], "cost": seconds}`. A `COPY` or `ADD` step is invalidated when any of **its own** files changed. A `RUN` step is never invalidated directly by file changes in this model; it only re-runs because an earlier step was invalidated. Once any step is invalidated, it and every later step runs again.

## Explanation

One pass with an `invalidated` flag expresses the cascade exactly as in the previous question: once the flag turns on it never turns off. Only `COPY`/`ADD` can switch it on, using the intersection of the step's files with the changed set. Summing costs for steps after the flag turns on gives the rebuild time. The test file compares the naive and cache-friendly orderings on the same change to make the benefit measurable rather than a rule of thumb.
