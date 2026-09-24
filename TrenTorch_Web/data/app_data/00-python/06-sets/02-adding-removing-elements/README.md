---
name: python-sets-adding-removing-elements
title: Adding and Removing Elements
tags: [python-set-mutation]
difficulty: Beginner
---

## Statement

Implement functions that add and remove elements from sets using `add`, `remove`, `discard`, `pop`, and `clear`. The key distinction is whether an operation requires the element to exist before it can be removed.

## Theory

| Method | Effect | Returns |
|---|---|---|
| `add(x)` | Inserts `x`; no effect if already present. | `None` |
| `remove(x)` | Removes `x`; `KeyError` if absent. | `None` |
| `discard(x)` | Removes `x` if present; otherwise does nothing. | `None` |
| `pop()` | Removes and returns an *arbitrary* element; `KeyError` if empty. | the removed element |
| `clear()` | Removes every element; the set object stays, empty. | `None` |

The distinction between `remove` and `discard`:

```text
remove(x)   -> remove it; error if absent
discard(x)  -> remove it if present; otherwise do nothing
```

Use `remove` when the program expects the element to exist (absence is a bug); use `discard` when the desired end state is simply "the element should not be present."

`clear()` empties the *existing* set object — a second variable referring to the same set sees it become empty too, unlike `s = set()`, which only repoints one variable.

**Where this matters later.** Set mutation maintains state such as visited nodes, processed IDs, or active features — and the mutation-vs-reassignment distinction is the same one from the very first module, applied here to sets.

## Explanation

`add_values` builds `set(values)` first rather than mutating the caller's `values` directly, since the spec requires the original untouched — the copy is the new set that gets mutated with `.add()` for each addition. `remove_if_present` uses `discard`, never `remove`, specifically because the spec calls for no exception on an absent value; `remove_required` uses `remove` specifically because the spec wants the `KeyError` to propagate when the value is genuinely expected to exist.
