---
name: linear-regression-l1-loss-mae
title: 'Stretch: L1 Loss (MAE), contrasted against MSE'
tags: [classical-ml, linear-regression, loss-functions]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Mean Squared Error Loss squares every error before averaging, which means one prediction that's wildly off (a data-entry error in the target, a genuinely unusual house that sold for 10x its neighbors) can dominate the entire loss and drag the fitted line toward accommodating that single outlier, at the expense of fitting everything else well. Mean Absolute Error takes the error's magnitude directly, no squaring, and behaves very differently in exactly this situation.

This question asks: implement L1 loss, then understand precisely why swapping MSE for L1 changes how a model responds to outliers, the same robustness distinction `02-imputing-missing-values` and `01-outlier-detection` (Math & Statistics) already introduced for mean vs. median.

### From theory to code

Theory gives the direct formula (mean of `|input - target|`, not squared). Implement it with the exact same reduction-mode signature `Mean Squared Error Loss` already established, so both losses are drop-in interchangeable in a training loop.

Implement `l1_loss(input, target, reduction="mean")` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input` and `target` share a shape; any shape is valid, not just 2D.
- `reduction`: `"mean"` (default), `"sum"`, or `"none"`, raise `ValueError` for anything else.
- No squaring anywhere, this is absolute error, not squared error.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.abs(input - target)` replaces MSE Loss's `(input - target) ** 2`, everything else about the reduction logic is identical.

</details>

<details>
<summary>Hint 2</summary>

Copy `Mean Squared Error Loss`'s three-branch reduction structure directly, only the elementwise error formula changes.

</details>

## Theory

### The simple version

Ten houses sell for prices clustered around $300k, and one sells for $3 million (a genuine mansion, correctly recorded, just unusual). Fit a line minimizing SQUARED error, and that one mansion's error gets squared into a huge number, the fit distorts noticeably to reduce that one giant squared term, at real cost to how well it fits the other nine houses. Fit minimizing ABSOLUTE error instead, and that same house contributes proportionally to its error, big, but not squared-big, the fit stays much closer to what's "typical" for the other nine.

### The formula

```text
l1_loss(input, target) = mean(|input - target|)
```

compared against `Mean Squared Error Loss`'s:

```text
mse_loss(input, target) = mean((input - target)^2)
```

Squaring an error of `10` gives `100`; squaring an error of `2` gives `4`, a 25x difference from a 5x difference in the raw errors. This is precisely why MSE is outlier-sensitive and L1 is comparatively robust: MSE's squaring amplifies large errors disproportionately, while L1's absolute value scales linearly no matter how large the error gets. This is the exact same mean-vs-median-style robustness tradeoff `01-outlier-detection` and `02-imputing-missing-values` (Math & Statistics) already introduced, applied here to a loss function instead of a summary statistic.

The tradeoff has a real cost too: L1's gradient (a later, more advanced treatment would derive `04-gradient-clipping`-style considerations here) is a constant `+1`/`-1` regardless of how large the error is, whereas MSE's gradient shrinks toward zero as the prediction gets close to the target (`03-mse-gradient`'s own `2*(prediction-target)/n`), giving MSE smoother, more stable convergence behavior near the optimum, one reason MSE remains the more common default despite its outlier sensitivity.

### How PyTorch actually implements this

`torch.nn.functional.l1_loss` (this question's exact target) and `torch.nn.L1Loss` are real, commonly-used alternatives to MSE specifically when a dataset has known outliers or heavy-tailed noise. `torch.nn.SmoothL1Loss` (closely related to `09-huber-loss`, the next question in this track) exists as a middle ground precisely because real practitioners often want L1's outlier-robustness far from the optimum AND MSE's smooth gradient behavior near it, rather than being forced to choose one extreme or the other.

## Explanation

`l1_loss` computes `np.abs(input - target)` (absolute error, not squared), then reduces via the identical `"mean"`/`"sum"`/`"none"` branching `Mean Squared Error Loss` already established, raising `ValueError` on an unrecognized reduction mode.
