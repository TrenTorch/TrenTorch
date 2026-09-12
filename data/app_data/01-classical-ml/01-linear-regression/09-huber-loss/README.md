---
name: linear-regression-huber-loss
title: 'Stretch: Huber Loss, quadratic near zero and linear far from it'
tags: [classical-ml, linear-regression, loss-functions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`08-l1-loss-mae` and `Mean Squared Error Loss` sit at two extremes: MSE has smooth, well-behaved gradients but is dragged around by outliers; L1 is outlier-robust but has a constant-magnitude gradient everywhere, including right at the optimum, which can make training oscillate rather than settle smoothly. Huber loss is the deliberate middle ground: behave like MSE (smooth, small gradients) for typical, small errors, and switch to behaving like L1 (bounded, outlier-resistant) once an error crosses a threshold.

The part that makes Huber loss genuinely well-designed, not just "average the two formulas", is that the two branches are chosen specifically so they meet seamlessly at the switch point: same value, same slope, no kink, no discontinuity a gradient-based optimizer would stumble on.

### From theory to code

Theory gives the exact piecewise formula and a threshold `delta` controlling where the switch happens. Implement it directly with `np.where`, reusing the reduction-mode pattern `Mean Squared Error Loss` and `08-l1-loss-mae` both already established.

Implement `huber_loss(input, target, delta=1.0, reduction="mean")` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- The branch boundary uses `<=` for the quadratic case (matching real PyTorch's convention at exactly `|error| == delta`).
- `delta` defaults to `1.0`, matching `torch.nn.functional.huber_loss`'s own default.
- Same `reduction` modes (`"mean"`, `"sum"`, `"none"`) as the other two losses in this track.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute both branches for every element (`0.5 * error**2` and `delta * (abs_error - 0.5*delta)`), then `np.where(abs_error <= delta, quadratic, linear)` picks the right one per element.

</details>

<details>
<summary>Hint 2</summary>

Plug `abs_error = delta` into both formulas by hand: `0.5*delta^2` and `delta*(delta - 0.5*delta) = 0.5*delta^2`, they agree exactly, that's the "seamless" property Theory describes.

</details>

## Theory

### The simple version

Most measurement errors are small and genuinely random noise, worth treating gently (MSE's smooth, proportionally-small penalty near zero handles this well). A few errors are huge and probably signal something unusual, a genuine outlier, a data problem, not "typical" noise worth chasing aggressively (L1's bounded, linear penalty handles this well). Huber loss uses MSE's behavior for the first case and L1's for the second, switching between them at a threshold, `delta`, you choose.

### The formula

```text
error = input - target

huber(error) = 0.5 * error^2                    if |error| <= delta
             = delta * (|error| - 0.5 * delta)   otherwise
```

At exactly `|error| = delta`, both branches agree: `0.5*delta^2` from the quadratic side, `delta*(delta - 0.5*delta) = 0.5*delta^2` from the linear side, the same number. Their SLOPES also agree at that point (the quadratic branch's slope is `delta` there, and the linear branch's slope is a constant `delta` everywhere), which is why Huber loss has no kink: it's smooth, not just continuous, exactly the property that keeps gradient descent well-behaved across the switch point, unlike a naive "just pick whichever of MSE or L1 gives the smaller penalty" would produce.

Smaller `delta` makes Huber loss behave more like L1 (switching to the robust linear branch sooner); larger `delta` makes it behave more like MSE (staying quadratic over a wider range of errors). `delta -> infinity` recovers MSE exactly; `delta -> 0` recovers something proportional to L1.

### How PyTorch actually implements this

`torch.nn.functional.huber_loss` (this question's exact target) and its close cousin `torch.nn.SmoothL1Loss` (differing only by a scale factor, `SmoothL1Loss`'s `beta` parameter plays the same role as `delta` here but the un-normalized formula differs by a factor of `beta`) are both real, commonly-used losses, particularly prominent in object detection models (bounding-box regression is a classic use case: most box-coordinate errors are small, but occasional large errors from a genuinely mis-detected object shouldn't be allowed to dominate training the way squared error would let them).

## Explanation

`huber_loss` computes `error = input - target` and both candidate branches (`0.5 * error**2` and `delta * (abs_error - 0.5*delta)`), then selects per element via `np.where(abs_error <= delta, quadratic_branch, linear_branch)`, exactly the piecewise definition from Theory, before applying the same `"mean"`/`"sum"`/`"none"` reduction logic as `Mean Squared Error Loss` and `08-l1-loss-mae`.
