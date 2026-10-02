---
name: python-dicts-reading-updating
title: 'Creating, Updating & Removing'
tags: [python-dicts, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that create dictionaries in several ways, read keys safely, update values in place, merge dictionaries and insert missing keys with `update()` and `setdefault()` and remove entries while returning the removed data where the operation provides it.

## Theory

### Creating, reading, & updating

**Creating.** `{}`, `{"a": 1}`, `dict(a=1, b=2)`, `dict([("a", 1)])`, `dict.fromkeys(["a", "b"], 0)`. `fromkeys` stores the **same object** under every key, harmless for an immutable value, but an aliasing bug for a mutable one.

**Reading.**

| Expression            | Result                              |
| --------------------- | ----------------------------------- |
| `d[key]`              | The value, or `KeyError` if absent. |
| `d.get(key)`          | The value, or `None` if absent.     |
| `d.get(key, default)` | The value, or `default` if absent.  |
| `key in d`            | `True` if present.                  |

`get` never raises for a missing key and **never inserts** anything. A stored value of `None` and an absent key are indistinguishable through `d.get(key)`, when the difference matters, use `in`.

**Updating.** Assigning to a key does both jobs: if the key is present its value is replaced; if absent, a new entry is added at the end. Assignment mutates the dictionary in place.

A common pattern is read-modify-write, and `get` with a default makes it safe for keys not yet present:

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] = counts.get(word, 0) + 1     # {"a": 2, "b": 1}
```

**Where this matters later.** Counting with `get(key, 0) + 1` is the manual form of building vocabularies and frequency tables for text data.

### update() & setdefault()

**`update`** copies entries from another source into the dictionary, in place and returns `None`. Existing keys have their values **replaced**; new keys are added at the end.

**Merging into a new dictionary.** To combine two dictionaries without changing either, copy one and update the copy, or use `|`, which does this in one expression with the right operand winning on shared keys:

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

Two cautions: the `default` argument is evaluated **every call**, even when the key already exists; and `get(key, default)` reads without inserting, use `get` when the key should _not_ be added.

**Where this matters later.** Applying default settings under user-supplied options (`options.setdefault("lr", 0.001)`) is a standard way to fill in configuration.

### Removing entries

| Operation             | Effect                                                                                                   |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| `d.pop(key)`          | Removes the entry and **returns its value**. `KeyError` if absent.                                       |
| `d.pop(key, default)` | Same, but returns `default` instead of raising when absent.                                              |
| `d.popitem()`         | Removes and returns the **most recently inserted** entry as a `(key, value)` tuple. `KeyError` if empty. |
| `del d[key]`          | Removes the entry. `KeyError` if absent.                                                                 |
| `d.clear()`           | Removes every entry; the dictionary object stays, empty.                                                 |

All of these mutate in place. `d = {}` is reassignment instead, and leaves other variables referring to the old dictionary.

**Removal affects order.** Remaining entries keep their relative order. A key removed and reinserted goes to the **end**.

**Removing while iterating is not allowed**, it raises `RuntimeError`. To remove entries whose keys are already known, no loop over the dictionary is needed.

**Choosing.** `pop(key, default)` to remove _and use_ a value without failing on absence; `del d[key]` when the key must be present; `popitem()` to take entries one at a time from the end.

**Where this matters later.** Removing and reading in one operation is the pattern for consuming configuration options (`options.pop("lr", 0.001)`).

## Explanation

`word_frequencies` uses `counts[word] = counts.get(word, 0) + 1` for every word, the exact read-modify-write pattern the theory names, one line handles both "first time seen" (get returns 0) and "seen before" (get returns the running count) with no separate branch. `increment` uses the same `get(key, 0)` pattern rather than checking `key in d` first, so a present key with the value `0` isn't mistaken for absent.

`merge_prefer_second` copies `a` with `dict(a)` and calls `.update(b)` on that copy, per the spec's own instruction, never `a | b`, which the spec doesn't ask for here, and never mutating `a` directly, which would violate "neither may be modified." `group_by_first_letter` calls `.setdefault(letter, []).append(word)` in one line, letting `setdefault` both create the list on first sight of a letter and return the existing one on every later sight, the same grouping idiom the theory names, which is also why each letter's list ends up a genuinely separate object (never shared) with no extra code needed.

`remove_keys` checks `key in d` before calling `del`, since `keys` may contain duplicates or entries already absent, and `del` on a missing key raises, checking first (rather than catching the exception) also makes counting successful removals a direct increment. `take_last` handles the empty case as an explicit early return before calling `popitem()`, since that method raises on an empty dictionary and the spec calls for `None` instead. `remove_and_return` needs no such branch: `pop(key, default)` already returns `default` for a missing key without raising, which is exactly the built-in behavior the spec asks for.
