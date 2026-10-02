---
name: python-dicts-objects-key-lookup
title: Dictionary Objects and How Key Lookup Works
tags: [python-dicts, hashing]
difficulty: Intermediate
---

## Statement

Implement functions that build dictionaries from data and test whether two objects would occupy the same key, exposing the equality and hashing rules that govern lookup.

## Theory

A **dictionary** is a **mutable** object that stores **entries**, each associating one **key** with one **value**. Given a key, it returns its value without examining other entries.

The rules:

- **Keys are unique.** Storing a second value under an equal key replaces the first.
- **Keys must be hashable**: immutable objects whose contents, if any, are also hashable.
- **Values can be any object**, including mutable ones.
- **Entries keep insertion order.**

**How a lookup works.** Compute `hash(key)`, use it to find a starting slot, and if occupied, compare the stored hash then the stored key (identity or equality) against the lookup key. The number of slots examined stays small on average regardless of dictionary size — lookup, insertion, and removal take about the same time whether the dictionary has ten entries or ten million, unlike scanning a list.

**Equal keys are the same key.** Keys are matched by hash and equality, not by type. Since `1 == 1.0 == True` (and their hashes are equal too), they are one key:

```python
d = {}
d[1] = "int"
d[1.0] = "float"     # replaces the value; the original key object 1 stays in place
print(d)             # {1: "float"}
```

**Reading a missing key** with `d[key]` raises `KeyError`. `key in d` tests without raising.

**Where this matters later.** Dictionaries hold model configurations, vocabularies, and parameter collections such as a model's `state_dict`.

## Explanation

`same_key` checks `hash(a) == hash(b) and a == b` — both conditions, not either alone, since two hashable objects could theoretically share a hash by coincidence without being equal (a hash collision), and the dictionary's own matching rule requires both. `distinct_key_count` builds a real dictionary and reads `len()` off it afterward rather than trying to count distinct values some other way, since that's the most direct way to let Python's own key-equality rules (not a hand-rolled one) decide what counts as "distinct."
