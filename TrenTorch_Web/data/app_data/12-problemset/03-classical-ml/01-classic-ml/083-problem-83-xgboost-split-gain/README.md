---
name: problem-83-xgboost-split-gain
title: 'XGBoost Split Gain'
tags: [problemset, classical-ml-trees-ensembles, regularized-boosting]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'regularized boosting'
hint: 'compare child score sum against parent with regularization'
tools: [NumPy]
---

## Statement

### Input Format

```python
solve(GL, HL, GR, HR, GP, HP, lam)
```

Arguments are passed directly to the function; there is no stdin/stdout parsing.

### Output Format

Return the value computed by `solve`; do not print it.

### Constraints

- Vector inputs contain at most 100,000 elements; matrix dimensions are at most 512 per axis.
- Inputs must satisfy the shapes and finite-value assumptions in the function signature.

- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Example

**Example 1**

**Input**

```python
solve(...)
```

**Output**

```text
See the function's return value for this input.
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

compare child score sum against parent with regularization

</details>

## Theory

### What is XGBoost Split Gain?

XGBoost Split Gain is the specific computational form of **regularized boosting** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why XGBoost Split Gain is Necessary

- A tree split must improve the chosen impurity or objective.
- Ensemble methods reduce variance or bias by combining weak or diverse learners.
- Regularization and sampling determine how much each learner contributes.

### The Process / Mechanism

Compute the node or ensemble statistic, compare candidate choices, select the best valid option, then update predictions, weights, or counts.

### Mathematical Representation

For class proportions \(p_c\), Gini impurity is \(G=1-\sum_c p_c^2\). For a weighted split, \(G_{\mathrm{split}}=\frac{n_L}{n}G_L+\frac{n_R}{n}G_R\).

### Worked Example

For the first example, identify the inputs, compute the intermediate quantities in the order described by the mechanism, and only then form the final result. For the boundary example, apply the same rules without changing the algorithm; the edge case should fall out of the definition rather than from an unrelated special-case output.

## Explanation

The reference implementation follows the contract for XGBoost Split Gain and returns the computed value without printing.
