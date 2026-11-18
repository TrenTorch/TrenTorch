---
name: sheet-queue-with-two-stacks
title: 'Queue Made of Two Stacks'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Intermediate
theory: why-it-is-fast-on-average
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

**Example 2**

Input:

```python
queue_with_two_stacks(['empty', 'push 5', 'empty'])
```

Output:

```text
[1, 0]
```

### Constraints

- `0 <= len(ops) <= 200000`
- `-10**9 <= x <= 10**9`

## Explanation

`move()` refills the outbox only when it is empty. Between refills, `pop` and `peek` work on the outbox top, which is the front of the queue.

### Complexity

- Time: O(n). Every value moves from the inbox to the outbox at most once, so each operation is O(1) amortised.
- Space: O(n). The two stacks.
