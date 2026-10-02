---
name: python-dicts-creating-reading-updating
title: 'Creating, Reading, and Updating; get() and Defaults'
tags: [python-dicts]
difficulty: Beginner
---

## Statement

Implement functions that create dictionaries in several ways, read keys safely, and update values in place.

## Theory

**Creating.** `{}`, `{"a": 1}`, `dict(a=1, b=2)`, `dict([("a", 1)])`, `dict.fromkeys(["a", "b"], 0)`. `fromkeys` stores the **same object** under every key — harmless for an immutable value, but an aliasing bug for a mutable one.

**Reading.**

| Expression            | Result                              |
| --------------------- | ----------------------------------- |
| `d[key]`              | The value, or `KeyError` if absent. |
| `d.get(key)`          | The value, or `None` if absent.     |
| `d.get(key, default)` | The value, or `default` if absent.  |
| `key in d`            | `True` if present.                  |

`get` never raises for a missing key and **never inserts** anything. A stored value of `None` and an absent key are indistinguishable through `d.get(key)` — when the difference matters, use `in`.

**Updating.** Assigning to a key does both jobs: if the key is present its value is replaced; if absent, a new entry is added at the end. Assignment mutates the dictionary in place.

A common pattern is read-modify-write, and `get` with a default makes it safe for keys not yet present:

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] = counts.get(word, 0) + 1     # {"a": 2, "b": 1}
```

**Where this matters later.** Counting with `get(key, 0) + 1` is the manual form of building vocabularies and frequency tables for text data.

## Explanation

`word_frequencies` uses `counts[word] = counts.get(word, 0) + 1` for every word, the exact read-modify-write pattern the theory names — one line handles both "first time seen" (get returns 0) and "seen before" (get returns the running count) with no separate branch. `increment` uses the same `get(key, 0)` pattern rather than checking `key in d` first, so a present key with the value `0` isn't mistaken for absent.
