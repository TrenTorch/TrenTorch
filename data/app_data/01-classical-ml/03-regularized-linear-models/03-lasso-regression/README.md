---
name: regularized-linear-models-lasso-regression
title: 'Lasso Regression (L1), contrasted against Ridge'
tags: [classical-ml, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Ridge Regression (L2)` shrinks every weight toward zero, but rarely all the way TO zero, a feature that's only weakly useful still ends up with a small, nonzero coefficient. Sometimes what you actually want is different: not just "smaller weights," but genuine feature SELECTION, automatically zeroing out the features that don't matter at all, leaving a sparse, more interpretable model. Swapping Ridge's squared penalty (`sum(weight^2)`) for an absolute-value penalty (`sum(|weight|)`) produces exactly this behavior, and this swap is precisely the difference between Ridge and Lasso.

The cost of that swap: unlike Ridge, Lasso's penalty has no smooth derivative at exactly zero (the whole point, its kink AT zero is what makes weights land exactly there), which means the elegant closed-form Normal-Equation-style solution Ridge enjoys simply doesn't exist for Lasso. A different algorithm, coordinate descent, is needed instead.

### From theory to code

Theory introduces the soft-thresholding operator (the exact solution to a ONE-coordinate version of the Lasso problem), then coordinate descent: repeatedly solve for one weight at a time, holding all others fixed, cycling through every coordinate for several passes until the weights settle.

Implement `soft_threshold(x, threshold)` first, then `lasso_regression_coordinate_descent(input, target, alpha=1.0, epochs=200)` on top of it.

### Constraints

- Center `input` and `target` (subtract their means) before the coordinate descent loop; recover the bias afterward, don't penalize it directly.
- `soft_threshold` must produce EXACT zeros for inputs within `threshold` of zero, not just small values.
- Return `(weight, bias)` in the same `(1, in_features)`/`(1,)` shapes the other regression questions use.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`soft_threshold(x, t) = np.sign(x) * np.maximum(np.abs(x) - t, 0.0)`, a direct translation of the formula.

</details>

<details>
<summary>Hint 2</summary>

For each coordinate `j`, compute the PARTIAL residual (target minus the prediction from every OTHER coordinate), correlate it with feature `j`, and soft-threshold that correlation by `alpha` to get the new `weight[j]`.

</details>

## Theory

### The simple version

Ridge's penalty is like a gentle, continuous tax on every weight, larger weights pay more tax, but even a tiny weight still gets taxed a tiny bit, no reason to ever drop to exactly zero. Lasso's penalty behaves differently right at zero: it's the difference between a smoothly increasing tax and a tax with a genuine "free zone" near zero, small enough weights get taxed away entirely, landing at EXACTLY zero rather than merely small. That qualitative difference, a kink at zero instead of a smooth curve, is precisely what makes Lasso perform automatic feature selection while Ridge does not.

### The formula

Lasso's loss adds an L1 penalty instead of Ridge's L2:

```text
lasso_loss = mse_loss(prediction, target) + alpha * sum(|weight_i|)
```

Because `|weight|` has no derivative at exactly `weight = 0`, there's no single "set the gradient to zero and solve" formula the way Ridge's smooth penalty allows. Coordinate descent solves this differently: fix every weight except one, and for THAT single coordinate, the optimal update has an exact, closed-form answer, the **soft-thresholding operator**:

```text
soft_threshold(x, t) = sign(x) * max(|x| - t, 0)
```

This shrinks `x` toward zero by `t`, and if `x` was already within `t` of zero, the result is EXACTLY `0`, not just small, this is the mechanism that produces Lasso's sparse, feature-selecting solutions. Cycling through every coordinate, updating each one to its optimal value given the current state of all the others, and repeating for several passes (epochs), converges to the true Lasso solution, a general technique (coordinate descent) that works whenever a joint optimization problem is easy to solve one variable at a time even though it lacks a single closed form for all variables together.

### How PyTorch actually implements this

`sklearn.linear_model.Lasso` uses exactly this coordinate descent algorithm (with additional convergence acceleration tricks for speed at scale). Deep learning almost never uses Lasso's L1 penalty directly during training (L2/weight decay, seen in the Optimizers track, is far more common, since it composes cleanly with gradient descent, while L1's non-smooth penalty needs special handling like `torch.nn.utils.prune`'s structured pruning techniques or proximal gradient methods to get the same exact-sparsity benefit gradient descent doesn't provide automatically). Where L1-style sparsity DOES appear directly in deep learning: `torch.nn.utils.prune` and post-training sparsification techniques explicitly zero out small weights after training, achieving via an explicit, separate step what Lasso achieves automatically, as a side effect of its penalty's shape, during optimization itself.

## Explanation

`soft_threshold` returns `np.sign(x) * np.maximum(np.abs(x) - threshold, 0.0)`, the direct formula from Theory.

`lasso_regression_coordinate_descent` centers `input` and `target` by their means, then runs `epochs` full passes over every coordinate: for coordinate `j`, it computes the partial residual (target minus the prediction from every OTHER coordinate), correlates it with feature `j` (normalized by `n`), and applies `soft_threshold` with `alpha` to get the new value of `weight[j]`, dividing by feature `j`'s own normalized sum of squares. After the loop, the bias is recovered from the uncentered means: `bias = y_mean - x_mean @ weight`.
