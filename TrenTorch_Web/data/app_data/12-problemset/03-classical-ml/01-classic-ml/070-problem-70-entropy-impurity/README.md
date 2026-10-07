---
name: problem-70-entropy-impurity
title: 'Entropy Impurity'
tags: [problemset, classical-ml-trees-ensembles, decision-trees]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'decision trees'
hint: 'normalize counts and sum -p log2 p'
tools: [NumPy]
---

## Statement

Compute information entropy from class counts. Implement `solve(...)` so that it returns the required result exactly. Treat the task as an implementation contract rather than an open-ended modeling exercise.

**Topic:** decision trees.

### Examples

Input: solve([3, 1])
Output: 0.8112781244591328
Explanation: the class proportions are [0.75, 0.25]; entropy is -sum(p*log2(p)) over them.

Input: solve([2, 2])
Output: 1.0
Explanation: equal counts give equal proportions [0.5, 0.5], one bit of entropy.

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

### What is Entropy Impurity?

Entropy Impurity is the specific computational form of **decision trees** needed by this problem. The goal is not merely to call a library routine, but to make the mathematical or algorithmic contract explicit enough that the same result can be reproduced from first principles.

### Why Entropy Impurity is Necessary

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
