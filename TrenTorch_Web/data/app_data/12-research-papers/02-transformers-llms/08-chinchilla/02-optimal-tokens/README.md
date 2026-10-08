---
name: research-chinchilla-optimal-tokens
title: 'Chinchilla: The Compute-Optimal Token Count'
tags: [research-papers, transformers, llm, scaling, compute]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Chinchilla (Hoffmann et al., 2022) found that many large models were trained on too few tokens for their size. For compute-optimal training, parameters and tokens should grow together, at roughly twenty tokens per parameter.

### From theory to code

Implement `chinchilla_optimal_tokens(n_params)`, returning `20 * N`.

### Constraints

- Result is a float.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the parameter count by 20.

</details>

## Theory

### The simple version

Given a fixed size, training on about twenty tokens per parameter gives the lowest loss for the compute spent. Training longer on less data, or bigger on the same data, wastes compute.

### The formula

$$D_{\text{opt}} \approx 20\,N$$

### How NumPy/PyTorch actually implements this

Model releases cite their token counts against this ratio to show whether they were trained compute-optimally.

## Explanation

This rule of thumb summarizes the paper's fitted curves. It is a planning estimate, not an exact law.
