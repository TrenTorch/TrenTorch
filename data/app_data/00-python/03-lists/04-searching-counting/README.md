---
name: python-lists-searching-counting
title: 'Searching and Counting: index, count, in'
tags: [python-lists, searching]
difficulty: Beginner
---

## Statement

Implement functions that locate and count elements in a list, including the difference between equality and identity when searching.

## Theory

| Operation                   | Result                                                     |
| --------------------------- | ---------------------------------------------------------- |
| `x in lst`                  | `True` if some element matches `x`.                        |
| `lst.index(x)`              | Index of the **first** match. `ValueError` if none exists. |
| `lst.index(x, start, stop)` | Same, searching only positions `start` up to `stop`.       |
| `lst.count(x)`              | Number of elements that match `x`.                         |

**What "match" means.** A search compares each element with the target from left to right. For each element it first checks **identity** (`element is target`), and if that is false, checks **equality** (`element == target`). A match is either. Consequences:

- Equal values of different types match: `1 in [1.0]` is `True`, and `True == 1`, so `1 in [True]` is `True`.
- Two separately built lists with the same contents match: `[1, 2] in [[1, 2], [3]]` is `True`.

**Cost.** Every one of these operations may examine every element, so the time grows in proportion to the length of the list. Unlike `str.find`, `list.index` does not return `-1` for absent values — it raises an error.

**Where this matters later.** Repeated `in` tests on large lists become a performance problem in data pipelines; a later module shows how a set removes that cost.

## Explanation

`index_or_minus_one` catches `ValueError` from `list.index()` rather than pre-checking `value in lst` first, which would search the list twice for the common case where the value is present. `contains_same_object` uses `any(x is target for x in lst)` specifically with `is`, not `==`, so a separately-built equal object elsewhere in the list correctly does not count — the same identity-vs-equality distinction the theory calls out.
