---
name: sheet-distinct-permutations
title: 'Distinct Permutations'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
---

## Statement

Return every different arrangement (permutation) of the characters of `s`, as strings, in alphabetical (lexicographic) order. If `s` has repeated characters, an arrangement that looks the same must be listed only once.

### Examples

**Example 1**

Input:

```python
distinct_permutations('abc')
```

Output:

```text
['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
```

**Example 2**

Input:

```python
distinct_permutations('aab')
```

Output:

```text
['aab', 'aba', 'baa']
```

### Constraints

- `0 <= len(s) <= 8`
- `s` contains only lower-case letters.

## Theory

`itertools.permutations(s)` yields every ordering of the characters as tuples. With repeated letters it yields the same string more than once, because it treats positions as different, not values. A `set` removes the duplicates and `sorted` puts them in order.

The number of results is `n!` at most: 8 letters give 40,320. Past about 10 letters the count explodes, which is why constraints on permutation problems are always small.

## Explanation

`{"".join(p) for p in permutations(s)}` builds each arrangement as a string and the set keeps one copy of each. `sorted(...)` returns them in order. An empty `s` has exactly one arrangement, the empty string.
