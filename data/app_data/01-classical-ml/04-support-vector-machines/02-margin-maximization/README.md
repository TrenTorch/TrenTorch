---
name: support-vector-machines-margin-maximization
title: Margin maximization intuition
tags: [classic-ml]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Decision Boundary / Thresholding` drew one line separating two classes, but for most datasets, MANY different lines would separate the two classes equally well, on the training data. Which one should you actually prefer? Support Vector Machines answer this with a specific, principled criterion: prefer the line that sits as FAR as possible from the nearest points of either class, the widest possible "street" between the two classes, rather than a line that happens to squeeze uncomfortably close to some points even while technically separating them correctly.

This question builds the exact quantity SVMs maximize: the margin, the distance from the decision boundary to its single closest point. Understanding this concretely is what makes `Linear SVM via gradient descent on hinge loss` (the next question) make sense as "training an SVM" rather than just "yet another linear classifier with a different loss function."

### From theory to code

Theory defines two related but distinct notions of "margin": the functional margin (a raw, unnormalized number that depends on how large `weight` happens to be) and the geometric margin (the SAME idea, rescaled into an actual, scale-invariant distance). The dataset's overall margin is the SMALLEST geometric margin across every point, whichever point sits closest to the boundary.

Implement `functional_margin(weight, bias, X, y)` first, then `geometric_margin(weight, bias, X, y)` on top of it, then `dataset_margin(weight, bias, X, y)`.

### Constraints

- `y` is `{-1, +1}` (`Hinge loss`'s own convention).
- `geometric_margin` must be invariant to scaling `weight` and `bias` by the same positive constant (Theory explains why this matters).
- `dataset_margin` returns a single scalar: the minimum geometric margin across all points.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`functional_margin` is exactly the same expression `hinge_loss` computes before the `1 -` and `max(0, ...)`: `target * (X @ weight + bias)`.

</details>

<details>
<summary>Hint 2</summary>

Dividing `functional_margin` by `np.linalg.norm(weight)` is what makes it scale-invariant, `dataset_margin` is then just `np.min` over `geometric_margin`'s result.

</details>

## Theory

### The simple version

Draw a line separating red dots from blue dots on paper. If the line barely squeezes between the closest red dot and the closest blue dot, a single new point drawn slightly off from where its neighbors were would very likely land on the WRONG side. Draw the line instead so it sits as far as possible from BOTH groups' nearest points, right down the middle of the widest possible gap, and new points have much more room to land on the correct side even with some natural variation. SVMs formalize "as far as possible from both groups' nearest points" directly as the thing being optimized for.

### The formula

The **functional margin** measures how confidently correct a point is, using the raw, unnormalized score:

```text
functional_margin_i = target_i * (weight . x_i + bias)
```

exactly `Hinge loss`'s own `target * scores` expression. The problem with using this directly as "how far is this point from the boundary": it isn't actually a distance, scaling `weight` and `bias` by `10` (which doesn't move the decision boundary itself at all, the SIGN of `weight . x + bias` is unchanged) multiplies every functional margin by `10` too, a purely cosmetic change masquerading as "more confident."

The **geometric margin** fixes this by dividing out `weight`'s own scale:

```text
geometric_margin_i = functional_margin_i / ||weight||
```

This IS a genuine, scale-invariant distance, in the same units as the input space, from point `i` to the decision boundary. The **dataset margin** is the smallest geometric margin across every point, the distance from the boundary to its single closest correctly-classified point:

```text
dataset_margin = min_i(geometric_margin_i)
```

An SVM's training objective is precisely: find the `(weight, bias)` that MAXIMIZES this `dataset_margin`, subject to every point being correctly classified. The points that end up exactly at that minimum distance, pressed right up against the boundary of the maximum-width "street", are called **support vectors**, they're the only points that actually determine where the boundary sits; every other point could be moved further away without changing the optimal boundary at all.

### How PyTorch actually implements this

`sklearn.svm.SVC`/`LinearSVC` solve this margin-maximization problem directly (usually via its dual formulation, quadratic programming, rather than gradient descent on hinge loss the way `Linear SVM via gradient descent on hinge loss` does, but arriving at the same maximum-margin boundary). The "support vectors are the only points that matter" property is a genuinely distinctive, useful characteristic of this model family: unlike logistic regression (where every training point contributes to the fitted weights), an SVM's solution depends only on the handful of hardest, closest-to-the-boundary examples, everything else is, in a precise sense, irrelevant to where the final boundary ends up.

## Explanation

`functional_margin` computes `target * (X @ weight + bias)`, exactly `Hinge loss`'s own inner expression.

`geometric_margin` divides that by `np.linalg.norm(weight)`, turning it into a scale-invariant distance.

`dataset_margin` takes `np.min` over the result of `geometric_margin`, the closest point's actual distance to the boundary, exactly the quantity Theory names as an SVM's training objective.
