---
name: research-seq2seq-sequence-nll
title: 'Seq2seq: The Sequence Negative Log-Likelihood'
tags: [research-papers, transformers, llm, seq2seq]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The seq2seq model is trained to maximize the probability of the correct target sentence. Because a sentence probability is a product of per-word probabilities, its negative log is a sum of per-word losses.

### From theory to code

Implement `sequence_nll(probs, targets)`, which returns the summed negative log-probability of the correct token at each step.

### Constraints

- `probs` has shape `(T, V)`, one distribution per step.

### Hints

<details>
<summary>Hint 1</summary>

Pick the probability of each correct token with fancy indexing, take `-log`, then sum.

</details>

## Theory

### The simple version

Taking the log turns the product of probabilities into a sum, which is numerically stable and gives the cross-entropy loss used in practice.

### The formula

$$\mathcal{L} = -\sum_{t=1}^{T}\log p(y_t \mid y_{<t}, x)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.cross_entropy(logits, targets, reduction='sum')` computes the same total.

## Explanation

Index pairs `(t, targets[t])` select the correct probability at each step; the `-log` and sum follow the formula.
