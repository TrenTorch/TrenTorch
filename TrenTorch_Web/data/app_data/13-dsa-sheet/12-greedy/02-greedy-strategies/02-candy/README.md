---
name: sheet-candy
title: 'Distribute Candy'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
---

## Statement

Children stand in a line with ratings `ratings[i]`. Every child gets **at least one** candy, and a child with a **higher rating than a neighbour** must get **more candies than that neighbour**. Return the **fewest candies** needed.

For `[1, 0, 2]` the answer is `5` (candies `2, 1, 2`).

### Examples

**Example 1**

Input:

```python
candy([1, 0, 2])
```

Output:

```text
5
```

**Example 2**

Input:

```python
candy([1, 2, 2])
```

Output:

```text
4
```

### Constraints

- `0 <= len(ratings) <= 200000`
- `0 <= ratings[i] <= 10**9`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

There are two rules, one for each neighbour, and they can conflict: a child can be higher than the left neighbour **and** than the right one. Handle each direction in its own pass, then combine:

1. **Left to right**: if `ratings[i] > ratings[i - 1]`, then `give[i] = give[i - 1] + 1`, else 1.
2. **Right to left**: if `ratings[i] > ratings[i + 1]`, then `give[i] = max(give[i], give[i + 1] + 1)`.

The `max` satisfies both rules at once, and each child gets the least that works. Total: the sum. `O(n)`.

## Explanation

After the first pass every child respects the left neighbour. The second pass raises a child only as much as the right neighbour demands, never lowering what the first pass gave.
