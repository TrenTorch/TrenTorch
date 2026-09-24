---
name: python-errors-raising-custom-exceptions
title: Raising Your Own Exceptions
tags: [python-errors]
difficulty: Intermediate
---

## Statement

Implement a custom exception class, functions that raise it with useful data, and functions that re-raise or chain exceptions while preserving their cause.

## Theory

**Choose the built-in type that best describes the problem** — `ValueError` for a bad value, `TypeError` for a bad type — with a message stating what was wrong.

**Custom exception classes** inherit from `Exception` when built-ins are too general:

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, requested):
        super().__init__(f"balance {balance} is less than {requested}")
        self.balance = balance
        self.requested = requested
```

`super().__init__(message)` sets the exception's message so `str(e)` works; extra attributes carry structured data a handler can read directly (`e.balance`) without parsing text.

**Re-raising.** A bare `raise` inside an `except` block re-raises the *same* exception, unchanged — used to log or clean up and let the error keep propagating.

**Chaining.** `raise NewError(...) from original` raises a new exception recording `original` as its cause, available as `new.__cause__` — used to translate a low-level error into a meaningful one without losing the underlying information.

**`assert condition, message`** raises `AssertionError(message)` if `condition` is falsy — a debugging aid stating an internal assumption, not a way to validate user input.

**Where this matters later.** Library code validates shapes and argument values by raising precise `ValueError`/`TypeError`s; a good message is what makes shape errors fast to diagnose.

## Explanation

`parse_positive_int` catches the `ValueError` from a bad `int()` conversion and re-raises a *new*, clearer `ValueError` `from` the original — preserving `__cause__` — but the *separate* "not positive" check runs only after a successful conversion and raises its own plain `ValueError` with no cause, since that failure has nothing underlying it to chain from. `log_and_reraise` catches `Exception`, appends `str(exception)` to the log, then uses a bare `raise` (not `raise exception`) specifically so the exact same exception object — not a copy — continues on to the caller, which is what the hidden tests verify via identity.
