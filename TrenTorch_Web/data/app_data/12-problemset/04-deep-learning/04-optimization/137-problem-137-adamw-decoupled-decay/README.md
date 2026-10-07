---
name: problem-137-adamw-decoupled-decay
title: 'AdamW Decoupled Decay'
tags: [problemset, dl-training-theory, optimizers]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'optimizers'
hint: 'Adam step plus lr*wd*w, both subtracted from w'
tools: [NumPy]
---

## Statement

Perform one AdamW update: the Adam step of the previous problem plus **decoupled** weight decay, $w\leftarrow w-\eta\big(\hat m/(\sqrt{\hat v}+\varepsilon)+\lambda w\big)$, where `wd` is $\lambda$ (default $0.01$).

Implement `solve(w, g, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-08, wd=0.01)`.

**Returns.** Return a tuple `(new_w, new_m, new_v)`. Defaults: `lr=0.001`, `beta1=0.9`, `beta2=0.999`, `eps=1e-8`, `wd=0.01`.

### Examples

**Example 1**

Input:

```python
solve([2.0], [1.0], [0.0], [0.0], 1, lr=0.1, beta1=0.0, beta2=0.0, eps=0.0, wd=0.1)
```

Output:

```text
([1.88], [1.0], [1.0])
```

**Example 2**

Input:

```python
solve([1.0], [0.0], [0.0], [0.0], 1, lr=0.1, beta1=0.0, beta2=0.0, wd=0.1)
```

Output:

```text
([0.99], [0.0], [0.0])
```

## Theory

### The simple version

Weight decay shrinks weights toward zero to fight overfitting. In plain Adam, adding an L2 penalty to the loss gets mixed into the gradient and is then rescaled by the adaptive denominator, which makes the decay uneven across parameters. AdamW applies the decay directly to the weights, outside the adaptive step.

### The formula

$$w_t=w_{t-1}-\eta\left(\frac{\hat m_t}{\sqrt{\hat v_t}+\varepsilon}+\lambda\,w_{t-1}\right)$$

## Explanation

With $\beta_1=\beta_2=0$ and $\varepsilon=0$ the Adam part reduces to $\operatorname{sign}(g)$. In the first example: $2-0.1\cdot(1+0.1\cdot2)=1.88$. In the second the gradient is $0$ but the decay still shrinks the weight: $1-0.1\cdot0.1\cdot1=0.99$.
