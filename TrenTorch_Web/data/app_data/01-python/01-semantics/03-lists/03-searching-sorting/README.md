---
name: python-lists-searching-sorting
title: 'Searching, Counting & Sorting'
tags: [python-lists, searching, sorting]
difficulty: Intermediate
---

## Statement

Implement functions that locate and count elements in a list, including the difference between equality and identity when searching and that order lists in place and by producing new lists, using custom sort keys and relying on sort stability.

## Theory

### Searching & counting: index, count, in

| Operation                   | Result                                                     |
| --------------------------- | ---------------------------------------------------------- |
| `x in lst`                  | `True` if some element matches `x`.                        |
| `lst.index(x)`              | Index of the **first** match. `ValueError` if none exists. |
| `lst.index(x, start, stop)` | Same, searching only positions `start` up to `stop`.       |
| `lst.count(x)`              | Number of elements that match `x`.                         |

**What "match" means.** A search compares each element with the target from left to right. For each element it first checks **identity** (`element is target`), and if that is false, checks **equality** (`element == target`). A match is either. Consequences:

- Equal values of different types match: `1 in [1.0]` is `True`, and `True == 1`, so `1 in [True]` is `True`.
- Two separately built lists with the same contents match: `[1, 2] in [[1, 2], [3]]` is `True`.

**Cost.** Every one of these operations may examine every element, so the time grows in proportion to the length of the list. Unlike `str.find`, `list.index` does not return `-1` for absent values, it raises an error.

**Where this matters later.** Repeated `in` tests on large lists become a performance problem in data pipelines; a later module shows how a set removes that cost.

### Ordering: sort, sorted, reverse, & sort keys

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

`index_or_minus_one` catches `ValueError` from `list.index()` rather than pre-checking `value in lst` first, which would search the list twice for the common case where the value is present. `contains_same_object` uses `any(x is target for x in lst)` specifically with `is`, not `==`, so a separately-built equal object elsewhere in the list correctly does not count, the same identity-vs-equality distinction the theory calls out.

`sorted_desc_copy` uses `sorted(lst, reverse=True)`, never `lst.sort(reverse=True)`, since the spec requires the input untouched, `sorted()` is the form that returns a new list rather than mutating. `last_char` returns `""` for an empty string rather than raising on `word[-1]`, so it can safely serve as a sort key for a list that might contain an empty string, sorting it first (an empty key compares less than any non-empty one).
