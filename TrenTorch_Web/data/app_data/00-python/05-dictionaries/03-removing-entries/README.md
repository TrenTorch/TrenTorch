---
name: python-dicts-removing-entries
title: 'Removing Entries: pop, popitem, del, clear'
tags: [python-dicts, mutation]
difficulty: Intermediate
---

## Statement

Implement functions that remove entries from a dictionary in place and return the removed data where the operation provides it.

## Theory

| Operation             | Effect                                                                                                   |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| `d.pop(key)`          | Removes the entry and **returns its value**. `KeyError` if absent.                                       |
| `d.pop(key, default)` | Same, but returns `default` instead of raising when absent.                                              |
| `d.popitem()`         | Removes and returns the **most recently inserted** entry as a `(key, value)` tuple. `KeyError` if empty. |
| `del d[key]`          | Removes the entry. `KeyError` if absent.                                                                 |
| `d.clear()`           | Removes every entry; the dictionary object stays, empty.                                                 |

All of these mutate in place. `d = {}` is reassignment instead, and leaves other variables referring to the old dictionary.

**Removal affects order.** Remaining entries keep their relative order. A key removed and reinserted goes to the **end**.

**Removing while iterating is not allowed** — it raises `RuntimeError`. To remove entries whose keys are already known, no loop over the dictionary is needed.

**Choosing.** `pop(key, default)` to remove _and use_ a value without failing on absence; `del d[key]` when the key must be present; `popitem()` to take entries one at a time from the end.

**Where this matters later.** Removing and reading in one operation is the pattern for consuming configuration options (`options.pop("lr", 0.001)`).

## Explanation

`remove_keys` checks `key in d` before calling `del`, since `keys` may contain duplicates or entries already absent, and `del` on a missing key raises — checking first (rather than catching the exception) also makes counting successful removals a direct increment. `take_last` handles the empty case as an explicit early return before calling `popitem()`, since that method raises on an empty dictionary and the spec calls for `None` instead. `remove_and_return` needs no such branch: `pop(key, default)` already returns `default` for a missing key without raising, which is exactly the built-in behavior the spec asks for.
