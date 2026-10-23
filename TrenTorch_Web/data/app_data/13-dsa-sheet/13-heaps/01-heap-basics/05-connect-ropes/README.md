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

**Example 2**

Input:

```python
connect_ropes([1, 2, 3, 4, 5])
```

Output:

```text
33
```

### Constraints

- `0 <= len(ropes) <= 100000`
- `1 <= ropes[i] <= 10**4`

## Theory

A **heap** (priority queue) always gives you the **smallest** item in `O(log n)`, while letting you add items in `O(log n)`. Python's `heapq` module implements a **min-heap** on a plain list: `heappush(h, x)`, `heappop(h)` (the smallest), `h[0]` (peek) and `heapify(h)` (turn a list into a heap in `O(n)`). For a **max-heap** push the negated values.

A rope that is joined early gets **counted again** in every later join that contains it. So the long ropes should be joined **last**, and the short ones first: always join the **two shortest** ropes. (This is the same idea as building a Huffman code.)

A min-heap gives the two shortest ropes in `O(log n)`: pop two, add their sum to the total, push the sum back. Repeat until one rope is left. `O(n log n)`.

## Explanation

Each loop pops the two smallest, adds the cost and pushes the new rope. The heap shrinks by one each round.
