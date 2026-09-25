---
name: python-errors-with-context-managers
title: with Blocks and Context Managers
tags: [python-errors]
difficulty: Intermediate
---

## Statement

Implement context managers as classes and as generator functions, and use `with` to guarantee setup and cleanup around a block of code, including when an exception occurs.

## Theory

A **context manager** defines `__enter__(self)` (runs at the start of the block, its return value bound after `as`) and `__exit__(self, exc_type, exc_value, traceback)` (runs when the block ends, whether it finished normally or was interrupted by an exception).

```python
with manager as target:
    body
```

behaves as: call `__enter__()`, store in `target`; run `body`; call `__exit__(...)` — all `None` if `body` finished normally, or the exception's details if it raised. If `__exit__` returns **truthy**, the exception is suppressed; otherwise (including `None`) it keeps propagating.

**Writing one with a generator.** `@contextlib.contextmanager` turns a generator with exactly one `yield` into a context manager — code before `yield` is setup, the yielded value is what `as` receives, code after `yield` is cleanup. Wrap the `yield` in `try`/`finally` so cleanup runs even if the block raises:

```python
@contextmanager
def temporary(settings, key, value):
    old = settings[key]
    settings[key] = value
    try:
        yield
    finally:
        settings[key] = old
```

**Where this matters later.** `torch.no_grad()` is a context manager — gradient tracking switches off for the block and back on when it ends, even on error.

## Explanation

`Recorder.__exit__` always appends `"exit"` first, then conditionally appends an `"error:..."` entry only if `exc_type is not None` — the ordering matters because the hidden tests check the exact log sequence, and `__exit__` receiving non-`None` arguments is precisely how it learns an exception happened, without needing a `try`/`except` of its own. `temporary_value` wraps its single `yield` in `try`/`finally`, restoring `settings[key]` in the `finally` — this is what makes the restoration happen even when the `with` block itself raises, since a generator's `finally` still runs when an exception is thrown into it at the `yield` point.
