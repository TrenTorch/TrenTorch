---
name: sheet-min-stack-simulation
title: 'Stack With Minimum'
tags: [dsa-sheet, stack-and-queue, stack-basics]
difficulty: Intermediate
theory: a-stack-with-a-minimum
---

## Statement

A stack must support four operations, each in `O(1)`: `push x`, `pop`, `top` (the top value) and `get_min` (the smallest value in the stack). `ops` is a list of operations written as text, such as `"push 5"`, `"pop"`, `"top"` and `"get_min"`.

Run them from an empty stack and return the **results of every `top` and `get_min`**, in order. `push` and `pop` give no result. No operation is applied to an empty stack.

For `["push 5", "push 3", "get_min", "pop", "top", "get_min"]` the answer is `[3, 5, 5]`.

### Examples

**Example 1**

Input:

```python
min_stack(['push 5', 'push 3', 'get_min', 'pop', 'top', 'get_min'])
```

Output:

```text
[3, 5, 5]
```

**Example 2**

Input:

```python
min_stack(['push -2', 'push 0', 'push -3', 'get_min', 'pop', 'top', 'get_min'])
```

Output:

```text
[-3, 0, -2]
```

### Constraints

- `0 <= len(ops) <= 200000`
- `-10**9 <= x <= 10**9`
- `pop`, `top` and `get_min` are only used when the stack is not empty.

## Explanation

`mins[-1]` is the smallest value among all values at or below the current top. Because it is pushed and popped together with the value, it is always up to date.

### Complexity

- Time: O(n). Every operation is O(1), with `n` operations.
- Space: O(n). Two stacks (values and running minimums).
