---
name: research-dropout-forward
title: 'Dropout: The Forward Pass With Inverted Scaling'
tags: [research-papers, regularization, dropout]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Dropout (Srivastava et al., 2014, following Hinton et al., 2012) fights overfitting by randomly switching off units during training. Each unit is kept with probability `1 - p` and dropped with probability `p`. Without correction, the next layer would see activations that are too small on average, so the survivors are scaled up. This question implements that forward pass.

### From theory to code

Implement `dropout_forward(x, keep_mask, p)`. It multiplies `x` by the mask and rescales by `1 / (1 - p)`. The signature and docstring are already in the editor.

### Constraints

- `keep_mask` has the same shape as `x` and holds 0s and 1s.
- `0 <= p < 1`.

### Hints

<details>
<summary>Hint 1</summary>

Multiply element-wise by the mask first, then divide by `1 - p`.

</details>

## Theory

### The simple version

Imagine a team where each member randomly sits out some meetings. To keep the total effort the same on average, the people who show up work a little harder. Inverted dropout does that: survivors are scaled up by `1 / (1 - p)` during training, so inference needs no change.

### The formula

$$
\tilde h = \frac{m \odot h}{1 - p}, \qquad m_i \sim \text{Bernoulli}(1 - p)
$$

- `h` — the activations before dropout.
- `m` — the keep mask, one entry per unit.
- `\odot` — element-wise multiplication.
- `p` — the drop probability.

### How NumPy/PyTorch actually implements this

`torch.nn.functional.dropout(x, p, training=True)` draws the mask and applies this exact scaling. The mask is sampled per call, so the same input gives different outputs in training mode.

## Explanation

`dropout_forward` multiplies by `keep_mask` and divides by `1 - p`. Dividing at training time means the expected activation matches inference, where nothing is dropped and nothing is rescaled.
