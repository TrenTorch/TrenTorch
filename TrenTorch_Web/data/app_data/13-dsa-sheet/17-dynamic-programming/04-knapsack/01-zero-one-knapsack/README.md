---
name: sheet-zero-one-knapsack
title: '0/1 Knapsack'
tags: [dsa-sheet, dynamic-programming, knapsack]
difficulty: Intermediate
---

## Statement

Item `i` weighs `weights[i]` and is worth `values[i]`. The bag holds total weight at most `capacity`. Use each item **at most once**. Return the **largest total value**.

For `weights = [1, 3, 4, 5]`, `values = [1, 4, 5, 7]` and `capacity = 7` the answer is `9` (items of weight 3 and 4).

### Examples

**Example 1**

Input:

```python
knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)
```

Output:

```text
9
```

**Example 2**

Input:

```python
knapsack([10], [100], 5)
```

Output:

```text
0
```

### Constraints

- `0 <= number of items <= 200`
- `1 <= weights[i] <= 1000`, `0 <= values[i] <= 1000`
- `0 <= capacity <= 10000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Greedy by value per weight is **wrong** here (items cannot be cut), so DP. **State:** `best(i, w)`, the best value using the first `i` items with room `w`. **Transition:** item `i` is skipped (`best(i - 1, w)`) or taken if it fits (`values[i] + best(i - 1, w - weights[i])`). **Base case:** no items, value 0.

Use one array `best[w]` and process each item with `w` **going downwards**, so that an item is not used twice (`best[w - weight]` still refers to the table without this item). `O(items × capacity)`.

## Explanation

The downward loop over `w` is the whole trick: an upward loop would let the same item be taken many times (the unbounded knapsack).

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                              | Variables                                                       |
| -------------------------------------------- | --------------------------------------------------------------- |
| `best = [0] * (capacity + 1)`                | `best = [0, 0, 0, 0, 0, 0, 0, 0]`                               |
| `for w in range(capacity, weight - 1, -1):`  | `best = [0, 0, 0, 0, 0, 0, 1, 1], weight = 1, value = 1, w = 5` |
| `for w in range(capacity, weight - 1, -1):`  | `best = [0, 0, 0, 1, 1, 1, 1, 1], w = 2`                        |
| `best[w] = best[w - weight] + value`         | `best = [0, 1, 1, 1, 1, 1, 1, 5], weight = 3, value = 4, w = 7` |
| `for w in range(capacity, weight - 1, -1):`  | `best = [0, 1, 1, 1, 1, 5, 5, 5], w = 4`                        |
| `best[w] = best[w - weight] + value`         | `best = [0, 1, 1, 4, 5, 5, 5, 9], weight = 4, value = 5, w = 7` |
| `for weight, value in zip(weights, values):` | `best = [0, 1, 1, 4, 5, 6, 6, 9], weight = 5, value = 7, w = 4` |
| `return`                                     | `returned = 9`                                                  |

### Complexity

- Time: O(n * capacity).
- Extra space: O(capacity).
- The brute force takes O(2^n).
