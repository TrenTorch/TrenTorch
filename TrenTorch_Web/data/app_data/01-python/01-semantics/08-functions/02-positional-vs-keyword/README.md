---
name: python-functions-positional-vs-keyword
title: Positional vs Keyword Arguments
tags: [python-function-arguments]
difficulty: Beginner
---

## Statement

Implement functions that are called using positional arguments, keyword arguments, and combinations of both.

## Theory

**Positional arguments** are matched by position: `describe("A", 18, "Delhi")` sends `"A"` to the first parameter, `18` to the second, and so on.

**Keyword arguments** identify their parameter by name, and their order doesn't need to match the parameter order: `describe(city="Delhi", name="A", age=18)`.

**Mixing** is allowed as long as positional arguments come first: `describe("A", age=18, city="Delhi")` is valid; a positional argument after a keyword argument is a syntax error.

**Repeating a parameter** — supplying the same parameter both positionally and by keyword in one call — raises `TypeError`, since Python can't decide which value that parameter should get.

**Positional-only and keyword-only parameters.** `def f(a, b, /, c)` forces `a` and `b` to be positional; `def f(a, *, b, c)` forces `b` and `c` to be keyword-only. Neither of these forms is required for an ordinary function to already accept both calling styles.

**Where this matters later.** Keyword arguments are common in ML APIs, where functions often have many configuration parameters.

## Explanation

None of these three functions restricts its parameters with `/` or `*` — an ordinary `def` already accepts positional calls, all-keyword calls, and any valid mix of the two, since Python's default parameter-matching rules (position first, then name) apply automatically. The functions exist to prove that fact with real calling-convention tests, not to add code that enables it.
