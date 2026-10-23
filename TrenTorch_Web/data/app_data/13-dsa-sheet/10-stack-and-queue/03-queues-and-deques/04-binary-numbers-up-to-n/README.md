---
name: sheet-binary-numbers-up-to-n
title: 'Binary Numbers From 1 to N'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Beginner
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

## Theory

The binary numbers in order follow a pattern: the numbers after `x` are `x + "0"` and `x + "1"`. Start with `"1"`. Take the front of a queue, output it, and add its two children `front + "0"` and `front + "1"` at the back. Because it is a queue (first in, first out), the numbers come out in increasing order.

This is **breadth-first search** on an infinite binary tree: you visit all nodes of one level before the next one. A queue is the data structure behind BFS, and you will meet it again for trees and graphs.

## Explanation

Each loop round outputs the oldest string and queues its two children. After `n` rounds the output is the first `n` binary numbers.
