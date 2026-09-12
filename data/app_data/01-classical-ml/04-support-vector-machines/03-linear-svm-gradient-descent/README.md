---
name: support-vector-machines-linear-svm-gradient-descent
title: Linear SVM via gradient descent on hinge loss
tags: [classic-ml]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`Margin maximization intuition` defined exactly what an SVM wants: the decision boundary with the largest possible margin to its nearest points. Real SVM solvers usually reach that boundary via a different route entirely (quadratic programming on the problem's "dual" formulation, the classic textbook approach), but there's a much simpler path that reuses everything this curriculum has already built: treat "maximize the margin, subject to correct classification" as an ordinary loss-minimization problem, plug it into the same gradient descent machinery `Full Training Loop` already uses, and let optimization find the answer directly.

`Hinge loss` supplies exactly the right loss for this: minimizing it directly pushes toward correct, confidently-margined predictions, and adding an L2 penalty on the weights (this question's contribution) is precisely what connects "small weights" back to "large margin," `geometric_margin`'s own formula divides by `||weight||`, so keeping `||weight||` small, for a given functional margin, is mathematically the same thing as making the geometric margin large.

### From theory to code

Theory combines mean hinge loss with an L2 penalty into a single scalar objective, derives its (sub)gradient (hinge loss's kink at the margin boundary makes the gradient piecewise, exactly zero for comfortably-correct points, a specific nonzero contribution for margin-violating points), and trains by plain gradient descent, reusing `Full Training Loop`'s own loop structure.

Implement `svm_objective(weight, bias, X, y, lambda_reg)` first, then `svm_gradient(weight, bias, X, y, lambda_reg)`, then `train_linear_svm(input, target, lr=0.01, epochs=1000, lambda_reg=0.01)`.

### Constraints

- `target` is `{-1, +1}` (`Hinge loss`'s own convention throughout this track).
- `svm_gradient` must match `svm_objective`'s true gradient (verify with a finite-difference check before trusting it).
- `train_linear_svm` uses plain gradient descent, the same loop shape `Full Training Loop` and `Full Linear Regression Training Loop` both use.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`svm_objective` is one line, calling the already-imported `hinge_loss` and adding `lambda_reg * np.dot(weight, weight)`.

</details>

<details>
<summary>Hint 2</summary>

`svm_gradient`'s "which points violate the margin" mask is `(target * scores) < 1`; only those points contribute to the hinge-loss part of the gradient, everything else contributes zero.

</details>

## Theory

### The simple version

Optimizing "widest possible street between two groups" sounds like it needs a fundamentally different kind of math than the gradient descent this curriculum has used throughout. It doesn't, phrase "widest street" as a LOSS to minimize instead (hinge loss penalizes points inside or on the wrong side of the street, an L2 penalty rewards a narrower `weight` vector, which per `Margin maximization intuition`'s own formula corresponds to a WIDER street for the same functional margin), and the exact same walk-downhill machinery this curriculum has used since `Full Linear Regression Training Loop` finds the answer.

### The formula

The soft-margin SVM objective:

```text
svm_objective = mean(hinge_loss(scores, target)) + lambda_reg * ||weight||^2
```

Its gradient, derived piece by piece: the L2 term's gradient is the familiar `2 * lambda_reg * weight` (`Stretch: L2 Regularization (Ridge)`'s own gradient formula). Hinge loss's gradient is piecewise, since `max(0, 1 - margin)` has a kink exactly at `margin = 1`:

```text
d(hinge_loss_i)/d(weight) = 0                  if margin_i >= 1  (comfortably correct)
                           = -target_i * x_i    if margin_i < 1   (violates the margin)
```

averaged over every point, plus the L2 term's contribution:

```text
grad_weight = mean(-target_i * x_i, over margin-violating points only) + 2 * lambda_reg * weight
grad_bias   = mean(-target_i, over margin-violating points only)
```

This piecewise structure is the direct gradient-descent echo of `Margin maximization intuition`'s "support vectors are the only points that matter" property: points comfortably past the margin (`margin >= 1`) contribute EXACTLY zero to the gradient, only the margin-violating points (the ones closest to, or on the wrong side of, the boundary) push the weights around at all.

### How PyTorch actually implements this

`sklearn.svm.LinearSVC` and `sklearn.linear_model.SGDClassifier(loss="hinge")` both support optimizing exactly this objective (the latter using gradient-descent-family methods directly, the same approach this question builds by hand), an alternative to the classical dual quadratic-programming solvers most SVM textbooks present first. This gradient-descent-on-hinge-loss framing is also precisely why SVMs and neural networks aren't as different as they might first appear, a linear SVM is, mechanically, `linear` plus `hinge_loss` plus L2 regularization plus gradient descent, the exact same four ingredients (a linear layer, a loss function, a regularizer, an optimizer) that build every neural network in this curriculum's Deep Learning parts, just with a different choice of loss function standing in for cross-entropy.

## Explanation

`svm_objective` calls the imported `hinge_loss` on `X @ weight + bias` against `y`, and adds `lambda_reg * np.dot(weight, weight)`, the L2 penalty term, exactly the formula from Theory.

`svm_gradient` computes each point's margin (`target * scores`), builds a mask of margin-violating points (`margin < 1`), and averages `-target * X` over exactly those points (zero contribution from everything else) to get `grad_weight`, adding `2 * lambda_reg * weight`; `grad_bias` is the same margin-violating average of `-target` alone.

`train_linear_svm` runs plain gradient descent for `epochs` steps, calling `svm_gradient` and updating `weight`/`bias` each time, the same loop shape `Full Training Loop` uses.
