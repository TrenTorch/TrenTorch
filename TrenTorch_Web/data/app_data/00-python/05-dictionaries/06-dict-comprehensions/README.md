---
name: python-dicts-comprehensions
title: Dictionary Comprehensions
tags: [python-dicts, comprehensions]
difficulty: Intermediate
---

## Statement

Implement functions that build dictionaries from other data with comprehensions, including filters, inversion, and pairing two parallel lists with `zip`.

## Theory

A **dictionary comprehension** builds a new dictionary in one expression: `{key_expression: value_expression for variable in iterable}`.

```python
{n: n * n for n in range(1, 4)}                 # {1: 1, 2: 4, 3: 9}
```

**Filtering** works as in list comprehensions: an `if` after the `for` clause keeps only matching items.

**Transforming a dictionary.** Iterate over `items()` and unpack:

```python
prices = {"apple": 2, "pear": 3}
{v: k for k, v in prices.items()}           # inverted: {2: "apple", 3: "pear"}
```

When inverting, values become keys, so they must be hashable and **unique** — if two keys share a value, the **later** entry overwrites the earlier one, and one key is lost. The same rule applies to any duplicate key produced by a comprehension: the last value assigned wins.

**Pairing with `zip`.** `zip(a, b)` produces pairs `(a[0], b[0])`, ..., stopping at the end of the **shorter** input:

```python
dict(zip(["a", "b"], [1, 2]))                # {"a": 1, "b": 2}
```

**Where this matters later.** Building a lookup table (token to ID, and its inverse) is a two-line dictionary comprehension.

## Explanation

`invert` iterates `d.items()` in `d`'s own insertion order and writes `{v: k for k, v in d.items()}` — since a comprehension assigns each key exactly once as encountered and a later assignment to an equal key overwrites the earlier one, iterating in `d`'s natural order automatically makes "the key that appears later in `d`" the one that survives, with no extra bookkeeping. `dict_from_parallel` pairs with `zip(keys, values)` rather than an index loop over `range(len(keys))`, since `zip` already stops at the shorter input on its own, which is exactly the "ignore the extra elements of the longer list" behavior the spec asks for.
