---
name: sheet-fruit-into-baskets
title: 'Fruit Into Baskets'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

Trees stand in a row, and `fruits[i]` is the type of fruit on tree `i`. You have **two baskets**, and each basket holds only **one type** of fruit (any number of pieces). Starting at any tree, you pick exactly one fruit from every tree to the right, in order, until you reach a tree whose fruit does not fit in the baskets, and then you stop. Return the **most fruits** you can pick.

This is the longest run of trees with **at most two types**. For `[1, 2, 3, 2, 2]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
total_fruit([1, 2, 3, 2, 2])
```

Output:

```text
4
```

**Explanation:** The subarray [2, 3, 2, 2] contains at most two fruit types, which are 2 and 3, giving a maximum length of 4.

**Example 2**

Input:

```python
total_fruit([0, 1, 2, 2])
```

Output:

```text
3
```

**Explanation:** The subarray [1, 2, 2] contains at most two fruit types, which are 1 and 2, giving a maximum length of 3.

### Constraints

- `0 <= len(fruits) <= 200000`
- `0 <= fruits[i] < 200000`

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

This is "longest subarray with at most `k` distinct values" with `k = 2`, the same as the previous question on characters. Keep a dictionary of the fruit types in the window and their counts; when it holds more than 2 types, shrink from the left until one type disappears.

Recognising that a story question is a known pattern in disguise is half the work.

## Explanation

The dictionary is the contents of the baskets. A type is deleted when its count drops to zero.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                      | Variables                                          |
| ------------------------------------ | -------------------------------------------------- |
| `count = {}`                         | `count = {}`                                       |
| `for right, f in enumerate(fruits):` | `left = 0, best = 0, right = 0, f = 1`             |
| `for right, f in enumerate(fruits):` | `count = {1: 1}, best = 1, right = 1, f = 2`       |
| `for right, f in enumerate(fruits):` | `count = {1: 1, 2: 1}, best = 2, right = 2, f = 3` |
| `count[fruits[left]] -= 1`           | `count = {1: 0, 2: 1, 3: 1}`                       |
| `for right, f in enumerate(fruits):` | `count = {2: 1, 3: 1}, left = 1, right = 3, f = 2` |
| `for right, f in enumerate(fruits):` | `count = {2: 2, 3: 1}, best = 3, right = 4`        |
| `return`                             | `returned = 4`                                     |

### Complexity

- Time: O(n) where n is the number of trees.
- Extra space: O(1) since the map stores at most three elements.
- The brute force takes O(n^3) where n is the number of trees.
