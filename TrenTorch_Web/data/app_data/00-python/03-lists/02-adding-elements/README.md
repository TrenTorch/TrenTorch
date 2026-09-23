---
name: python-lists-adding-elements
title: "Adding Elements: append, extend, insert"
tags: [python-lists]
difficulty: Beginner
---

## Statement

Implement functions that grow a list in place and demonstrate the difference between operations that mutate a list and operations that build a new one.

## Theory

Three methods add elements to an existing list, all mutating in place and returning `None`.

| Method | Effect |
|---|---|
| `lst.append(x)` | Adds **one** element, `x`, at the end. |
| `lst.extend(iterable)` | Adds **each element** of `iterable` at the end. |
| `lst.insert(i, x)` | Inserts `x` before position `i`, shifting later elements right. |

**`append` vs `extend`.** `append` always adds exactly one element, even if that element is itself a list. `extend` unpacks its argument and adds its elements one by one:

```python
a = [1]
a.append([2, 3])       # [1, [2, 3]]      one new element: a list
b = [1]
b.extend([2, 3])       # [1, 2, 3]        two new elements
```

**`insert` and indices.** `insert` uses slice-style bounds: an index at or beyond `len(lst)` appends, and a negative index counts from the end.

**`+` and `+=`.** `lst + other` builds a **new list**; neither operand changes. `lst += other` is a **mutation** — it behaves like `lst.extend(other)` and the list keeps its address.

```python
x = [1, 2]
before = id(x)
x += [3]                 # in place: id(x) == before
x = x + [4]              # new list: id(x) != before, and x is reassigned
```

**Methods return `None`.** Because these methods mutate, they return `None`. Writing `x = x.append(3)` reassigns `x` to `None` and loses the list.

**Where this matters later.** Growing a list with `append` inside a loop and then converting it to an array is the standard way to collect per-step results (losses, predictions) in training code.

## Explanation

`insert_sorted` scans forward with `while i < len(lst) and lst[i] <= value: i += 1` — advancing past elements *equal* to `value`, not just less than it — which is exactly what places a new equal element after all existing ones, matching the spec's explicit "after any existing elements equal to value." `concat_identity_report` relies on `lst += extra` mutating the caller's actual list object, then `lst = lst + extra` only repointing this function's own local name afterward — the caller never sees that second reassignment, which is the point being demonstrated.
