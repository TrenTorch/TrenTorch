---
name: python-truthy-falsy
title: Truthy and Falsy Values
tags: [python-core, control-flow]
difficulty: Beginner
---

## Statement

Implement a function that determines, for a variety of values, whether Python treats them as true or false in a boolean context — without converting them to actual booleans first.

## Theory

Every object in Python can be evaluated in a boolean context — inside an `if`, a `while`, or a call to `bool()` — even if it isn't literally `True` or `False`. Python has fixed rules for which values count as false:

**Falsy values** (everything else is truthy):

- `False`
- `None`
- `0`, `0.0` (zero of any numeric type)
- `""` (empty string)
- `[]` (empty list)
- `()` (empty tuple)
- `{}` (empty dict)
- `set()` (empty set)

Every other value — including any non-empty string, non-empty list, non-zero number (even negative ones), and any object instance without special configuration — is truthy.

```python
if []:
    print("won't run — empty list is falsy")

if [0]:
    print("will run — this list has one element, so it's truthy,")
    print("even though that element (0) is itself falsy")
```

This matters because it lets conditions be written directly on a value, without explicitly comparing it to something:

```python
def process(items):
    if items:          # true only if items is non-empty
        ...
```

`bool(x)` converts any value `x` to its actual `True`/`False` equivalent using these same rules.

```python
bool([])       # False
bool([0])      # True
bool("")       # False
bool("0")      # True — a non-empty string, even one that looks like zero
```

Note the last example carefully: the string `"0"` is truthy, because it's a non-empty string — its _content_ looking like the number zero is irrelevant to truthiness rules, which only check emptiness/zero-ness of the object itself.

## Explanation

`is_truthy` checks each category explicitly (numeric zero, empty string, empty list/tuple/dict/set, `None`, `False`) rather than delegating to `bool(value)` — the exercise is to internalize the actual rule set the theory lists, not just to call the built-in that already implements it. `first_truthy` scans with an explicit loop and an `is_truthy`-style check per element rather than `any()`, since `any()` would hide the exact same logic this question is meant to practice.
