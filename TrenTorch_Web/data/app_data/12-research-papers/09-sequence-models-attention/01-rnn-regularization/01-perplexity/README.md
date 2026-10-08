---
name: research-zaremba-perplexity
title: 'RNN Regularization: Perplexity'
tags: [research-papers, sequence-models, language-modelling, regularization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Zaremba et al. (2014) regularize LSTM language models with dropout on the non-recurrent connections, and report results in perplexity. Perplexity is the exponential of the average per-token loss, so it reads as an effective number of choices per token.

### From theory to code

Implement `perplexity(total_nll, n)`, the exponential of the average negative log-likelihood per token.

### Constraints

- Losses are in nats.

### Hints

<details>
<summary>Hint 1</summary>

Divide the total loss by the token count, then exponentiate.

</details>

## Theory

### The simple version

A perplexity of k means the model is as uncertain as choosing uniformly among k tokens, which makes model comparisons easy to read.

### The formula

$$\text{PPL} = \exp\left(\frac{1}{n}\sum_{t=1}^{n}-\log p(x_t\mid x_{<t})\right)$$

### How NumPy/PyTorch actually implements this

Language-model evaluation scripts compute the same quantity from the summed token losses.

## Explanation

Lower perplexity is better; the paper reports validation and test perplexity for each model size.
