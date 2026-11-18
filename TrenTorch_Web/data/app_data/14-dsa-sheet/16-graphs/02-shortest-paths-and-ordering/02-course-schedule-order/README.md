---
name: sheet-course-schedule-order
title: 'Course Order'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Advanced
theory: the-smallest-order-first
---

## Statement

As in the previous question, a pair `[a, b]` means course `b` must be taken before course `a`. Return an **order in which all courses can be taken**. Many orders may exist; return the **lexicographically smallest** one (compare the first course, then the second, and so on). If it is impossible, return an empty list.

For `num_courses = 4` and `prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]` the answer is `[0, 1, 2, 3]`.

### Examples

**Example 1**

Input:

```python
find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
```

Output:

```text
[0, 1, 2, 3]
```

**Example 2**

Input:

```python
find_order(2, [[0, 1], [1, 0]])
```

Output:

```text
[]
```

### Constraints

- `0 <= num_courses <= 100000`
- `0 <= len(prerequisites) <= 200000`

## Explanation

The heap holds the courses whose prerequisites are all taken. Popping the smallest gives the lexicographically smallest valid order.

### Complexity

- Time: O((n + e) log n). Kahn's algorithm with a heap, so that the smallest available course is taken first.
- Space: O(n + e). The adjacency lists, the in-degrees and the heap.
