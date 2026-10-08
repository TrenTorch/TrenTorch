---
name: research-switch-routing
title: 'Switch Transformers: Top-1 Routing'
tags: [research-papers, transformers, llm, moe, routing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Switch Transformers (Fedus, Zoph & Shazeer, 2021) send each token to just one expert, chosen by a router. Routing to a single expert keeps compute per token constant, even as the total number of parameters grows with the number of experts.

### From theory to code

Implement `switch_route(logits)`, which returns each token's top expert and that expert's softmax probability.

### Constraints

- Use a stable softmax over the expert axis.

### Hints

<details>
<summary>Hint 1</summary>

Softmax each row, take the argmax as the expert, then read that expert's probability as the gate.

</details>

## Theory

### The simple version

The gate multiplies the chosen expert's output, so the router receives a gradient through the probability even though the routing itself is a hard choice.

### The formula

$$i^* = \arg\max_i p_i(x), \qquad p(x) = \operatorname{softmax}(W_r x)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.softmax` followed by `torch.max` over the expert dimension gives the same routing.

## Explanation

Argmax is not differentiable, so the gradient reaches the router through the selected probability used as a multiplier.
