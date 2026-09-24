---
name: python-errors-assemble-job-runner
title: "Assemble: Run Jobs With Retries and Guaranteed Logging"
tags: [python-errors]
difficulty: Advanced
---

## Statement

Implement a small job runner that retries transient failures, converts other failures into a custom exception with its cause preserved, and logs the start and end of every job through a context manager.

## Theory

This problem introduces no new concepts. It combines this module's topics into one realistic task:

- Raise, propagate, and stop exceptions at the right level.
- Use `try`, `except`, `else`, and `finally` to separate retry handling from success handling.
- Define custom exception classes and chain an underlying error with `from`.
- Use a context manager class so that "end" is always logged, even when a job fails.

A **transient** error (`TransientError`) is a temporary condition that may succeed on a later attempt. Any other exception from a job is permanent — retrying won't help. A job that succeeds returns a value; a job that never succeeds produces a `JobFailedError`. The logging context manager must never hide exceptions.

## Explanation

`run_job` wraps its whole retry loop in `with JobLogger(label, log):`, so `"end {label}"` is written by `__exit__` regardless of how the function leaves the block — a successful return, a raised `JobFailedError`, or anything else. Inside the loop, `try`/`except`/`else` cleanly separates the three outcomes per attempt: `except TransientError` records the error and lets the loop continue to the next attempt; `except Exception` (anything else) immediately raises `JobFailedError(label, n) from e` with no retry, since a non-transient failure won't be fixed by trying again; `else: return result` returns only when `func()` raised nothing at all, which is exactly what the "use `else` for the return" requirement is checking — a `return` placed directly in `try` would also fire if an exception got raised and then somehow ignored, which `else` structurally can't do. `run_jobs` wraps each `run_job` call in its own `try`/`except JobFailedError`, so one job's failure only updates `failed` for that label and never interrupts the loop over the remaining jobs.
