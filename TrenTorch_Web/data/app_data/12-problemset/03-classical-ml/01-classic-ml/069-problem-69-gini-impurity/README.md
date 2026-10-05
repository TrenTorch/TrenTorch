---
name: problem-69-gini-impurity
title: 'Gini Impurity'
tags: [problemset, classical-ml-trees-ensembles, decision-trees]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'decision trees'
hint: 'use 1-sum p²'
tools: [NumPy]
---

## Statement

### Input Format

```python
solve(counts)
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
solve([2,2])
```

**Output**

```text
0.5
```

The output is produced by running the reference solution with these arguments.

**Example 2**

**Input**

```python
solve([0,0])
```

**Output**

```text
1.0
```

The output is produced by running the reference solution with these arguments.

### Hints

<details><summary>Hint</summary>

use 1-sum p²

</details>

## Theory

### What is Gini Impurity?

Gini Impurity is the specific computational form of **decision trees** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Gini Impurity is Necessary

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

The reference implementation follows the contract for Gini Impurity and returns the computed value without printing.
