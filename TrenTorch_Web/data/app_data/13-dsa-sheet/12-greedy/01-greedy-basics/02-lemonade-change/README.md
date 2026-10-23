---
name: sheet-lemonade-change
title: 'Lemonade Stand Change'
tags: [dsa-sheet, greedy, greedy-basics]
difficulty: Beginner
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Change for a 5 needs nothing, for a 10 needs one 5, and for a 20 needs 15: either `10 + 5` or `5 + 5 + 5`. Count your 5s and 10s. For a 20 there are two ways; the greedy rule is to **prefer `10 + 5`**, because 10s can only be used for change in this one situation, while 5s are useful in every situation (including as change for another 10). Keep the flexible bills.

Process the queue, updating the counts; if you cannot make the change at any point, return `False`.

## Explanation

Using the 10 first when a 20 arrives keeps as many 5s as possible. If neither way works, the answer is `False`.
