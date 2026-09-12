---
name: dl-training-muon
title: Muon
tags: [optimization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`Adam: full update rule` scales each parameter's step by its OWN historical gradient magnitude, but treats every entry of a weight matrix independently, entry-by-entry, with no notion that the matrix as a WHOLE has a shape and a structure (rows, columns, singular directions). For 2D weight matrices specifically (the vast majority of a transformer's parameters), this leaves real structure on the table: some directions in weight-space matter far more than others for how the layer actually transforms its input, and Adam's per-entry scaling doesn't distinguish between them.

Muon (short for "MomentUm Orthogonalized by Newton-schulz") takes a different, matrix-aware approach: instead of adapting each entry independently, it takes the momentum-accumulated update (a full matrix) and ORTHOGONALIZES it, rescaling it so every one of its singular values moves toward `1`, before using it to step. This has the effect of treating every "direction" the update wants to move in roughly equally, rather than letting a few dominant directions (large singular values) drown out the rest, the same "normalize before combining" spirit `04-feature-scaling`'s standardization applies to input features, applied here to an optimizer's own update matrix instead.

### From theory to code

Theory uses a fast, fixed-coefficient iterative approximation (a specific quintic polynomial map, applied a handful of times) to push a matrix's singular values toward `1` cheaply, using only matrix multiplications, no actual SVD ever computed. This is deliberately NOT run to full convergence, a few steps get most singular values substantially closer to `1` than they started, which is all Muon's update actually needs.

Implement `newton_schulz_orthogonalize(G, steps=5, eps=1e-7)` first, then `muon_step(param, grad, momentum_buf, lr, momentum=0.95)` on top of it.

### Constraints

- `newton_schulz_orthogonalize` must handle tall, wide, AND square matrices, always returning a result the same shape as `G`.
- Normalize `G` by its Frobenius norm (`np.linalg.norm(G)`) before iterating.
- `muon_step` accumulates momentum first (`SGD + Momentum`'s own formula), THEN orthogonalizes the resulting momentum buffer, never the raw gradient directly.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

If `G` has more rows than columns, transpose it before iterating (working on the "tall" orientation internally), then transpose the result back before returning, so the output always matches `G`'s original shape.

</details>

<details>
<summary>Hint 2</summary>

The iteration itself is: `A = X @ X.T`, `B = b*A + c*(A@A)`, `X = a*X + B@X`, repeated `steps` times, with `(a, b, c) = (3.4445, -4.7750, 2.0315)`.

</details>

## Theory

### The simple version

Imagine a rowing team where a few rowers are pulling far harder than everyone else, the boat lurches in whatever direction those few dominant rowers happen to be pulling, and the weaker rowers' contributions barely register. "Equalizing" everyone's effort, so every rower contributes roughly the same amount regardless of how hard they'd naturally pull, produces steadier, more evenly-distributed progress. Orthogonalizing an update matrix does something structurally similar: it rescales the update so every one of its underlying "directions" (singular values) contributes roughly equally, instead of letting a few dominant directions overwhelm the rest.

### The formula

Given a matrix `G` (Muon's momentum buffer), the Newton-Schulz iteration approximately orthogonalizes it:

```text
X = G / ||G||_F                      -- normalize by Frobenius norm first
repeat `steps` times:
    A = X @ X.T
    B = b*A + c*(A @ A)               -- (a, b, c) = (3.4445, -4.7750, 2.0315)
    X = a*X + B @ X
```

This specific quintic polynomial (fifth-degree in `X`, chosen and tuned for exactly this purpose) pushes every singular value of `X` toward `1` faster than a simpler iteration would, without ever computing an actual SVD (which would be far more expensive to run every single optimizer step). Crucially, it does NOT converge to exact orthogonality in the handful of steps (`5`, by default) Muon actually runs it for, singular values end up SUBSTANTIALLY closer to `1` than they started, not landed exactly on `1`. That's a deliberate design choice, not a bug: getting closer is all a useful update needs, and running more steps to reach full convergence would cost more compute for a difference that, in practice, doesn't meaningfully change how well the optimizer trains.

Muon's full update:

```text
new_momentum_buf = momentum * momentum_buf + grad     -- SGD + Momentum's own formula
update           = newton_schulz_orthogonalize(new_momentum_buf)
new_param         = param - lr * update
```

### How PyTorch actually implements this

Muon (introduced by Keller Jordan and collaborators) has seen rapid, genuine adoption for training large transformer models specifically on their 2D weight matrices (embeddings, biases, and other non-matrix parameters typically still use AdamW alongside it, a hybrid approach), reported to reach competitive results with meaningfully fewer total training steps in several published speed-run results. It isn't (yet) part of PyTorch's own `torch.optim`, third-party implementations (matching the same Newton-Schulz core this question builds) are what practitioners currently use. It represents a genuinely different philosophy from Adam's per-entry adaptive scaling: treat a weight matrix as a MATRIX, not just a flat bag of independent numbers, and shape the optimizer's update accordingly.

## Explanation

`newton_schulz_orthogonalize` normalizes `G` by its Frobenius norm, transposes to the "tall" orientation if needed (more rows than columns after transposing, so the iteration always operates on a consistent shape), runs the quintic update `steps` times, and transposes back before returning, guaranteeing the result matches `G`'s original shape.

`muon_step` updates the momentum buffer exactly like `SGD + Momentum`'s own formula, orthogonalizes that buffer via `newton_schulz_orthogonalize`, and steps the parameter opposite the orthogonalized result, scaled by `lr`.
