---
name: research-prelu-forward
title: 'Parametric ReLU: Learning the Negative Slope'
tags: [research-papers, activation, relu]
difficulty: Beginner
---

## Statement

### The problem, from first principles

ReLU sets every negative input to zero, which kills gradients for those units. Parametric ReLU (He et al., 2015) keeps a small learnable slope `a` for negative inputs, so those units still carry signal and gradient.

### From theory to code

Implement `prelu(x, a)`, which returns `x` for positive entries and `a * x` for non-positive ones.

### Constraints

- `a` is a float; `a = 0` gives ordinary ReLU.

### Hints

<details>
<summary>Hint 1</summary>

`np.where(x > 0, x, a * x)` applies the rule element-wise in one call.

</details>

## Theory

### The simple version

The output is linear in each region, with slope 1 for positive inputs and slope `a` for negative inputs. Learning `a` lets the network choose the negative slope from data.

### The formula

$$\text{PReLU}(x) = \begin{cases} x & x > 0 \\ a\,x & x \le 0 \end{cases}$$

### How NumPy/PyTorch actually implements this

`torch.nn.PReLU(num_parameters, init=0.25)` learns exactly this slope and implements the same forward rule.

## Explanation

`prelu` applies element-wise, matching the paper's per-channel or per-layer slope. Taking the zero case to match ReLU makes the function a strict generalization of ReLU.
