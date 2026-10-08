---
name: research-chinchilla-optimal-params
title: 'Chinchilla: Choosing Model Size for a Budget'
tags: [research-papers, transformers, llm, scaling, compute]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

If you have a fixed compute budget, how big should the model be? Combining the two rules gives a square-root relationship: the compute-optimal parameter count grows with the square root of the budget.

### From theory to code

Implement `optimal_params_for_budget(flops)`, returning the compute-optimal parameter count `N = sqrt(C / 120)`.

### Constraints

- Derive from `C = 6 N D` with `D = 20 N`.

### Hints

<details>
<summary>Hint 1</summary>

Substitute `D = 20N` into `C = 6ND` to get `C = 120 N^2`, then solve for `N`.

</details>

## Theory

### The simple version

Compute splits evenly between model size and data in log terms. A budget that is 100 times larger supports a model that is only 10 times larger.

### The formula

$$C = 6\,N\,D,\ D = 20N \;\Rightarrow\; C = 120\,N^2 \;\Rightarrow\; N = \sqrt{C/120}$$

### How NumPy/PyTorch actually implements this

Pre-training planners solve this same equation to pick a model size for a given cluster budget.

## Explanation

The square root is what makes the budget split balanced. The same algebra gives the optimal token count from the same budget.
