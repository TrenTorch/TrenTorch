---
name: research-zaremba-nonrecurrent-dropout
title: 'RNN Regularization: Dropout on Non-recurrent Connections'
tags: [research-papers, sequence-models, language-modelling, regularization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Zaremba et al. found that dropout works for LSTMs only when it is applied to the non-recurrent connections, between layers and before the output. Applying it to the recurrent state erases memory too fast.

### From theory to code

Implement `nonrecurrent_dropout(h, mask, p)`, the inverted dropout applied to a non-recurrent activation.

### Constraints

- The mask is supplied by the caller.

### Hints

<details>
<summary>Hint 1</summary>

Multiply by the mask and divide by one minus the drop probability.

</details>

## Theory

### The simple version

Keeping the recurrent path clean lets the cell carry information across many steps, while dropout between layers still regularizes the model.

### The formula

$$\tilde h = \frac{m \odot h}{1 - p}, \qquad \text{applied to } h^{l-1}_t \to h^{l}_t \text{ only}$$

### How NumPy/PyTorch actually implements this

PyTorch's `nn.LSTM(dropout=...)` applies dropout between stacked layers, the same placement the paper uses.

## Explanation

The expectation over masks equals the input, so inference needs no change.
