---
name: sheet-merge-k-sorted-arrays
title: 'Merge K Sorted Arrays'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
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

**Explanation:** The merged list contains every element from all arrays in non-decreasing order. The smallest values 1 and 1 come from the first two arrays, followed by 2, 3, then 4 and 4, and finally 5 and 6.

**Example 2**

Input:

```python
merge_k_arrays([[], [1]])
```

Output:

```text
[1]
```

**Explanation:** Only one element exists across the arrays: 1 from the second array. The empty array contributes nothing, so the final list is [1].

### Constraints

- `0 <= k <= 10000`
- `0 <= total number of values <= 200000`
- `-10**9 <= value <= 10**9`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

The next value of the merged list is the smallest among the **front elements** of all arrays. A min-heap holds exactly those fronts: `(value, array_index, position)`. Pop the smallest, append it to the output, and push the next value from the same array (if any).

The heap never holds more than `k` items, so each of the `N` values costs `O(log k)`: `O(N log k)`. Sorting everything costs `O(N log N)`, and merging pairs of lists one after another costs `O(N * k)` in the worst case.

## Explanation

The tuple carries the array number and the position, so after a pop you know where to read the next value. Equal values compare by array number, so tuples never compare past the integers.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                  | Variables                                                                               |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]` | `heap = [(1, 0, 0), (1, 1, 0), (2, 2, 0)]`                                              |
| `out.append(value)`                                              | `heap = [(1, 1, 0), (2, 2, 0)], out = [1], value = 1, i = 0, j = 0`                     |
| `heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))`             | `heap = [(2, 2, 0), (4, 0, 1), (3, 1, 1)], out = [1, 1], i = 1`                         |
| `heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))`             | `heap = [(3, 1, 1), (4, 0, 1), (6, 2, 1)], out = [1, 1, 2], value = 2, i = 2`           |
| `heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))`             | `heap = [(4, 0, 1), (6, 2, 1), (4, 1, 2)], out = [1, 1, 2, 3], value = 3, i = 1, j = 1` |
| `heapq.heappush(heap, (arrays[i][j + 1], i, j + 1))`             | `heap = [(4, 1, 2), (6, 2, 1), (5, 0, 2)], out = [1, 1, 2, 3, 4], value = 4, i = 0`     |
| `out.append(value)`                                              | `heap = [(6, 2, 1)], out = [1, 1, 2, 3, 4, 4, 5], value = 5, j = 2`                     |
| `return`                                                         | `returned = [1, 1, 2, 3, 4, 4, 5, 6]`                                                   |

### Complexity

- Time: O(n log k), n total elements, k arrays.
- Extra space: O(k), heap of size k.
- The brute force takes O(n log n), sorting all elements.
