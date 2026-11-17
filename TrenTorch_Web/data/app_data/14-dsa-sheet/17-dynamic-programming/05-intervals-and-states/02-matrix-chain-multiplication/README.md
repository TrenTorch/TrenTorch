---
name: sheet-matrix-chain-multiplication
title: 'Matrix Chain Multiplication'
tags: [dsa-sheet, dynamic-programming, intervals-and-states]
difficulty: Mastery
theory: interval-dp-matrix-chain
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

## Explanation

`dp[i][j]` covers the sub-chain from boundary `i` to boundary `j`; `k` is where the last product splits it.

### Complexity

- Time: O(n^3). The table has `n^2` cells, each trying up to `n` split points.
- Space: O(n^2). The table.
