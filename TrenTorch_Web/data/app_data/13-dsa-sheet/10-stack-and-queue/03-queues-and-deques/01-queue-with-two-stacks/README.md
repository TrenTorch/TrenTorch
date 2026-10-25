---
name: sheet-queue-with-two-stacks
title: 'Queue Made of Two Stacks'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Intermediate
---

## Statement

A **queue** is first in, first out. Build one from **two stacks** (Python lists used only with `append` and `pop()` from the end) so that every operation takes `O(1)` on average. `ops` is a list of operations written as text: `"push x"`, `"pop"` (remove and return the front), `"peek"` (return the front) and `"empty"` (return `1` if the queue is empty, otherwise `0`).

Run them from an empty queue and return the **results of every `pop`, `peek` and `empty`**, in order. `pop` and `peek` are only used on a non-empty queue.

For `["push 1", "push 2", "peek", "pop", "empty"]` the answer is `[1, 1, 0]`.

### Examples

**Example 1**

Input:

```python
queue_with_two_stacks(['push 1', 'push 2', 'peek', 'pop', 'empty'])
```

Output:

```text
[1, 1, 0]
```

**Explanation:** After pushing 1 and 2 the front is 1, so peek yields 1; pop removes that 1; the queue then contains 2, so empty returns 0.

**Example 2**

Input:

```python
queue_with_two_stacks(['empty', 'push 5', 'empty'])
```

Output:

```text
[1, 0]
```

**Explanation:** The queue starts empty, so empty returns 1; after pushing 5 the queue is non-empty, so empty returns 0.

### Constraints

- `0 <= len(ops) <= 200000`
- `-10**9 <= x <= 10**9`

## Theory

A stack reverses the order of what you put in. **Two reversals give the original order**. Keep an `inbox` stack for `push` and an `outbox` stack for `pop` and `peek`. When the outbox is empty and you need the front, **move everything** from the inbox to the outbox, one pop and push at a time. Now the oldest value is on top of the outbox.

Moving looks expensive, but each value is moved **at most once** on its way through the queue, so over `n` operations the total moving work is `O(n)`. That is called **amortized** `O(1)` per operation.

The queue is empty only when both stacks are empty.

## Explanation

`move()` refills the outbox only when it is empty. Between refills, `pop` and `peek` work on the outbox top, which is the front of the queue.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line  | Variables                                                                            |
| ---------------- | ------------------------------------------------------------------------------------ |
| `inbox = []`     | `inbox = []`                                                                         |
| `out = []`       | `outbox = [], out = []`                                                              |
| `for op in ops:` | `move = <function queue_with_two_stacks.<locals>.move at 0x000001..., op = 'push 1'` |
| `for op in ops:` | `inbox = [1], op = 'push 2'`                                                         |
| `move()`         | `inbox = [], outbox = [2, 1], op = 'peek'`                                           |
| `for op in ops:` | `out = [1], op = 'pop'`                                                              |
| `for op in ops:` | `outbox = [2], out = [1, 1], op = 'empty'`                                           |
| `return`         | `returned = [1, 1, 0]`                                                               |

### Complexity

- Time: O(n) where n is number of operations.
- Extra space: O(n) extra memory for the two stacks.
- The brute force takes O(n) where n is number of operations.
