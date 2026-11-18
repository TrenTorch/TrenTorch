---
name: sheet-connect-ropes
title: 'Connect Ropes With Minimum Cost'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Intermediate
theory: join-the-cheapest-pair
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

## Explanation

Each loop pops the two smallest, adds the cost and pushes the new rope. The heap shrinks by one each round.

### Complexity

- Time: O(n log n). Each of `n - 1` joins pops two ropes and pushes one, `O(log n)` each; always joining the two shortest is optimal (Huffman).
- Space: O(n). The heap.
