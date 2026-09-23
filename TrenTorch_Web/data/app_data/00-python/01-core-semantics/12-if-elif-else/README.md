---
name: python-if-elif-else
title: if / elif / else
tags: [python-core, control-flow]
difficulty: Beginner
---

## Statement

Implement a function using a full `if` / `elif` / `else` chain to classify a numeric input, establishing exactly how Python evaluates conditional branches.

## Theory

An `if` statement evaluates an expression and, if that expression is `True`, runs the indented block beneath it. Python decides indentation (not braces or keywords) marks which statements belong to which block.

```python
if condition:
    # runs only if condition is True
```

`elif` (short for "else if") is checked only if every condition above it was `False`. Python evaluates conditions top to bottom and stops at the **first** one that's `True` — none of the conditions after it are even evaluated, and only that one block runs.

```python
if condition_a:
    ...
elif condition_b:
    ...
elif condition_c:
    ...
else:
    ...
```

If `condition_a` is `True`, only that block runs — `condition_b` and `condition_c` are never checked, even if they would also have been `True`. `else` runs only if every condition above it was `False`; it takes no condition itself.

Each `if`/`elif`/`else` chain is a single structure — exactly one of its blocks runs (or none, if there's no `else` and every condition was `False`). This is different from writing several separate `if` statements in a row, where each one is evaluated independently regardless of what the others decided.

```python
# a chain: only one branch runs
if x > 10:
    print("big")
elif x > 5:
    print("medium")

# separate ifs: both can run
if x > 10:
    print("big")
if x > 5:
    print("also at least medium")
```

Conditions can be any expression that evaluates to `True` or `False` — comparisons (`x > 5`), boolean combinations (`x > 5 and x < 10`), or values checked for truthiness directly (covered in the next topic).

## Explanation

`classify_number` checks the four cases in a single `if`/`elif`/`elif`/`elif` chain, in the exact order the boundaries require: `x < 0` first (so `0` never gets accidentally classified as negative), then `x == 0` before the range check (so `0` doesn't fall into `"small"`'s `0 < x <= 10` range, which correctly excludes it), then the two remaining ranges. Writing this as separate `if` statements instead of a chain would risk more than one branch's `print`/return firing for a boundary value.
