---
name: dl-training-vanishing-exploding-gradients
title: 'Vanishing and exploding gradients: why a deep, badly-initialized net fails to train'
tags: [neural-networks, theory, initialization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[02-layers/04-weight-initialization]` derived Xavier and Kaiming initialization from the requirement "keep activation variance roughly constant across layers." This question demonstrates, numerically, exactly what goes wrong if you DON'T: `[02-layers/02-linear-backward]`'s `linear_backward` shows that backpropagating a gradient through one layer involves multiplying by that layer's weight matrix. Chain many layers together, and the gradient reaching an early layer has been multiplied by EVERY layer's weight matrix in between, one after another. If each individual multiplication happens to shrink the gradient's magnitude even slightly (say, by a factor of 0.9), the CUMULATIVE effect across, say, 50 layers is `0.9^50`, an almost unimaginably tiny number, meaning early layers receive a gradient signal so close to zero that gradient descent essentially can't move them at all: they stop learning. The mirror-image failure, if each multiplication instead slightly GROWS the gradient (a factor of 1.1), compounds to `1.1^50`, an enormous number, which manifests as training instability, `nan` losses, or wildly oscillating weights (exactly what `[03-dl-training/01-optimizers/07-gradient-clipping]`'s `clip_grad_norm` was built to guard against).

This is a fundamentally MULTIPLICATIVE, compounding effect, and that's precisely why it becomes catastrophic specifically for DEEP networks: a shallow, 2-3 layer network barely notices a per-layer factor of 0.9 or 1.1, but a 50-layer network experiences an effect that's roughly `factor^50`, astronomically far from `factor^1`.

### From theory to code

Implement `scalar_gradient_chain(depth, layer_scale)`, the simplest possible model: `layer_scale` raised to the `depth`-th power, representing what happens if every layer scales the gradient by the exact same fixed factor. Then implement `matrix_gradient_norms(depth, dim, weight_std, rng)`, a more realistic simulation: start with a gradient vector of all `1`s, and at each of `depth` layers, multiply it by a FRESH random `(dim, dim)` weight matrix with entries drawn from `N(0, weight_std^2)` (exactly the kind of matrix `[02-layers/04-weight-initialization]`'s formulas are designed to scale correctly), tracking the gradient vector's norm after every layer.

### Constraints

- `scalar_gradient_chain` computes `layer_scale ** depth` exactly.
- `matrix_gradient_norms` must return a list of length `depth + 1`: the starting norm (before any layers), followed by the norm after each of the `depth` layers.
- Each layer in `matrix_gradient_norms` must use a FRESH random weight matrix (drawn via the passed-in `rng`), not the same matrix reused across every layer.
- `matrix_gradient_norms` must genuinely demonstrate BOTH failure modes: a small `weight_std` should cause the norm to shrink toward zero across depth, and a large `weight_std` should cause it to grow explosively.

### Hints

<details>
<summary>Hint 1: scalar_gradient_chain</summary>

`layer_scale ** depth`: Python's `**` operator handles this in one line, `layer_scale=0.9, depth=50` gives approximately `0.00515`, a dramatic shrinkage from the starting value of `1.0`.

</details>

<details>
<summary>Hint 2: matrix_gradient_norms setup</summary>

Start with `grad = np.ones(dim)` and `norms = [float(np.linalg.norm(grad))]` (the STARTING norm, before any layer is applied, this is why the result has `depth + 1` entries, not `depth`).

</details>

<details>
<summary>Hint 3: The loop</summary>

`for _ in range(depth): weight = rng.randn(dim, dim) * weight_std; grad = weight @ grad; norms.append(float(np.linalg.norm(grad)))`. A FRESH `weight` is drawn inside the loop body on every iteration (via `rng`, not `np.random` directly), simulating each layer having its own independently-initialized weights.

</details>

## Theory

### The simple version

A rumor passed hand-to-hand down a long line of people, where each person, before repeating it, either exaggerates it slightly or downplays it slightly. If everyone consistently exaggerates even a LITTLE, by the end of a long enough line the "rumor" has become an absurd, wildly inflated claim; if everyone consistently downplays it even a little, by the end it's shrunk to an inaudible whisper, effectively lost. Only if each person repeats it at very close to its original volume does the message survive a long chain intact, exactly the property good weight initialization is designed to guarantee for gradients flowing backward through a deep network.

### The formula

Simplified scalar model:

```
final_gradient_magnitude = layer_scale ^ depth
```

`layer_scale < 1` -> vanishing (shrinks toward 0 as depth grows); `layer_scale > 1` -> exploding (grows toward infinity as depth grows); `layer_scale = 1` -> stable (the ideal case good initialization aims for).

More realistic vector/matrix model, over `depth` layers each with a random `(dim, dim)` weight matrix:

```
grad_0 = initial gradient
grad_{i+1} = weight_i @ grad_i          for i = 0, ..., depth-1
```

The NORM of `grad_depth` relative to `grad_0`'s norm reflects the same compounding effect as the scalar model, but now driven by the weight matrices' actual singular values (their own "scale factor" per layer) rather than a single hand-picked scalar.

### How PyTorch actually implements this

PyTorch itself doesn't "solve" vanishing/exploding gradients directly (it's a property of the ARCHITECTURE and initialization, not something the framework can automatically fix), but several standard tools this curriculum covers exist specifically because of this problem: `[02-layers/04-weight-initialization]`'s Xavier/Kaiming schemes choose `weight_std` specifically so that, ON AVERAGE across a whole layer, the multiplicative effect stays close to `1` rather than compounding away from it; `[03-dl-training/01-optimizers/07-gradient-clipping]`'s `clip_grad_norm` handles the EXPLODING case directly and reactively, capping a gradient's magnitude after it's already grown too large, regardless of why; and residual/skip connections (used throughout modern architectures, including transformers, covered later in this curriculum) sidestep the problem architecturally, by giving the gradient a direct, UN-multiplied path backward through the network (`grad_x = grad_output` for the skip branch, bypassing the compounding weight multiplications entirely), which is widely credited as the single biggest reason very deep networks (ResNets with over 100 layers, and transformers far deeper still) became trainable at all.

## Explanation

`scalar_gradient_chain` computes `layer_scale ** depth` directly, showing the raw compounding effect of a CONSTANT per-layer scale factor across `depth` layers.

`matrix_gradient_norms` starts `grad = np.ones(dim)` and records its norm, then loops `depth` times: on each iteration, draws a fresh `(dim, dim)` weight matrix from `N(0, weight_std^2)` via `rng.randn(dim, dim) * weight_std`, multiplies it into `grad`, and records the new norm. Because a FRESH random matrix is drawn at each layer (rather than reusing one matrix), the resulting sequence of norms reflects the same compounding multiplicative effect the scalar model captures, but grounded in the actual singular-value behavior of random matrices at the chosen `weight_std`, small values of `weight_std` drive the norm toward zero across depth (vanishing), and large values drive it toward infinity (exploding).
