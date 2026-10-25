---
name: sheet-jump-game-ii
title: 'Fewest Jumps to the End'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Intermediate
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

**Explanation:** From index 0 jump 1 step to index 1 where value 3 allows reaching the last index in one further jump totaling 2 jumps.

**Example 2**

Input:

```python
min_jumps([2, 3, 0, 1, 4])
```

Output:

```text
2
```

**Explanation:** From index 0 jumping 1 step to index 1 where value 3 enables a direct jump to the last index achieving 2 jumps; jumping to index 2 with value 0 leads to a dead end.

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= nums[i] <= 100000`

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Think in **levels** like a breadth-first search. The indices reachable with 1 jump form a range `1 .. far1`; with 2 jumps a range up to `far2`, which is the farthest you can get from any index in the first range; and so on.

Keep three numbers: `end` (the last index reachable with the current number of jumps), `far` (the farthest index reachable with one more jump from anything seen so far) and `jumps`. Scan the indices: update `far = max(far, i + nums[i])`; when `i` reaches `end`, you must jump: `jumps += 1`, `end = far`. If `far` does not move beyond `i`, you are stuck.

This is `O(n)` and needs no extra memory.

## Explanation

Whenever the scan reaches `end`, the current jump count has covered everything it can; one more jump is required and the new range ends at `far`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line          | Variables                     |
| ------------------------ | ----------------------------- |
| `n = len(nums)`          | `n = 5`                       |
| `end = far = 0`          | `jumps = 0, end = 0, far = 0` |
| `for i in range(n - 1):` | `i = 0`                       |
| `jumps += 1`             | `jumps = 1, far = 2`          |
| `for i in range(n - 1):` | `end = 2, i = 1`              |
| `for i in range(n - 1):` | `far = 4, i = 2`              |
| `jumps += 1`             | `jumps = 2`                   |
| `return`                 | `returned = 2`                |

### Complexity

- Time: O(n) where n is the length of nums.
- Extra space: O(1) extra space where n is the length of nums.
- The brute force takes O(n^2) where n is the length of nums.
