---
name: python-lists-ordering-sort
title: 'Ordering: sort, sorted, reverse, and sort keys'
tags: [python-lists, sorting]
difficulty: Intermediate
---

## Statement

Implement functions that order lists in place and by producing new lists, using custom sort keys and relying on sort stability.

## Theory

| Form               | Effect                                 | Returns      |
| ------------------ | -------------------------------------- | ------------ |
| `lst.sort()`       | Reorders `lst` **in place**            | `None`       |
| `sorted(iterable)` | Builds a **new list**; input untouched | the new list |

The most common bug is `nums = nums.sort()`, which reassigns `nums` to `None` and loses the list.

Both accept `reverse=True` (descending order) and `key=function`, which calls `function` once per element and orders by the values it returns:

```python
words = ["pear", "fig", "apple"]
sorted(words, key=len)           # ["fig", "pear", "apple"]
sorted([-3, 1, -2], key=abs)     # [1, -2, -3]
```

**Stability.** Python's sort is **stable**: elements whose keys compare equal keep their original relative order. This makes multi-level sorting possible by sorting repeatedly, least important key first, and stability holds with `reverse=True` too.

**Reversing.** `lst.reverse()` reverses in place, returning `None`. `reversed(lst)` returns an iterator, which `list()` turns into a new list. `lst[::-1]` also builds a new reversed list.

**Ordering rules.** `<` decides order; values that can't be compared (an `int` and a `str`) raise `TypeError`. Strings compare by code point.

**Where this matters later.** Sorting with a key is how top-k results and ranked predictions are produced in ML code.

## Explanation

`sorted_desc_copy` uses `sorted(lst, reverse=True)`, never `lst.sort(reverse=True)`, since the spec requires the input untouched — `sorted()` is the form that returns a new list rather than mutating. `last_char` returns `""` for an empty string rather than raising on `word[-1]`, so it can safely serve as a sort key for a list that might contain an empty string, sorting it first (an empty key compares less than any non-empty one).
