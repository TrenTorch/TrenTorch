---
name: dl-activation-prelu
title: 'PReLU'
tags: [deep-learning, activations]
difficulty: Beginner
---

## Statement

Master the PReLU activation function: f(x) = x if x>0 else αx (α learnable). Adaptive Leaky ReLU. Implement forward and backward passes. Understand when to use it.

## Theory

### What it does

This activation function transforms inputs to enable non-linearity, essential for deep networks to learn complex patterns.

### Output range and gradient properties

Different activations have:
- Different output ranges (ReLU: [0, ∞), Sigmoid: (0, 1), Tanh: (-1, 1))
- Different gradient behavior (sharp vs smooth, saturating vs non-saturating)
- Different computational cost (ReLU: cheap, GELU: moderate)

### Dead neuron problem

ReLU-family activations can have dead neurons (output always 0, gradient always 0). Leaky/ELU variants mitigate this.

### Normalization interaction

Activation choice affects output distribution:
- ReLU: positive outputs need normalization
- Tanh: roughly centered, helps convergence
- GELU/Swish: smooth, work well with batch norm

## Explanation

The solution implements this activation efficiently, computes gradients correctly, and recognizes scenarios where it excels. Key insight: activation is as important as weight initialization for training dynamics.
