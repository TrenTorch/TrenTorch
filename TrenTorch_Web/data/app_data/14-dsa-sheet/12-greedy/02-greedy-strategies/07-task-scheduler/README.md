---
name: sheet-task-scheduler
title: 'Task Scheduler'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
theory: task-scheduler
---

## Statement

`tasks` is a string where each letter is a task of one time unit. You may run the tasks in **any order**, and in each time unit you do one task or stay **idle**. The **same letter** needs at least `n` other time units (tasks or idle) between two runs. Return the **least number of time units** to finish all tasks.

For `tasks = "AAABBB"` and `n = 2` the answer is `8` (`A B _ A B _ A B`).

### Examples

**Example 1**

Input:

```python
least_interval('AAABBB', 2)
```

Output:

```text
8
```

**Example 2**

Input:

```python
least_interval('AAABBB', 0)
```

Output:

```text
6
```

### Constraints

- `0 <= len(tasks) <= 200000`
- `0 <= n <= 100`
- Upper-case letters.

## Explanation

`m` is the largest count and `ties` the number of letters with that count. The frame length is the minimum when idle time is needed; with many different tasks the answer is just `len(tasks)`.

### Complexity

- Time: O(n). One pass to count the tasks; the answer is a formula from the most frequent task.
- Space: O(1). A count per task name (26 at most).
