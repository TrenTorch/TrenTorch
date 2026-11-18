---
name: sheet-lemonade-change
title: 'Lemonade Stand Change'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Beginner
theory: greedy-with-a-small-memory
---

## Statement

A lemonade costs 5. Customers queue up and each pays with a bill of 5, 10 or 20, buying one lemonade. You start with no money, so you must give **change** from the bills you collected. Return `True` if you can give the correct change to **every** customer in order.

For `[5, 5, 5, 10, 20]` the answer is `True`; for `[5, 5, 10, 10, 20]` it is `False`.

### Examples

**Example 1**

Input:

```python
lemonade_change([5, 5, 5, 10, 20])
```

Output:

```text
True
```

**Example 2**

Input:

```python
lemonade_change([5, 5, 10, 10, 20])
```

Output:

```text
False
```

### Constraints

- `0 <= len(bills) <= 200000`
- Each bill is 5, 10 or 20.

## Explanation

Using the 10 first when a 20 arrives keeps as many 5s as possible. If neither way works, the answer is `False`.

### Complexity

- Time: O(n). One pass keeping the number of 5 and 10 bills.
- Space: O(1). Two counters.
