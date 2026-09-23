---
name: regularized-linear-models-polynomial-features
title: 'Polynomial features: expanding inputs before a linear model'
tags: [classical-ml, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`linear` (this curriculum's very first question) can only ever compute weighted SUMS of its inputs, it fundamentally cannot represent a curve, no matter how it's trained. `Feature engineering: deriving a feature that makes the model's job easier` (Math & Statistics) already showed one fix: hand-derive a specific nonlinear feature (`radius_feature`) when you know exactly what shape the data needs. Polynomial feature expansion generalizes that idea into something systematic, instead of hand-picking one clever feature, generate EVERY power and cross-product of your existing features up to some degree, and let a plain linear model choose which of those (now numerous) features actually matter.

`07-evaluation/03-bias-variance-tradeoff`'s own `polynomial_features` already did this for a SINGLE input variable. This question generalizes it to MULTIPLE features at once, which introduces a genuinely new kind of term that a single-variable expansion never needs: INTERACTION terms, products of two DIFFERENT features (`x0 * x1`), not just powers of one feature alone (`x0^2`).

### From theory to code

Theory enumerates every monomial (a product of input features raised to some powers) of total degree `0` through `degree`, using `itertools.combinations_with_replacement` over feature indices, the systematic way to generate "every way to multiply some number of features together, repeats allowed, order doesn't matter."

Implement `polynomial_features_multivariate(X, degree)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `X` is `(n, num_features)`, any number of features, not just one.
- Output columns must be ordered by degree first (`0`, then `1`, then `2`, ...), then by `combinations_with_replacement` order within each degree, matching `sklearn.preprocessing.PolynomialFeatures`' own column ordering exactly.
- Degree `0` always produces exactly one column, all `1`s (the bias/intercept term).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

For each degree `d` from `0` to `degree`, loop over `combinations_with_replacement(range(num_features), d)`, each combination is a tuple of feature indices (possibly repeated) to multiply together.

</details>

<details>
<summary>Hint 2</summary>

For a combination like `(0, 0, 1)`, the resulting column is `X[:, 0] * X[:, 0] * X[:, 1]`, start from a column of ones and multiply in each feature named in the combination.

</details>

## Theory

### The simple version

A single number, "square footage," probably has a roughly linear relationship with house price, more square footage, proportionally more value. But "square footage" and "number of bedrooms" TOGETHER might interact in a way neither explains alone, a huge house with very few bedrooms (an unusual, maybe undesirable layout) behaves differently from a huge house with proportionally many bedrooms. A plain linear model, given only the two raw numbers, can't represent that interaction at all, it can only weight each feature independently. Adding a new feature, literally `square_footage * bedrooms`, computed once ahead of time, gives the linear model exactly the extra piece of information it needs to represent that interaction, without changing the model itself at all.

### The formula

For a single feature, `07-evaluation/03-bias-variance-tradeoff`'s expansion generates `[1, x, x^2, x^3, ..., x^degree]`. For MULTIPLE features (`x0, x1, ..., x_{k-1}`), the full expansion generates every MONOMIAL of total degree `0` through `degree`, a product of some (possibly repeated) subset of the features:

```text
degree 0: 1
degree 1: x0, x1, ..., x_{k-1}
degree 2: x0^2, x0*x1, ..., x1^2, ..., x_{k-1}^2
... and so on up to the requested degree
```

`itertools.combinations_with_replacement(range(num_features), d)` generates exactly this list systematically: every way to choose `d` feature indices, with repeats allowed (so `x0^2` comes from choosing index `0` twice) and order not mattering (`x0*x1` and `x1*x0` are the same monomial, only generated once). This is precisely why a degree-2 expansion of `k` raw features produces `x0^2`, `x0*x1`, `x1^2`, and so on, both the pure-power terms `07-evaluation/03-bias-variance-tradeoff`'s single-variable version already covers AND every cross-feature interaction term that a multi-feature expansion adds on top.

The real tradeoff worth knowing: the number of generated features grows FAST (combinatorially) with both the number of raw features and the requested degree, which is exactly why polynomial expansion is almost always paired with regularization (`Ridge Regression (L2)`, `Lasso Regression (L1), contrasted against Ridge`, `Elastic Net`, all three questions immediately preceding this one in this track): with many more features than data points, an unregularized fit would badly overfit (`Generalization: train/val split and the generalization gap`'s own concern), regularization keeps the now much-larger feature set under control.

### How PyTorch actually implements this

`sklearn.preprocessing.PolynomialFeatures` implements exactly this expansion (this question's implementation matches its column ordering exactly, verified directly against it), a standard classical-ML preprocessing step used specifically to let a fast, simple, well-understood linear model capture nonlinear relationships without needing a neural network at all. Deep learning generally sidesteps this entirely: a hidden layer with a nonlinear activation (`02-deep-learning-core`'s ReLU, GELU, etc.) can, in principle, learn arbitrary nonlinear feature combinations directly from raw inputs (the Universal Approximation idea, covered later in the Deep Learning Training part), without a human enumerating every polynomial term by hand. Polynomial features remain genuinely useful specifically where interpretability matters (you can name exactly which interaction term a nonzero coefficient corresponds to) or where data is too scarce to let a more flexible model learn the right nonlinearity on its own.

## Explanation

`polynomial_features_multivariate` loops over every degree `d` from `0` to `degree`, and for each degree, over every `combinations_with_replacement(range(num_features), d)`, building each resulting column by starting from a column of ones and multiplying in every feature named in that combination, then stacking every generated column, in that exact degree-then-combination order, into the final result.
