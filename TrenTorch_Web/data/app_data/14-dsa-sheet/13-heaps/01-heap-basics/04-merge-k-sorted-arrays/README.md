---
name: sheet-merge-k-sorted-arrays
title: 'Merge K Sorted Arrays'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
theory: merging-many-lists-with-a-heap
---

## Statement

`arrays` is a list of `k` lists, each sorted in increasing order. Merge them into **one sorted list**.

For `[[1, 4, 5], [1, 3, 4], [2, 6]]` the answer is `[1, 1, 2, 3, 4, 4, 5, 6]`.

### Examples

**Example 1**

Input:

```python
merge_k_arrays([[1, 4, 5], [1, 3, 4], [2, 6]])
```

Output:

```text
[1, 1, 2, 3, 4, 4, 5, 6]
```

**Example 2**

Input:

```python
merge_k_arrays([[], [1]])
```

Output:

```text
[1]
```

### Constraints

- `0 <= k <= 10000`
- `0 <= total number of values <= 200000`
- `-10**9 <= value <= 10**9`

## Explanation

The tuple carries the array number and the position, so after a pop you know where to read the next value. Equal values compare by array number, so tuples never compare past the integers.

### Complexity

- Time: O(N log k). A heap of `k` array heads gives the next smallest value in `O(log k)`, done `N` times.
- Space: O(k). The heap (the result is output).
