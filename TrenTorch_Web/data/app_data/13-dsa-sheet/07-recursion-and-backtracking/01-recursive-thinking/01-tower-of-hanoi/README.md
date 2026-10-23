---
name: sheet-tower-of-hanoi
title: 'Tower of Hanoi'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Intermediate
---

## Statement

There are three pegs, numbered `1`, `2` and `3`. `n` disks of different sizes start stacked on peg `1`, the biggest at the bottom. You may move **one disk at a time** from the top of one peg to another peg, and you may **never put a bigger disk on a smaller one**.

Return the list of moves, each written `[from_peg, to_peg]`, that shifts all the disks to peg `3` using the **fewest** moves. (The shortest solution is unique.)

### Examples

**Example 1**

Input:

```python
tower_of_hanoi(2)
```

Output:

```text
[[1, 2], [1, 3], [2, 3]]
```

**Example 2**

Input:

```python
tower_of_hanoi(0)
```

Output:

```text
[]
```

### Constraints

- `0 <= n <= 14`
- The answer has `2^n - 1` moves.

## Theory

This is the textbook example of recursive thinking. To move `n` disks from `source` to `target` using a spare peg:

1. Move the top `n - 1` disks from `source` to `spare` (a smaller version of the same problem).
2. Move the biggest disk from `source` to `target`.
3. Move the `n - 1` disks from `spare` to `target` (the same smaller problem again).

The base case is `n = 0`: nothing to move. The number of moves satisfies `T(n) = 2 * T(n - 1) + 1`, so `T(n) = 2^n - 1`: 15 moves for 4 disks, 16,383 for 14. Many problems become easy once you trust the smaller version to work.

## Explanation

`move(k, source, target, spare)` does nothing for `k == 0`. Otherwise it moves `k - 1` disks out of the way (to the spare), records `[source, target]` for the big disk, and moves the `k - 1` disks on top of it. The pegs swap roles in the two recursive calls.
