---
name: research-switch-load-balancing
title: 'Switch Transformers: The Load-Balancing Loss'
tags: [research-papers, transformers, llm, moe, routing]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Left alone, a learned router tends to send most tokens to a few favourite experts, leaving the rest unused. Switch Transformers add an auxiliary loss that penalizes uneven routing, so that the experts share the work.

### From theory to code

Implement `load_balancing_loss(expert_index, probs, n_experts)`, returning `E * sum_i f_i P_i`.

### Constraints

- `f_i` counts the tokens assigned to expert `i` divided by `T`.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.bincount` for the token fractions, take the mean of `probs` over tokens, then combine.

</details>

## Theory

### The simple version

The product `f_i P_i` is large only when an expert both receives many tokens and gets high router probability. Minimizing the sum pushes the router toward balance.

### The formula

$$\mathcal{L}_{\text{aux}} = \alpha\,E\sum_{i=1}^{E} f_i\,P_i, \qquad f_i = \frac{1}{T}\sum_t \mathbb{1}[\text{token } t \to i], \quad P_i = \frac{1}{T}\sum_t p_{t,i}$$

### How NumPy/PyTorch actually implements this

The `f_i` term is non-differentiable, so the gradient flows through `P_i`; implementations add this loss, scaled by a small coefficient, to the main objective.

## Explanation

The loss equals 1 for perfectly balanced routing and grows toward E when everything collapses onto one expert, so it works as a balance score.
