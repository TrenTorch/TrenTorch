---
name: sheet-binary-numbers-up-to-n
title: 'Binary Numbers From 1 to N'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Beginner
theory: counting-in-order
---

## Statement

Return the binary representations of `1, 2, 3, ..., n` as a list of strings (`["1", "10", "11", "100", ...]`). Use a **queue** rather than converting each number.

### Examples

**Example 1**

Input:

```python
binary_numbers_up_to(5)
```

Output:

```text
['1', '10', '11', '100', '101']
```

**Example 2**

Input:

```python
binary_numbers_up_to(0)
```

Output:

```text
[]
```

### Constraints

- `0 <= n <= 200000`

## Explanation

Each loop round outputs the oldest string and queues its two children. After `n` rounds the output is the first `n` binary numbers.

### Complexity

- Time: O(n log n). `n` strings of up to `log2(n) + 1` characters have to be written.
- Space: O(n log n). The output; the queue holds at most `n` strings.
