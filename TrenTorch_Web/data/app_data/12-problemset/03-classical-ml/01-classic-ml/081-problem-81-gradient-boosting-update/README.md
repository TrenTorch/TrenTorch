---
name: problem-81-gradient-boosting-update
title: 'Gradient Boosting Update'
tags: [problemset, classical-ml-trees-ensembles, gradient-boosting]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'gradient boosting'
hint: 'pred += learning_rate*weak_pred'
tools: [NumPy]
---

## Statement

Add a shrinkage-scaled weak learner prediction to the ensemble. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** gradient boosting.

### Examples

Input: f(x)=x², x=3, h=1e-5
Output: approximately 6
Explanation: the centered finite difference approximates the analytic derivative 2x.

Input: f(x)=x³, x=2, h=1e-5
Output: approximately 12
Explanation: the derivative is 3x².

### Hint

<details><summary>Hint</summary>
pred += learning_rate*weak_pred
</details>

### Requirements

- Return the exact object described by the task; do not add logging or explanatory text to the return value.
- Use deterministic behavior for ties and boundary cases.
- Handle the explicit edge cases in the constraints without special-casing the visible examples.

### Input Format

```text
Arguments are passed directly to the typed Python function signature; no stdin/stdout parsing is used.
```

### Output Format

```text
Return the exact Python value described by the statement.
```

### Constraints

- Input sizes are bounded by the examples and function contract.
- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

- Inputs contain finite numeric values unless the problem explicitly states otherwise.
- Node sample count <= 10,000 and class count <= 32.
- Define behavior for empty inputs, singleton inputs, and zero denominators where applicable.

## Theory

### What is Gradient Boosting Update?

Gradient Boosting Update is the specific computational form of **gradient boosting** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Gradient Boosting Update is Necessary

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

### Why This Solution Works

The reference implementation follows the problem definition in the same order as the mechanism above. It computes the required intermediate state once, uses explicit boundary checks where division, normalization, sampling, or masking could otherwise become undefined, and returns only the requested result. This matters because a superficially similar implementation can produce the wrong shape, leak held-out statistics, mishandle a zero denominator, or change a boundary condition.

### Complexity and Optimization

The shown implementation uses the simplest asymptotic structure that matches the task. Vectorized NumPy operations move inner loops into optimized array kernels where that is natural; explicit loops remain where the algorithm itself is sequential or where clarity is more important than micro-optimization. The usual optimization is to avoid recomputing distances, norms, masks, or reductions that can be cached once. Space is dominated by the output and any intermediate arrays required by the stated operation. Do not replace the reference with an optimization that changes numerical semantics or makes the implementation harder to verify.

---
