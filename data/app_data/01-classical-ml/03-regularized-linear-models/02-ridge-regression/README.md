---
name: regularized-linear-models-ridge-regression
title: Ridge Regression (L2)
tags: [classical-ml, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Linear Regression: closed form (Normal Equation)` solves for the EXACT weights that minimize training error, no compromise, whatever fits the training data best, wins. But `Generalization: train/val split and the generalization gap` already showed why "fits training data best" and "generalizes well" aren't the same goal: with enough features relative to data, the exact solution can chase every quirk in the training set, including noise, producing large, unstable weights that fit training data perfectly but generalize badly.

Ridge regression adds a second term to the objective: alongside "minimize prediction error," ALSO "keep the weights small." This tension, between fitting the data and staying simple, is regularization's whole idea, and Ridge specifically penalizes weights by their SQUARED magnitude, which (conveniently) keeps the problem exactly as solvable in closed form as plain linear regression was.

### From theory to code

Theory modifies the Normal Equation with one additional term, a small multiple of the identity matrix added before inverting, that shrinks every weight toward zero proportional to a tunable strength, `alpha`.

Implement `ridge_regression_closed_form(input, target, alpha=1.0)` against that reasoning, reusing `Linear Regression: closed form (Normal Equation)`'s own augmented-matrix structure.

### Constraints

- Augment `input` with a bias column, exactly like the plain Normal Equation.
- The regularization penalty applies to the WEIGHTS only, never the bias (the identity matrix's last diagonal entry must be `0`, not `alpha`).
- `alpha=0` should recover the plain Normal Equation's answer exactly.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Build the penalty matrix as `alpha * np.eye(d + 1)`, then explicitly zero out its very last diagonal entry (the bias position).

</details>

<details>
<summary>Hint 2</summary>

The rest of the formula is `Linear Regression: closed form (Normal Equation)`'s own `(X^T X)^-1 X^T y`, with `X^T X` replaced by `X^T X + penalty`.

</details>

## Theory

### The simple version

Fitting a curve through a handful of noisy data points with a model flexible enough to hit every point exactly usually produces a wild, wiggly curve, technically a perfect fit to the training points, but obviously not what's "really" going on, and a terrible predictor for any new point. Telling the fitting process "match the data well, but ALSO keep your parameters small and boring unless the data really justifies otherwise" tends to produce a much more sensible, better-generalizing curve. That's exactly what ridge regression's penalty term does.

### The formula

Ridge regression modifies plain linear regression's loss by adding an L2 penalty on the weights:

```text
ridge_loss = mse_loss(prediction, target) + alpha * sum(weight_i^2)
```

Setting this modified loss's gradient to zero and solving (the same derivation `Linear Regression: closed form (Normal Equation)` performs, with one extra term) gives a closed form nearly identical to the plain Normal Equation:

```text
theta = (X^T @ X + alpha * I) @ X^T @ y
```

with `I`'s last diagonal entry zeroed out so the bias term is excluded from the penalty (conventionally, you don't want to discourage the model from learning a genuinely useful baseline offset, only from relying too heavily on any individual FEATURE). `alpha` controls the tradeoff directly: `alpha = 0` recovers plain linear regression exactly; larger `alpha` shrinks every weight further toward zero, trading a little training-set fit for (often) meaningfully better generalization, exactly the train/val tradeoff `Generalization: train/val split and the generalization gap` introduced.

Adding `alpha * I` before inverting has a second, purely numerical benefit worth knowing: it makes the matrix being inverted strictly better-conditioned (`Positive-definite matrices, and why they matter for optimization`'s own vocabulary: adding a positive multiple of the identity to any matrix pushes every eigenvalue up by `alpha`, guaranteeing a genuinely invertible, well-behaved result even when the unregularized `X^T X` is singular or nearly so, `Matrix inverse, and when it does not exist`'s own scenario).

### How PyTorch actually implements this

`sklearn.linear_model.Ridge` uses exactly this closed-form solution (via an efficient factorization rather than a literal matrix inversion, for numerical stability at scale). In deep learning specifically, `Stretch: L2 Regularization (Ridge)`'s own gradient-based version is what actually gets used, `torch.optim`'s `weight_decay` parameter (seen throughout the Optimizers track) applies precisely this same L2 penalty during gradient-based training, since neural networks have no closed-form solution to fall back on the way plain linear/ridge regression does. `08-map-estimation`'s own connection (Math & Statistics) is worth remembering here too: L2 regularization is mathematically equivalent to placing a Normal prior on the weights and finding the MAP estimate instead of the plain maximum likelihood estimate, `alpha` plays exactly the role `prior_precision` played there.

## Explanation

`ridge_regression_closed_form` augments `input` with a bias column exactly like the plain Normal Equation, builds the penalty matrix `alpha * np.eye(d+1)` with its last diagonal entry zeroed (excluding the bias), and solves `(X^T X + penalty)^-1 X^T y`, splitting the result into `weight` and `bias` the same way `Linear Regression: closed form (Normal Equation)` does.
