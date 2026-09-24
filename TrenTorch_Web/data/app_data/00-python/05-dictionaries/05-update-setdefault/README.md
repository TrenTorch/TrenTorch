---
name: python-dicts-update-setdefault
title: update() and setdefault()
tags: [python-dicts]
difficulty: Intermediate
---

## Statement

Implement functions that merge dictionaries and insert missing keys, using `update()` and `setdefault()` and choosing correctly between mutating and building a new dictionary.

## Theory

**`update`** copies entries from another source into the dictionary, in place, and returns `None`. Existing keys have their values **replaced**; new keys are added at the end.

**Merging into a new dictionary.** To combine two dictionaries without changing either, copy one and update the copy — or use `|`, which does this in one expression with the right operand winning on shared keys:

```python
merged = a | b            # new dictionary; a and b unchanged
```

Both copies are **shallow**: values are shared between source and result.

**`setdefault(key, default)`** returns the value for `key` if present. If absent, it **inserts** `key` with `default` and returns `default`. Unlike `get`, it modifies the dictionary. Its most common use is **grouping**:

```python
groups = {}
for word in ["apple", "avocado", "banana"]:
    groups.setdefault(word[0], []).append(word)
# {"a": ["apple", "avocado"], "b": ["banana"]}
```

Two cautions: the `default` argument is evaluated **every call**, even when the key already exists; and `get(key, default)` reads without inserting — use `get` when the key should *not* be added.

**Where this matters later.** Applying default settings under user-supplied options (`options.setdefault("lr", 0.001)`) is a standard way to fill in configuration.

## Explanation

`merge_prefer_second` copies `a` with `dict(a)` and calls `.update(b)` on that copy, per the spec's own instruction — never `a | b`, which the spec doesn't ask for here, and never mutating `a` directly, which would violate "neither may be modified." `group_by_first_letter` calls `.setdefault(letter, []).append(word)` in one line, letting `setdefault` both create the list on first sight of a letter and return the existing one on every later sight — the same grouping idiom the theory names, which is also why each letter's list ends up a genuinely separate object (never shared) with no extra code needed.
