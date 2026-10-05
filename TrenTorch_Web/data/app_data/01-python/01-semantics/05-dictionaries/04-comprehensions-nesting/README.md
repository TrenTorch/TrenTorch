---
name: python-dicts-comprehensions-nesting
title: 'Comprehensions & Nesting'
tags: [python-dicts, comprehensions, nested-structures]
difficulty: Advanced
---

## Statement

Implement functions that build dictionaries from other data with comprehensions, including filters, inversion and pairing two parallel lists with `zip` and that read, write and flatten dictionaries whose values are themselves dictionaries.

## Theory

### Dictionary comprehensions

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

When inverting, values become keys, so they must be hashable and **unique**, if two keys share a value, the **later** entry overwrites the earlier one and one key is lost. The same rule applies to any duplicate key produced by a comprehension: the last value assigned wins.

**Pairing with `zip`.** `zip(a, b)` produces pairs `(a[0], b[0])`, ..., stopping at the end of the **shorter** input:

```python
dict(zip(["a", "b"], [1, 2]))                # {"a": 1, "b": 2}
```

**Where this matters later.** Building a lookup table (token to ID, and its inverse) is a two-line dictionary comprehension.

### Nested dictionaries

A **nested dictionary** is a dictionary whose values include other dictionaries, describing hierarchical data:

```python
config = {"model": {"layers": 4, "dropout": 0.1}, "train": {"lr": 0.001}}
config["model"]["layers"]       # 4
```

**Reading safely.** A missing key at any level raises `KeyError`. Chained `get` calls with an empty dictionary as the default avoid it: `config.get("data", {}).get("path")`.

**Writing.** Assigning at depth requires the intermediate dictionaries to exist: `config["data"]["path"] = "x"` raises `KeyError` if `"data"` is missing. `config.setdefault("data", {})["path"] = "x"` creates the level first, then assigns.

**Iterating two levels.**

```python
for group, inner in config.items():
    for key, value in inner.items():
        ...
```

**Aliasing.** Inner dictionaries are separate mutable objects. A shallow copy of the outer dictionary shares every inner dictionary. `copy.deepcopy` produces fully independent inner dictionaries.

**Key paths.** A sequence of keys such as `["model", "layers"]` identifies one value at depth, reading or writing along a path means stepping into one inner dictionary per key.

**Where this matters later.** Model and training configurations, JSON documents, and checkpoint metadata are nested dictionaries.

## Explanation

`invert` iterates `d.items()` in `d`'s own insertion order and writes `{v: k for k, v in d.items()}`, since a comprehension assigns each key exactly once as encountered and a later assignment to an equal key overwrites the earlier one, iterating in `d`'s natural order automatically makes "the key that appears later in `d`" the one that survives, with no extra bookkeeping. `dict_from_parallel` pairs with `zip(keys, values)` rather than an index loop over `range(len(keys))`, since `zip` already stops at the shorter input on its own, which is exactly the "ignore the extra elements of the longer list" behavior the spec asks for.

`nested_get` walks `path` one key at a time with a plain loop rather than chained `.get()` calls, since the number of levels is only known at runtime (`path` is an arbitrary-length list), at each step it checks both "is this a dict" and "is the key present" before descending, since either failure means the spec's `default` return, not a crash. `nested_set` walks all but the last key of `path`, using `setdefault(key, {})`-style creation at each level (replacing a non-dict value found along the way, per the spec), then assigns the final key directly, building the missing scaffolding exactly one level at a time as it goes, never assuming any level already exists.
