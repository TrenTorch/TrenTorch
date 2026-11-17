---
name: sheet-fruit-into-baskets
title: 'Fruit Into Baskets'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: at-most-k-different-letters
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

**Example 2**

Input:

```python
total_fruit([0, 1, 2, 2])
```

Output:

```text
3
```

### Constraints

- `0 <= len(fruits) <= 200000`
- `0 <= fruits[i] < 200000`

## Explanation

The dictionary is the contents of the baskets. A type is deleted when its count drops to zero.

### Complexity

- Time: O(n). Each index enters and leaves the window once.
- Space: O(1). The count map has at most 3 entries.
