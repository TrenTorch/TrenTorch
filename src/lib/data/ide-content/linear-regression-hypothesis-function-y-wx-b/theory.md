# Theory: The Linear Hypothesis

## What

The hypothesis function is the simplest possible model: `y = wx + b`. One weight, one bias, one straight line. Every more complex model TrenTorch builds later (logistic regression, a `Linear` layer, an entire Transformer) reduces to this same shape, computed many times over.

## Why this shape

A line is the smallest function with two free parameters that can express "some relationship between x and y" while staying differentiable everywhere. Differentiability is what makes gradient descent possible at all: it's what lets you ask "if I nudge `w` a little, how does the loss change?" and get a real, usable answer.

## How it maps onto real PyTorch

This is exactly what `torch.nn.functional.linear` computes for a single input and output feature: `y = x @ w.T + b`. `nn.Linear(1, 1)` is a thin wrapper around that same operation, generalized from scalars to matrices. When TrenTorch's own `Linear` layer shows up later in the curriculum, this is its one-dimensional special case.

## When to use it (and when not to)

Reach for a plain linear hypothesis when the relationship between input and output really is (approximately) linear -- house size vs. price in a narrow range, say. It stops working the moment the true relationship curves: no number of straight lines, on their own, can fit a parabola. That's what nonlinearity (activations, stacked layers) is for, covered later in this curriculum.

## Pros and cons

- **Pros:** trivially interpretable (`w` is "how much `y` changes per unit of `x`"), cheap to compute, and its loss surface is convex -- gradient descent can't get stuck in a bad local minimum.
- **Cons:** can only express linear relationships. Adding more input features helps, but the model stays linear _in its parameters_ regardless.

## At scale

In a real network, this exact operation runs as a matrix multiply (`x @ W.T + b`) across a batch of thousands of examples and thousands of output features at once, on a GPU. The math doesn't change -- it's still `w * x + b` per element -- only the shapes involved, and the hardware executing it, do.
