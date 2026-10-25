---
name: sheet-connect-ropes
title: 'Connect Ropes With Minimum Cost'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
---

## Statement

You have ropes with lengths `ropes[i]`. Joining two ropes costs the **sum of their lengths** and gives one rope of that length. Join all the ropes into one, and return the **minimum total cost**.

For `[4, 3, 2, 6]` the answer is `29` (join 2+3 = 5, then 4+5 = 9, then 6+9 = 15; total 5 + 9 + 15 = 29).

The starter code re-sorts the ropes after every join. It is correct but too slow for many ropes.

### Examples

**Example 1**

Input:

```python
connect_ropes([4, 3, 2, 6])
```

Output:

```text
29
```

**Explanation:** The smallest ropes are joined first, minimizing the cost at each step.

**Example 2**

Input:

```python
connect_ropes([1, 2, 3, 4, 5])
```

Output:

```text
33
```

**Explanation:** The total cost is the sum of the lengths of the ropes joined at each step.

### Constraints

- `0 <= len(ropes) <= 100000`
- `1 <= ropes[i] <= 10**4`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

A rope that is joined early gets **counted again** in every later join that contains it. So the long ropes should be joined **last**, and the short ones first: always join the **two shortest** ropes. (This is the same idea as building a Huffman code.)

A min-heap gives the two shortest ropes in `O(log n)`: pop two, add their sum to the total, push the sum back. Repeat until one rope is left. `O(n log n)`.

## Explanation

Each loop pops the two smallest, adds the cost and pushes the new rope. The heap shrinks by one each round.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                      | Variables                            |
| ---------------------------------------------------- | ------------------------------------ |
| `heap = list(ropes)`                                 | `heap = [4, 3, 2, 6]`                |
| `total = 0`                                          | `heap = [2, 3, 4, 6], total = 0`     |
| `joined = heapq.heappop(heap) + heapq.heappop(heap)` | `heap = [4, 6], joined = 5`          |
| `heapq.heappush(heap, joined)`                       | `heap = [4, 6, 5], total = 5`        |
| `total += joined`                                    | `heap = [6], total = 14, joined = 9` |
| `joined = heapq.heappop(heap) + heapq.heappop(heap)` | `heap = [], joined = 15`             |
| `total += joined`                                    | `total = 29`                         |
| `return`                                             | `returned = 29`                      |

### Complexity

- Time: O(n log n).
- Extra space: O(n).
- The brute force takes O(n^2 log n).
