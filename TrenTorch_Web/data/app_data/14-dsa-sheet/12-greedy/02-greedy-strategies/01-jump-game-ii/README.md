---
name: sheet-jump-game-ii
title: 'Fewest Jumps to the End'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
theory: fewest-jumps
---

## Statement

You start at index 0. `nums[i]` is the **maximum jump length** from index `i`. Return the **fewest jumps** needed to reach the last index, or `-1` if it is unreachable. A list with 0 or 1 elements needs 0 jumps.

For `[2, 3, 1, 1, 4]` the answer is `2` (jump 1 step to index 1, then 3 steps to the end).

The starter code updates every reachable index from every earlier index. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
min_jumps([2, 3, 1, 1, 4])
```

Output:

```text
2
```

**Example 2**

Input:

```python
min_jumps([2, 3, 0, 1, 4])
```

Output:

```text
2
```

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= nums[i] <= 100000`

## Explanation

Whenever the scan reaches `end`, the current jump count has covered everything it can; one more jump is required and the new range ends at `far`.

### Complexity

- Time: O(n). One pass; each index is passed once while the current jump range is extended.
- Space: O(1). A few numbers.
