---
name: research-ns-loss
title: 'Negative Sampling: The Per-pair Loss'
tags: [research-papers, unsupervised, word-embeddings, negative-sampling]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Negative sampling (Mikolov et al., 2013) replaces the full softmax with a binary task: is this word a real context, or one of a few random words? Each training pair then costs only one positive and a handful of negative dot products.

### From theory to code

Implement `negative_sampling_loss(v_c, u_o, U_neg)`, the logistic loss for the true pair plus the sampled negatives.

### Constraints

- Use `logaddexp` to compute `-log sigma(x)` stably.

### Hints

<details>
<summary>Hint 1</summary>

The positive term is `-log sigma(u_o . v_c)`; each negative term is `-log sigma(-u_n . v_c)`. Sum all of them.

</details>

## Theory

### The simple version

The model learns to score real neighbours high and random words low. Sampling negatives from a noise distribution gives a cheap approximation of the softmax that works well in practice.

### The formula

$$\mathcal{L} = -\log\sigma(u_o^\top v_c) - \sum_{n=1}^{k}\mathbb{E}_{w_n \sim P_n}\big[\log\sigma(-u_{w_n}^\top v_c)\big]$$

### How NumPy/PyTorch actually implements this

Word-embedding libraries evaluate this loss with batched dot products and a logistic function.

## Explanation

The paper uses about five negatives per positive for small corpora and two to five for large ones.
