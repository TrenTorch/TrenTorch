---
name: research-double-descent-regime
title: 'Deep Double Descent: Which Regime Is It In?'
tags: [research-papers, classical-ml, learning-theory, double-descent]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Double descent has three regimes. Below the interpolation threshold (parameters fewer than samples), test error is U-shaped. At the threshold it peaks. Beyond it, error falls again, so bigger models can generalize better.

### From theory to code

Implement `double_descent_regime(n, p)`, returning the regime name for `n` samples and `p` parameters.

### Constraints

- The interpolation threshold is exactly `p == n`.

### Hints

<details>
<summary>Hint 1</summary>

Compare `p` with `n` in order.

</details>

## Theory

### The simple version

The peak at the threshold is where the model can just barely fit the training data, which forces it to use large, unstable weights. Beyond the threshold there are many interpolating solutions, and training finds a smooth one.

### The formula

$$\text{regime} = \begin{cases} \text{under} & p < n \\ \text{interpolation} & p = n \\ \text{over} & p > n \end{cases}$$

### How NumPy/PyTorch actually implements this

Experiment logs record `p` and `n` in the same way when sweeping model width.

## Explanation

This classification is the basic bookkeeping behind the paper's figures, which plot test error against model size with this threshold marked.
