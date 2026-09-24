---
name: python-lists-list-comprehensions
title: List Comprehensions
tags: [python-lists, comprehensions]
difficulty: Intermediate
---

## Statement

Implement functions that build lists from other iterables using comprehensions, including filters, conditional values, and nested loops.

## Theory

A **list comprehension** builds a new list in a single expression: `[expression for variable in iterable]`, equivalent to a loop that appends `expression` for each `variable`.

```python
[n * n for n in [1, 2, 3]]          # [1, 4, 9]
```

**`range`.** `range(stop)` produces `0, 1, ..., stop - 1`. `range(start, stop, step)` follows slicing rules.

**Filtering.** An `if` after the `for` clause keeps only elements for which the condition is truthy:

```python
[n for n in range(10) if n % 2 == 0]      # [0, 2, 4, 6, 8]
```

**Conditional values.** To choose between two values for each element, use `value_if_true if condition else value_if_false` _before_ the `for` (it always needs an `else`):

```python
["even" if n % 2 == 0 else "odd" for n in range(4)]   # ["even", "odd", "even", "odd"]
```

The position matters: `if` after `for` filters (may shorten the result); `if ... else` before `for` chooses a value (result length equals input length).

**Nested loops.** Multiple `for` clauses run like nested loops, with the **first** `for` as the outermost:

```python
[x for row in [[1, 2], [3]] for x in row]         # [1, 2, 3]   flattening
```

**Scope.** The loop variable of a comprehension exists only inside it.

**Where this matters later.** Comprehensions state _what_ the new list contains rather than the steps to fill it — the same "describe the whole result from the whole input" style vectorized array code expresses.

## Explanation

`squares_of_evens` puts its `if` _after_ the `for` (a filter, possibly shortening the result), while `label_parity` puts its conditional _before_ the `for` (a value choice, always as long as the input) — these are the two syntactic positions the theory distinguishes, and using the wrong one for either function would either produce the wrong length or fail to filter at all. `flatten` uses one comprehension with two `for` clauses (`for row in nested for x in row`) rather than a nested comprehension, since flattening one level only needs to iterate the outer list once and each inner list once, not build an intermediate list of lists.
