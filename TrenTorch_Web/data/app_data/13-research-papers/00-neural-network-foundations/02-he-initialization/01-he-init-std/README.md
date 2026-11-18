---
name: research-he-init-std
title: 'He Initialization: The Standard Deviation Rule'
tags: [research-papers, initialization, relu]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Deep ReLU networks lose signal scale layer by layer. ReLU zeroes half of its inputs, so the variance halves at each layer unless the weights are scaled to compensate.

### From theory to code

Implement `he_init_std(fan_in)`, the standard deviation of the weight distribution for a layer with `fan_in` inputs.

### Constraints

- `fan_in` is a positive integer.

### Hints

<details>
<summary>Hint 1</summary>

Variance should be `2 / fan_in`, so the standard deviation is its square root.

</details>

## Theory

### The simple version

For a ReLU layer, half of the pre-activations are zeroed, which halves the second moment. Doubling the weight variance cancels that loss, keeping activation variance stable from layer to layer.

### The formula

$$\text{Var}(W) = \frac{2}{n_{\text{in}}}, \qquad \sigma = \sqrt{\frac{2}{n_{\text{in}}}}$$

### How NumPy/PyTorch actually implements this

`torch.nn.init.kaiming_normal_(w, nonlinearity='relu')` uses this same rule with `mode='fan_in'`.

## Explanation

The standard deviation is the square root of the variance. `n_in` is the number of inputs feeding each output unit, which is the number of columns in the weight matrix.
