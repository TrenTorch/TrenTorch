---
name: sheet-last-stone-weight
title: 'Last Stone Weight'
tags: [dsa-sheet, heaps, heap-basics]
difficulty: Beginner
theory: smash-the-heaviest-stones
---

## Statement

`stones[i]` is the weight of stone `i`. Each turn take the **two heaviest** stones and smash them together. If their weights are equal both are destroyed; otherwise the lighter one is destroyed and the heavier one keeps the **difference** of the weights. Return the weight of the **last remaining stone**, or `0` if none is left.

For `[2, 7, 4, 1, 8, 1]` the answer is `1`.

The starter code sorts all stones after every smash. It is correct but too slow for many stones.

### Examples

**Example 1**

Input:

```python
last_stone_weight([2, 7, 4, 1, 8, 1])
```

Output:

```text
1
```

**Example 2**

Input:

```python
last_stone_weight([1])
```

Output:

```text
1
```

### Constraints

- `0 <= len(stones) <= 100000`
- `1 <= stones[i] <= 10**9`

## Explanation

`heap` holds negative weights, so `heappop` returns the heaviest stone. The loop runs until at most one stone remains.

### Complexity

- Time: O(n log n). Each of at most `n - 1` rounds pops two stones and pushes one, `O(log n)` each.
- Space: O(n). The heap.
