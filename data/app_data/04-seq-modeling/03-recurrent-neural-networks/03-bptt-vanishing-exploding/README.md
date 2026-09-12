---
name: seq-rnn-bptt-vanishing-exploding
title: 'Backprop through time (BPTT): vanishing and exploding gradient intuition'
tags: [nlp, neural-networks, training-dynamics]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[02-rnn-cell-backward]`'s Theory section named the concern directly: `grad_h_prev = grad_z @ weight_hh` means that walking a gradient backward through `N` time steps of an RNN multiplies it by `weight_hh` a total of `N` times, once per step. `[03-dl-training/05-why-deep-networks-work/03-vanishing-exploding-gradients]` demonstrated this SAME compounding-multiplication effect for DEPTH, a fresh random matrix per layer, and found that even a modest per-layer scale factor compounds catastrophically across enough layers. Backpropagation Through Time (BPTT), the standard algorithm for training an RNN, has this EXACT same structural vulnerability, but with one crucial difference worth making precise: it's not `N` DIFFERENT random matrices multiplied together, it's the exact SAME `weight_hh` matrix, multiplied by itself `N` times in a row (`weight_hh^N`, in matrix-power notation).

This distinction matters mathematically: repeatedly multiplying by the SAME matrix is exactly the setup behind the "power iteration" method from linear algebra, and it has a sharp, well-understood consequence: as `N` grows large, `weight_hh^N` becomes increasingly DOMINATED by `weight_hh`'s single largest-magnitude eigenvalue (its "spectral radius"). If that spectral radius is less than 1, `weight_hh^N` shrinks toward the zero matrix, gradients vanish. If it's greater than 1, `weight_hh^N` grows without bound, gradients explode. This is WHY vanilla RNNs are notoriously difficult to train on long sequences, and it's the exact motivation behind `LSTM cell, forward (gating mechanism)` and `GRU cell, forward (simplified gating)`, both immediately following this question: both architectures were specifically designed with gated pathways that let gradients flow backward WITHOUT necessarily being repeatedly multiplied by the same weight matrix at every single step.

### From theory to code

Implement `bptt_gradient_norms(seq_len, weight_hh, grad_h_final)`, starting from the LAST time step's gradient and repeatedly multiplying by the SAME `weight_hh` matrix `seq_len` times (simplifying away the `tanh` derivative term from `[02-rnn-cell-backward]`'s full formula, to isolate `weight_hh`'s own compounding effect specifically), recording the gradient's norm after every step.

### Constraints

- `weight_hh` must be reused, UNCHANGED, at every single step (unlike `[03-dl-training/05-why-deep-networks-work/03-vanishing-exploding-gradients]`'s `matrix_gradient_norms`, which deliberately drew a FRESH random matrix per layer).
- The returned list must have length `seq_len + 1`: the starting norm, followed by one entry per step.
- Must demonstrate BOTH failure modes for an appropriately scaled `weight_hh`: a small-magnitude matrix causes the norm to vanish toward zero across enough steps; a large-magnitude matrix causes it to explode.

### Hints

<details>
<summary>Hint 1</summary>

Start with `grad_h = grad_h_final` and `norms = [float(np.linalg.norm(grad_h))]` (the norm BEFORE any steps, matching the `seq_len + 1` length requirement).

</details>

<details>
<summary>Hint 2</summary>

`for _ in range(seq_len): grad_h = grad_h @ weight_hh; norms.append(float(np.linalg.norm(grad_h)))`, the SAME `weight_hh`, read fresh from the function's own argument (never redrawn or modified), applied at every iteration.

</details>

## Theory

### The simple version

An echo bouncing back and forth between two parallel walls, where each bounce either amplifies the sound slightly (if the walls happen to reflect more energy than they absorb) or dampens it slightly (if they absorb more than they reflect). A SINGLE bounce barely changes the echo's volume either way, but after hundreds of bounces between the exact SAME two walls, even a tiny amplification or dampening per bounce compounds into either a deafening roar or complete silence. `weight_hh`, applied identically at every single BPTT step, is exactly this pair of walls: the SAME transformation, over and over, whose tiny per-step effect compounds explosively (or vanishingly) over a long enough sequence.

### The formula

```
grad_h_0 = grad_h_final
grad_h_{k+1} = grad_h_k @ weight_hh                for k = 0, ..., seq_len-1
```

After `N` steps, `grad_h_N = grad_h_final @ weight_hh^N` (repeated multiplication by the SAME matrix is literally matrix exponentiation). As `N -> infinity`, `weight_hh^N`'s behavior is governed almost entirely by `weight_hh`'s dominant eigenvalue `lambda_max`: `||weight_hh^N|| ~ |lambda_max|^N`, exactly the same `layer_scale^depth` compounding formula `[03-dl-training/05-why-deep-networks-work/03-vanishing-exploding-gradients]`'s `scalar_gradient_chain` demonstrated, except here `lambda_max` (a property of the RECURRENT weight matrix) plays the role `layer_scale` played there.

### How PyTorch actually implements this

`torch.nn.RNN`'s (or `RNNCell`'s, chained across a sequence) backward pass, when called via `loss.backward()`, performs exactly this repeated same-matrix multiplication automatically, as part of unrolling the recurrence backward through time. This structural vulnerability is precisely why vanilla RNNs, in practice, struggle to learn dependencies spanning more than a few dozen time steps, and it's the DIRECT motivation behind both `LSTM cell, forward (gating mechanism)` and `GRU cell, forward (simplified gating)`: both architectures introduce an ADDITIVE (rather than purely multiplicative) pathway for the cell state to flow backward through time (an LSTM's cell state update includes a term that's added, not multiplied, controlled by learned "gates" that can, when useful, let a gradient flow backward through many steps almost entirely UNCHANGED), directly sidestepping the repeated-multiplication-by-the-same-matrix problem this question demonstrates numerically. `[03-dl-training/01-optimizers/07-gradient-clipping]`'s `clip_grad_norm` remains a standard practical safeguard specifically for the EXPLODING half of this problem, even with gated architectures.

## Explanation

`bptt_gradient_norms` starts with `grad_h = grad_h_final` and records its norm, then loops `seq_len` times: on each iteration, it multiplies `grad_h` by the SAME `weight_hh` matrix (`grad_h = grad_h @ weight_hh`, never redrawing or modifying `weight_hh` between iterations) and records the resulting norm. Because the identical matrix is reused at every step, the resulting sequence of norms reflects `weight_hh`'s own repeated-power behavior, dominated increasingly by its largest eigenvalue's magnitude as `seq_len` grows, small eigenvalue magnitudes (below 1) drive the norm toward zero (vanishing), and large ones (above 1) drive it toward infinity (exploding), a sharper, matrix-power-driven version of the same compounding effect `[03-dl-training/05-why-deep-networks-work/03-vanishing-exploding-gradients]` demonstrated for depth with fresh matrices per layer.
