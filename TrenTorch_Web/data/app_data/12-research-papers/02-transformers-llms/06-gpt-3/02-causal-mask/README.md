---
name: research-causal-mask
title: 'GPT-3: The Causal Attention Mask'
tags: [research-papers, transformers, llm, llm, transformer]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A GPT-style model is trained to predict each token from the tokens before it. During training every position is processed at once, so attention must be blocked from looking at the future. A causal mask does that.

### From theory to code

Implement `causal_mask(n)`, returning an `n x n` boolean matrix that allows attention only to current and earlier positions.

### Constraints

- `True` means the attention is allowed.

### Hints

<details>
<summary>Hint 1</summary>

Use a lower-triangular matrix of ones, cast to boolean.

</details>

## Theory

### The simple version

Blocking future positions keeps training consistent with generation, where the model only ever sees a prefix. Without the mask the model could copy the answer.

### The formula

$$M_{ij} = \begin{cases} 1 & j \le i \\ 0 & j > i \end{cases}$$

### How NumPy/PyTorch actually implements this

`torch.nn.Transformer.generate_square_subsequent_mask` builds the same triangle, and decoders apply it inside attention.

## Explanation

`np.tril` keeps the lower triangle; in attention code the masked entries are set to negative infinity before the softmax.
