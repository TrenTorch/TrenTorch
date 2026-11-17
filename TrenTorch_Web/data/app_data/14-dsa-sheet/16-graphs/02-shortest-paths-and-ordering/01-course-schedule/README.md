---
name: sheet-course-schedule
title: 'Course Schedule'
tags: [dsa-sheet, graphs, shortest-paths-and-ordering]
difficulty: Intermediate
theory: course-schedule
---

## Statement

There are `num_courses` courses numbered `0` to `num_courses - 1`. A pair `[a, b]` in `prerequisites` means you must take course `b` **before** course `a`. Return `True` if it is possible to take **all** the courses.

For `num_courses = 2` and `prerequisites = [[1, 0]]` the answer is `True`; with `[[1, 0], [0, 1]]` it is `False`.

### Examples

**Example 1**

Input:

```python
can_finish(2, [[1, 0]])
```

Output:

```text
True
```

**Example 2**

Input:

```python
can_finish(2, [[1, 0], [0, 1]])
```

Output:

```text
False
```

### Constraints

- `0 <= num_courses <= 100000`
- `0 <= len(prerequisites) <= 200000`

## Explanation

`taken` counts the courses removed from the queue. It equals `num_courses` exactly when the graph has no cycle.

### Complexity

- Time: O(n + e). Kahn's algorithm removes each node and edge once.
- Space: O(n + e). The adjacency lists, the in-degrees and the queue.
