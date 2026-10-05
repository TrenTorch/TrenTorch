---
name: python-lists-comprehensions
title: Comprehensions
tags: [python-lists, comprehensions, python-numpy-bridge]
difficulty: Intermediate
---

## Statement

Implement functions that build lists from other iterables using comprehensions, including filters, conditional values and nested loops, then express whole-collection operations (element-wise application, masking, broadcasting and normalization) with comprehensions and `zip`, mirroring how vectorized array operations are written.

## Theory

### List comprehensions

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

**Where this matters later.** Comprehensions state _what_ the new list contains rather than the steps to fill it, the same "describe the whole result from the whole input" style vectorized array code expresses.

### Comprehensions as vectorized thinking

Comprehensions, functions as values, and `map`/`filter` together express a way of thinking: describe **what the result is for the whole collection**, instead of writing the steps to fill it in position by position.

| Whole-collection idea | Comprehension form                         | Array-library form        |
| --------------------- | ------------------------------------------ | ------------------------- |
| Element-wise map      | `[f(x) for x in xs]`                       | `f(arr)`                  |
| Combine positions     | `[a + b for a, b in zip(xs, ys)]`          | `xs + ys`                 |
| Mask selection        | `[x for x, keep in zip(xs, mask) if keep]` | `arr[mask]`               |
| Reduction             | `sum(xs)`, `sum(xs) / len(xs)`             | `arr.sum()`, `arr.mean()` |
| Broadcasting          | `[x + 1 for x in xs]`                      | `arr + 1`                 |

**Broadcasting** treats a single number as if repeated to match the collection's length. The duck-typing test `hasattr(other, "__len__")` is a direct way to tell a scalar from a sequence.

**Normalization** rescales a vector to zero mean and unit variance:

$$\mu = \frac{1}{n}\sum x_i \qquad \sigma^2 = \frac{1}{n}\sum(x_i - \mu)^2 \qquad \hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}$$

$\epsilon$ prevents division by zero when all values are equal. This is two reductions (mean, then mean of squared differences) plus one element-wise map broadcasting the two scalars $\mu$ and $\sigma^2 + \epsilon$ against every element.

**What a comprehension does not change.** It's still an interpreted loop, writing code in this style just makes the translation to array operations mechanical.

**Where this matters later.** Layer normalization's forward pass has exactly this shape: a mean, a variance and a broadcasted element-wise expression.

## Explanation

`squares_of_evens` puts its `if` _after_ the `for` (a filter, possibly shortening the result), while `label_parity` puts its conditional _before_ the `for` (a value choice, always as long as the input), these are the two syntactic positions the theory distinguishes, and using the wrong one for either function would either produce the wrong length or fail to filter at all. `flatten` uses one comprehension with two `for` clauses (`for row in nested for x in row`) rather than a nested comprehension, since flattening one level only needs to iterate the outer list once and each inner list once, not build an intermediate list of lists.

`elementwise` uses `zip(*vectors)`, unpacking the variable number of input lists into `zip`'s own arguments, so it naturally stops at the shortest input and works for any number of vectors (including zero, where `zip()` with no arguments yields nothing and the comprehension produces `[]`). `broadcast_add` checks `hasattr(other, "__len__")` to decide scalar vs. sequence rather than `isinstance(other, list)`, which is exactly the duck-typing test from the previous topic and is what lets a tuple or another sequence type work as `other` too. `normalize` computes `mean` and `variance` as two separate reduction passes before the final comprehension, since the element-wise formula needs both finished scalars already in hand, it can't be done in a single pass over `values`.
