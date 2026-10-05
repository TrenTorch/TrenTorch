---
name: dl-tensor-gradient-tracking
title: 'Gradient Tracking (.requires_grad)'
tags: [deep-learning, tensor-ops]
difficulty: Beginner
---

## Statement

Enable gradient computation with .requires_grad. Build computation graphs. Call .backward() to compute gradients. Access gradients via .grad. Understand autograd mechanics.

## Theory

### .requires_grad enables backpropagation

Tensors with requires_grad=True build computation graphs:

`python
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x + 1
y.backward()
print(x.grad)          # dy/dx = 2*x + 3 = 7
`

### Computation graph

Each operation creates a node in the graph (chain rule):

`x (requires_grad=True)
  ↓ (** 2)
x²
  ↓ (+ 3*x)
x² + 3*x
  ↓ (+ 1)
y = x² + 3*x + 1`

Backward traces this graph to compute dy/dx.

### Multiple outputs

`python
x = torch.randn(3, requires_grad=True)
y = x.sum() # Scalar output
y.backward() # Computes dy/dx for all elements

z = x ** 2 # Vector output
z.backward(torch.ones_like(z)) # Scalar weight for each element
`

### Detaching from graph

`python
x = torch.randn(5, requires_grad=True)
y = x ** 2
z = y.detach()             # z doesn't require gradients
`

### Why gradient tracking matters

- Core of deep learning: optimize parameters via gradients
- Automatic differentiation: don't compute gradients manually
- Efficiency: backprop is typically O(1-2x) forward pass cost
- Debugging: print intermediate gradients to detect issues

## Explanation

Solutions enable gradient tracking, build computation graphs, compute gradients via backward(), and access results via .grad. Key insight: gradients accumulate; use .zero_grad() between batches.
