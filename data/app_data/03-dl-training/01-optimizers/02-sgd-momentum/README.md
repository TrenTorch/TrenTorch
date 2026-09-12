---
name: dl-training-sgd-momentum
title: SGD + Momentum
tags: [optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Plain `SGD` steps directly opposite whatever the CURRENT gradient happens to be, every single step, with zero memory of any earlier step. On a loss surface that curves much more steeply in one direction than another (an "ill-conditioned" surface, `Positive-definite matrices, and why they matter for optimization`'s own vocabulary applies here too), this makes SGD zigzag: it overcorrects across the steep direction on every step while crawling painfully slowly along the shallow direction, wasting most of its movement on oscillation rather than genuine progress toward the minimum.

Momentum fixes this with an idea borrowed directly from physics: instead of responding only to the instantaneous gradient, accumulate a "velocity" that builds up over consecutive steps pointing in a consistent direction, and gets partially cancelled out by steps that keep flip-flopping. A ball rolling downhill doesn't instantly reverse direction the moment the slope changes sign, it has momentum, and that's exactly the behavior this optimizer borrows.

### From theory to code

Theory maintains one extra piece of state per parameter, its velocity, blends the current gradient into that velocity (weighted by a `momentum` coefficient), and steps opposite the BLENDED velocity instead of the raw gradient.

Implement `sgd_momentum_step(params, grads, velocities, lr, momentum=0.9)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `velocities` is a separate list, parallel to `params`/`grads`, that must be threaded through from one call to the next (a training loop calls this once per step, carrying the returned velocities into the next call).
- Return `(new_params, new_velocities)`, both as new lists.
- `momentum` defaults to `0.9`, matching a common real-world default.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Update the velocity FIRST: `new_velocity = momentum * velocity + grad`.

</details>

<details>
<summary>Hint 2</summary>

Then step using the NEW velocity, not the raw gradient: `new_param = param - lr * new_velocity`, exactly `SGD`'s own formula with `velocity` standing in for `grad`.

</details>

## Theory

### The simple version

Pushing a shopping cart down a bumpy aisle, responding INSTANTLY to every tiny bump in the floor (swerving hard left, then hard right, then left again) wastes energy zigzagging and makes little forward progress. Letting the cart build up some momentum, so it keeps rolling roughly straight even through a few small bumps, gets it down the aisle far more efficiently, the bumps still nudge its direction a little, but they don't instantly override the cart's accumulated forward motion. SGD with momentum applies exactly this physical intuition to gradient descent.

### The formula

```text
velocity_new = momentum * velocity_old + grad
param_new    = param - lr * velocity_new
```

`velocity` is a running, exponentially-weighted average of RECENT gradients (`momentum` close to `1`, like the common default `0.9`, weighs many past gradients into the average; `momentum = 0` recovers plain `SGD` exactly, with no memory at all). When consecutive gradients point in roughly the same direction, they reinforce each other in the velocity, accelerating movement in that direction, exactly the "ball keeps rolling straight" behavior. When consecutive gradients keep flipping sign (the zigzag), they partially cancel each other out in the velocity, damping the oscillation that plain SGD would otherwise suffer on an ill-conditioned loss surface.

### How PyTorch actually implements this

`torch.optim.SGD(momentum=momentum)` implements exactly this update (this question's implementation matches it precisely, across multiple consecutive steps, verified directly). PyTorch's optimizer stores each parameter's velocity (called the "momentum buffer" internally) as part of the optimizer's own state dict, exactly why `velocities` needs to be threaded through explicitly here, in a real training loop, `optimizer.step()` reads and updates that buffer automatically behind the scenes, but the underlying state it's managing is precisely the `velocities` list this question makes explicit. Momentum is also the conceptual ancestor of `Adam: full update rule` (the next real optimizer question in this track): Adam maintains its OWN momentum-like running average of gradients (its "first moment"), plus a second, separate running average tracking gradient MAGNITUDE, to additionally adapt the effective learning rate per parameter.

## Explanation

`sgd_momentum_step` first computes `new_velocities` by blending each parameter's old velocity with its current gradient (`momentum * v + grad`), then computes `new_params` by stepping each parameter opposite its OWN new velocity, scaled by `lr`, exactly the two-line formula from Theory, returning both updated lists.
