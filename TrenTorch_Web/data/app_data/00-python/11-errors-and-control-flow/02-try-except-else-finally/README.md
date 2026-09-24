---
name: python-errors-try-except-else-finally
title: "try / except / else / finally"
tags: [python-errors]
difficulty: Intermediate
---

## Statement

Implement functions that catch specific exceptions, run code only when no exception occurred, and guarantee cleanup code runs in every case.

## Theory

```python
try:
    value = int(text)
except ValueError:
    value = 0
```

If a `try` block statement raises, the rest of the block is skipped and Python checks `except` clauses top to bottom; the first matching type (an exact match or subclass) handles it. `except (ValueError, TypeError):` catches either type in one clause. Order clauses most-specific to most-general — a general clause first would swallow everything after it.

**`else`** runs only if the `try` block raised nothing — code there isn't protected by the `except` clauses, so a bug in it isn't accidentally caught.

**`finally`** runs in every case: normal completion, a handled exception, an unhandled one, and even a `return`/`break`/`continue` inside `try` or `except`. It's where cleanup belongs.

| Outcome | Blocks run |
|---|---|
| No exception | `try`, `else`, `finally` |
| Matching exception | `try` (to the error), `except`, `finally` |
| Unmatched exception | `try` (to the error), `finally`, then it keeps propagating |

**Where this matters later.** Loading a checkpoint that may not exist, or parsing a config value, are classic `try`/`except` uses; `finally` guarantees a resource is released even after failure.

## Explanation

`safe_int` catches `(ValueError, TypeError)` in one clause rather than two separate ones, since both failures get exactly the same fallback behavior (`return default`) — `int("x")` raises `ValueError`, `int(None)` raises `TypeError`, and neither needs to be distinguished here. `parse_pair` checks the split length first (`len(parts) != 2`) *before* attempting `int()` on anything, so a malformed `"3:4:5"` is rejected on its own without ever risking a wrong-index lookup into `parts`. `cleanup_return` puts its `return "early"` inside `try` (not `finally`) and lets `finally`'s `log.append("cleanup")` run either way — a `return` inside `finally` would silently swallow the `try` block's own return value, which is exactly the trap the theory warns against.
