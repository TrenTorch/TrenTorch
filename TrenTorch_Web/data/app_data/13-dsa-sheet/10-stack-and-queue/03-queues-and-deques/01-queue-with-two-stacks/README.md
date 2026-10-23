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

## Theory

A stack reverses the order of what you put in. **Two reversals give the original order**. Keep an `inbox` stack for `push` and an `outbox` stack for `pop` and `peek`. When the outbox is empty and you need the front, **move everything** from the inbox to the outbox, one pop and push at a time. Now the oldest value is on top of the outbox.

Moving looks expensive, but each value is moved **at most once** on its way through the queue, so over `n` operations the total moving work is `O(n)`. That is called **amortized** `O(1)` per operation.

The queue is empty only when both stacks are empty.

## Explanation

`move()` refills the outbox only when it is empty. Between refills, `pop` and `peek` work on the outbox top, which is the front of the queue.
