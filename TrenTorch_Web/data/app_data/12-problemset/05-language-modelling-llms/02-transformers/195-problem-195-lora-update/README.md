---
name: problem-195-lora-update
title: 'LoRA Update'
tags: [problemset, transformer-llm, fine-tuning-and-peft]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'fine tuning and PEFT'
hint: 'B @ (A @ x)'
tools: [NumPy]
---

## Statement

Compute the LoRA low-rank update of a layer's output: $B\,(A\,x)$, where `A` has shape `(r, d_in)`, `B` has shape `(d_out, r)` and `x` is an input vector (or a matrix with one input per column). Return only the update, not the base layer output.

Implement `solve(x, A, B)`.

**Returns.** Return a NumPy array of shape `(d_out,)` for a vector input.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [[1.0, 1.0], [2.0, 0.0]])
```

Output:

```text
[3.0, 2.0]
```

**Example 2**

Input:

```python
solve([1.0, 1.0], [[0.0, 0.0]], [[5.0], [6.0]])
```

Output:

```text
[0.0, 0.0]
```

## Theory

### The simple version

Fine-tuning a huge weight matrix $W$ is expensive. LoRA freezes $W$ and learns only a small correction $\Delta W=BA$, a product of two thin matrices with a tiny inner dimension $r$. The adapted layer computes $Wx+BAx$, and the extra parameters are only $r(d_{in}+d_{out})$.

### The formula

$$h=Wx+\underbrace{B(Ax)}_{\text{LoRA update}}$$

## Explanation

Multiplying `A @ x` first gives a short vector of length $r$, so the cost is far lower than forming the full $d_{out}\times d_{in}$ matrix $BA$. When `A` is all zeros (second example) the update is zero, which is how LoRA starts training in practice (one of the two factors is initialised to zero).
