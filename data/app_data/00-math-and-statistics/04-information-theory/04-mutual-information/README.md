---
name: math-mutual-information
title: Mutual information between two variables
tags: [information-theory]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`03-probability`'s correlation measures whether two variables move together LINEARLY, and can be exactly zero even when two variables are strongly, deterministically related in a curved way (`y = x^2`, say). What you actually want, much of the time, is a measure of "how much does knowing X tell you about Y," with no assumption about linearity at all. That's mutual information: it's zero if and only if X and Y are genuinely, completely independent (knowing one tells you literally nothing about the other), and it grows the more knowing X narrows down what Y could be, no matter what shape that relationship takes.

The elegant part, and the reason this question sits at the very end of both the Probability and Information Theory tracks: mutual information is built entirely from tools you've already implemented, it is literally `03-kl-divergence`'s KL divergence, applied to compare the real joint distribution against what that same joint distribution WOULD look like if X and Y had no relationship at all.

### From theory to code

Theory defines mutual information as `KL(P(X,Y) || P(X)*P(Y))`: the real joint distribution, compared against the "independent" joint you'd get by multiplying the two marginals together (`03-probability/04-conditional-probability`'s `marginal_x`/`marginal_y`). Build that hypothetical independent joint via an outer product, then measure the KL divergence between the two, flattened into matching 1D distributions.

Implement `mutual_information(joint, base=2.0)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `joint` is a 2D array, `joint[i, j] = P(X=i, Y=j)`, summing to `1.0`.
- Must use `marginal_x`/`marginal_y` (already imported) to build the independent joint, not compute it any other way.
- Must reuse `kl_divergence` (already imported), not reimplement its formula.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.outer(px, py)` builds exactly the `(len(px), len(py))` table you'd expect from two independent variables with those marginals.

</details>

<details>
<summary>Hint 2</summary>

`kl_divergence` expects two flat distributions of matching shape. `.flatten()` both 2D tables before passing them in.

</details>

## Theory

### The simple version

Suppose you separately know "40% of days are rainy" and "30% of days have bad traffic." If rain and traffic were totally unrelated, you'd expect rainy-AND-bad-traffic days to happen `0.4 * 0.3 = 12%` of the time, by pure chance. If the ACTUAL fraction of rainy-and-bad-traffic days is much higher than that (say 25%), that gap is telling you something real: knowing it rained genuinely helps you predict traffic. Mutual information measures exactly the size of that gap, summed properly across every possible pairing of outcomes, not just the one example.

### The formula

```text
MI(X; Y) = KL(P(X, Y) || P(X) * P(Y))
```

`P(X) * P(Y)` (the outer product of the two marginals, `03-probability/04-conditional-probability`'s own `marginal_x`/`marginal_y`) is exactly what the joint distribution WOULD be if X and Y were independent (independence is defined as `P(X, Y) = P(X) * P(Y)` for every pair). `KL divergence (03-kl-divergence)` between the real joint and this hypothetical independent joint measures exactly how far reality is from independence.

This gives mutual information two properties correlation lacks: it's `>= 0` always (KL divergence's own guarantee), exactly `0` if and only if X and Y are TRULY independent (not just linearly uncorrelated), and it can detect ANY kind of dependence, linear or not, since it's built from the full joint distribution rather than a single linear-fit statistic.

### How PyTorch actually implements this

Mutual information (or differentiable approximations of it, like InfoNCE, seen later in this curriculum's contrastive-learning content) is the training objective behind self-supervised representation learning: a model learns representations by maximizing the mutual information between two augmented "views" of the same input, forcing it to capture information that's genuinely shared between them (the underlying content) rather than incidental noise specific to one view. Feature selection pipelines (`scikit-learn`'s `mutual_info_classif`/`mutual_info_regression`) use exactly this quantity to rank which input features carry the most information about a target variable, without assuming any particular (e.g. linear) relationship shape, a real, practical alternative to correlation-based feature selection when the relationship might be nonlinear.

## Explanation

`mutual_information` computes both marginals via the imported `marginal_x`/`marginal_y`, builds the hypothetical independent joint via `np.outer(px, py)`, and returns `kl_divergence` between the real `joint` and that independent joint, both flattened into matching 1D arrays first, exactly the formula from Theory, expressed entirely in terms of functions already built in earlier questions.
