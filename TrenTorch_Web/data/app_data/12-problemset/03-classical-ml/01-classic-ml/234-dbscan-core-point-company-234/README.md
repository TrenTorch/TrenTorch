---
name: dbscan-core-point-company-234
title: 'dbscan-core-point — Ola case'
tags: [problemset, unsupervised-ml, dbscan, ola]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'Classic ML'
caseCompany: 'Ola'
hint: 'Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.'
tools: [NumPy]
---

## Statement

Ola-inspired location-clustering service must identify dense groups of nearby pickup points while treating sparse points differently. You need to determine whether each point is a DBSCAN core point under the supplied radius and minimum-neighbor rules.

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
[[0,0],[0,1],[5,5]],1.1,2
```

**Output**
```text
[True,True,False]
```

**Explanation:** The first two points are within the radius of each other, while the isolated point has only itself.

### Hints

<details><summary>Hint 1</summary>
Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed.
</details>

<details><summary>Hint 2</summary>
Pay attention to the boundary case in which the denominator, norm, mask, or candidate set can become degenerate.
</details>

## Theory

### The simple version

**DBSCAN** is the mechanism behind this task. The important idea is to implement the definition directly, while preserving numerical stability and the shape of the data that later stages expect.

### The formula

|N_eps(x)|\ge minPts.

The symbols in the formula correspond directly to the values in the function signature; the implementation should compute these quantities in the same logical order.

### Worked reasoning

DBSCAN defines dense regions using neighborhood counts rather than a preselected number of clusters.

## Explanation

The reference solution first converts inputs into the representation required by the operation, computes the necessary intermediate state once, and then returns the requested result. The key implementation choice is the handling of the non-obvious boundary or numerical case rather than merely reproducing the formula.

O(n²d) time and O(n²) memory for the full distance matrix.
