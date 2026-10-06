---
name: gini-impurity-company-208
title: 'gini-impurity — Cloudflare case'
tags: [problemset, classical-ml-trees-ensembles, decision-trees, cloudflare]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Cloudflare'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Cloudflare** ranking and experimentation team might handle; it is not a real interview question or a claim that Cloudflare uses this exact task. The team needs a reliable implementation for decision-tree training in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Compute the Gini impurity of a binary label vector for a decision-tree node.

### Input Format

```text
See the `solve(...)` signature in the reference implementation. Arguments are ordinary Python values or NumPy arrays; no stdin/stdout parsing is used.
```

### Output Format

```text
Return exactly the scalar, vector, matrix, tuple, or other Python object described by the statement.
```

### Constraints

- Inputs must satisfy the dimensions and value assumptions stated by the problem.
- Use finite floating-point values unless the statement explicitly permits another case.
- Input sizes are bounded so the reference implementation completes comfortably within the platform limit.
- Time limit: 20 seconds (platform default — see processes/code-execution/pyodide-service.ts).

### Example

**Input**
```text
[0,0,1,1]
```

**Output**
```text
0.5
```

**Explanation:** The node contains two classes with equal probability, producing maximum binary impurity.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**gini impurity** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

G=1-\sum_c p_c^2.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

Gini impurity measures how often a randomly chosen item would be misclassified using the node's class distribution.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n) time and O(1) auxiliary space.
