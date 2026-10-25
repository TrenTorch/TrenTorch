---
name: sheet-matrix-chain-multiplication
title: 'Matrix Chain Multiplication'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
---

## Statement

Matrix `i` has `dims[i]` rows and `dims[i + 1]` columns, so `len(dims) - 1` matrices are given. Multiplying a `p x q` matrix by a `q x r` matrix costs `p * q * r` scalar multiplications. The **order of the multiplications** (the brackets) changes the total cost. Return the **smallest total cost** to multiply the whole chain. With fewer than two matrices the cost is `0`.

For `dims = [10, 30, 5, 60]` the answer is `4500` (`(A B) C`).

### Examples

**Example 1**

Input:

```python
matrix_chain_cost([10, 30, 5, 60])
```

Output:

```text
4500
```

**Example 2**

Input:

```python
matrix_chain_cost([40, 20, 30, 10, 30])
```

Output:

```text
26000
```

### Constraints

- `0 <= len(dims) <= 121`
- `1 <= dims[i] <= 100`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

Choose the **last multiplication**: split the chain at some `k`, multiply `i..k` and `k..j` separately, then multiply the two results. **State:** `cost(i, j)`, the cheapest way to multiply the matrices between the dimensions `i` and `j`. **Transition:** `cost(i, j) = min over k of cost(i, k) + cost(k, j) + dims[i] * dims[k] * dims[j]`. **Base case:** a single matrix costs 0. Fill by increasing chain length. `O(n³)`.

## Explanation

`dp[i][j]` covers the sub-chain from boundary `i` to boundary `j`; `k` is where the last product splits it.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line             | Variables                                                                                          |
| --------------------------- | -------------------------------------------------------------------------------------------------- |
| `n = len(dims)`             | `n = 4`                                                                                            |
| `j = i + length`            | `dp = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], length = 2, i = 0, j = 2`          |
| `best = value`              | `best = 1500, k = 1, value = 1500`                                                                 |
| `best = float("inf")`       | `dp = [[0, 0, 1500, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], i = 1, j = 3, best = inf`       |
| `best = value`              | `best = 9000, k = 2, value = 9000`                                                                 |
| `best = float("inf")`       | `dp = [[0, 0, 1500, 0], [0, 0, 0, 9000], [0, 0, 0, 0], [0, 0, 0..., length = 3, i = 0, best = inf` |
| `for k in range(i + 1, j):` | `best = 27000, value = 27000`                                                                      |
| `return`                    | `returned = 4500`                                                                                  |

### Complexity

- Time: O(n^3), where n is the number of matrices. The solution uses dynamic programming to fill a table of size n x n.
- Extra space: O(n^2), where n is the number of matrices. The solution uses a 2D list to store intermediate results.
- The brute force takes O(2^n), where n is the number of matrices. The brute-force solution tries all possible multiplication orders.
