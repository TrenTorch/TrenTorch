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

**Explanation:** The queue generates binary strings in order, and five iterations produce the first five binary numbers, matching the expected list.

**Example 2**

Input:

```python
binary_numbers_up_to(0)
```

Output:

```text
[]
```

**Explanation:** With n=0 the loop runs zero times, so the queue remains empty and the result is an empty list.

### Constraints

- `0 <= n <= 200000`

## Theory

The binary numbers in order follow a pattern: the numbers after `x` are `x + "0"` and `x + "1"`. Start with `"1"`. Take the front of a queue, output it, and add its two children `front + "0"` and `front + "1"` at the back. Because it is a queue (first in, first out), the numbers come out in increasing order.

This is **breadth-first search** on an infinite binary tree: you visit all nodes of one level before the next one. A queue is the data structure behind BFS, and you will meet it again for trees and graphs.

## Explanation

Each loop round outputs the oldest string and queues its two children. After `n` rounds the output is the first `n` binary numbers.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                                    |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| `out = []`                  | `out = []`                                                                                   |
| `out.append(front)`         | `out = ['1'], queue = deque([]), _ = 0, front = '1'`                                         |
| `front = queue.popleft()`   | `queue = deque(['11']), _ = 1, front = '10'`                                                 |
| `for _ in range(n):`        | `out = ['1', '10'], queue = deque(['11', '100', '101']), _ = 2`                              |
| `queue.append(front + "0")` | `out = ['1', '10', '11'], queue = deque(['100', '101', '110']), front = '11'`                |
| `out.append(front)`         | `out = ['1', '10', '11', '100'], queue = deque(['101', '110', '111']), _ = 3, front = '100'` |
| `front = queue.popleft()`   | `queue = deque(['110', '111', '1000', '1001']), _ = 4, front = '101'`                        |
| `return`                    | `returned = ['1', '10', '11', '100', '101']`                                                 |

### Complexity

- Time: O(n) n is the input.
- Extra space: O(n) n is the input.
- The brute force takes O(n log n) n is the input.
