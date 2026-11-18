---
name: sheet-allocate-books
title: 'Allocate Books'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Advanced
theory: splitting-books-fairly
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

## Explanation

If there are fewer books than students, no valid split exists: `-1`. Otherwise `lo = max(pages)`, `hi = sum(pages)`. For a guess `mid`, count the students needed with the greedy rule. If the count is at most `students` the guess works: `hi = mid`; otherwise `lo = mid + 1`.

### Complexity

- Time: O(n log S). Binary search over the page limit up to the total `S` costs `log S` probes, and each probe scans `n` books.
- Space: O(1). A few counters.
