---
name: python-errors-exceptions-and-flow
title: "Exceptions: What Raising Does to Program Flow"
tags: [python-errors]
difficulty: Beginner
---

## Statement

Implement functions that raise exceptions and a chain of nested calls that is interrupted midway, showing exactly which statements run and which are skipped.

## Theory

An **exception** is an object representing an error, whose type is a class inheriting from `Exception`. Common types: `ValueError` (right type, bad value), `TypeError` (unsupported type), `IndexError` (bad sequence position), `KeyError` (missing dict key), `ZeroDivisionError`, `AttributeError`.

**Raising.** `raise ValueError("...")` constructs the exception instance and starts the error process.

**What raising does to program flow:**

1. The raising statement stops — no later statement in that function body runs.
2. Python looks for a handler in the current function. If there is none, the function is **abandoned**: its locals are discarded, control returns to the caller as if the call itself had raised.
3. This repeats up the chain of callers — **unwinding**.
4. If it unwinds past the outermost call with no handler, the program stops with a traceback.

```python
def level_three():
    raise RuntimeError("boom")
    print("never runs")
```

Raising is a **transfer of control**, not a value — no `return` happens, and nothing downstream of the raise in that call (or any caller that doesn't catch it) runs.

**Where this matters later.** Shape mismatches and out-of-range indices in ML code raise from deep inside library calls; reading a traceback from the last line upward is the fastest way to find what failed.

## Explanation

`level_three` writes its "L3 end" append statement *after* the `raise`, exactly as instructed — it's there in the source, syntactically real code, but unreachable, which is the concrete demonstration that a raised exception genuinely skips the rest of the function body rather than merely being a convention. `first_element` does not check `len(items) == 0` before indexing — the spec explicitly wants Python's own `IndexError` from `items[0]` on an empty list, not a hand-written check that might raise something else or return a wrong sentinel.
