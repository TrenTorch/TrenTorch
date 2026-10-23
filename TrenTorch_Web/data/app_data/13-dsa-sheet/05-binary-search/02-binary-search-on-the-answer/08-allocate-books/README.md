---
name: sheet-allocate-books
title: 'Allocate Books'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Advanced
---

## Statement

Books with `pages[i]` pages are in a row. Give each of `students` students a **run of consecutive books**, so that every book goes to exactly one student and every student gets at least one book. Among all ways to do this, return the **smallest possible value of the largest page total** given to any one student.

If there are fewer books than students, return `-1`.

### Examples

**Example 1**

Input:

```python
allocate_books([12, 34, 67, 90], 2)
```

Output:

```text
113
```

Split `12 34 67` (113) and `90`: the largest is 113.

**Example 2**

Input:

```python
allocate_books([10, 20], 3)
```

Output:

```text
-1
```

There are fewer books than students.

### Constraints

- `1 <= len(pages) <= 2 * 10**4`
- `1 <= students <= 2 * 10**4`
- `1 <= pages[i] <= 10**4`
- Trying every limit one by one is too slow for the large tests.

## Theory

This **minimises a maximum**, which again points to binary search on the answer. Fix a limit `L` for the pages one student may read. Greedily give the current student books until the next one would pass `L`, then start the next student. If you need at most `students` students, the limit `L` works, and any bigger `L` works too.

So "limit `L` is enough" goes `False ... False True ... True`; find the first `True`. The limit is at least `max(pages)` (every book must fit) and at most `sum(pages)` (one student reads everything). Each check is `O(n)`, so the total is `O(n log S)`.

The same pattern solves _splitting an array into `k` parts to minimise the largest sum_ and the _painter's partition_ problem: only the story changes.

## Explanation

If there are fewer books than students, no valid split exists: `-1`. Otherwise `lo = max(pages)`, `hi = sum(pages)`. For a guess `mid`, count the students needed with the greedy rule. If the count is at most `students` the guess works: `hi = mid`; otherwise `lo = mid + 1`.
