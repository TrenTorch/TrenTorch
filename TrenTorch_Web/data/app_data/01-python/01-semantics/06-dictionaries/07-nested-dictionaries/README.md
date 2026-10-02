---
name: python-dicts-nested-dictionaries
title: Nested Dictionaries
tags: [python-dicts, nested-structures]
difficulty: Advanced
---

## Statement

Implement functions that read, write, and flatten dictionaries whose values are themselves dictionaries, creating intermediate levels as needed.

## Theory

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

**Key paths.** A sequence of keys such as `["model", "layers"]` identifies one value at depth — reading or writing along a path means stepping into one inner dictionary per key.

**Where this matters later.** Model and training configurations, JSON documents, and checkpoint metadata are nested dictionaries.

## Explanation

`nested_get` walks `path` one key at a time with a plain loop rather than chained `.get()` calls, since the number of levels is only known at runtime (`path` is an arbitrary-length list) — at each step it checks both "is this a dict" and "is the key present" before descending, since either failure means the spec's `default` return, not a crash. `nested_set` walks all but the last key of `path`, using `setdefault(key, {})`-style creation at each level (replacing a non-dict value found along the way, per the spec), then assigns the final key directly — building the missing scaffolding exactly one level at a time as it goes, never assuming any level already exists.
