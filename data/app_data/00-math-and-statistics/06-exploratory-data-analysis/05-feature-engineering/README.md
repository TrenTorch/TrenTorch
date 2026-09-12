---
name: math-feature-engineering
title: "Feature engineering: deriving a feature that makes the model's job easier"
tags: [data-processing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Imagine labeling points as "inside" or "outside" a circle of radius 3, based only on their `(x, y)` coordinates. Individually, `x` alone tells you almost nothing about the label (a point at `x=2` could be inside the circle or far outside it, depending on `y`), and the same goes for `y` alone, `04-data-leakage`'s own correlation check would find both features nearly USELESS on their own, even though the label is entirely determined by `x` and `y` together. A linear model, in particular, genuinely cannot represent "inside a circle" as a straight-line decision boundary in raw `(x, y)` space, no matter how it's trained, the true boundary is curved.

But compute ONE new number, `sqrt(x^2 + y^2)` (distance from the origin), and the exact same problem becomes trivial: "inside the circle" is now just "this single number is less than 3," a problem any linear model handles instantly. That's feature engineering: deriving a new feature from existing ones specifically because it captures the actual structure of the problem in a form the model can use directly, rather than hoping the model discovers that structure on its own from raw, poorly-shaped inputs.

### From theory to code

Theory gives two concrete, common engineered features: distance from the origin (`sqrt(x^2 + y^2)`, useful whenever "how far from center" matters more than raw coordinates) and a ratio between two raw features (useful whenever the RELATIONSHIP between two quantities matters more than either alone).

Implement `radius_feature(x, y)` and `ratio_feature(numerator, denominator)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- Both functions are vectorized: they accept arrays and return arrays of the same shape.
- `radius_feature` always returns non-negative values.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`radius_feature` is a direct translation of the Euclidean distance formula, `sqrt(x^2 + y^2)`.

</details>

<details>
<summary>Hint 2</summary>

`ratio_feature` is a single division, no special handling needed for this question (a real pipeline would guard against `denominator == 0` separately).

</details>

## Theory

### The simple version

Imagine sorting a pile of coins into "inside a 3-inch circle drawn on a table" and "outside it," using only each coin's `(x, y)` position. Looking at the x-coordinate alone tells you almost nothing, a coin at `x=2` might be well inside the circle or way outside, entirely depending on its y-coordinate too. But compute one new number for each coin, its straight-line distance from the circle's center, and the sorting rule becomes trivially simple: "distance less than 3 = inside." The information was always there in `(x, y)`, engineering the distance feature just puts it in the shape the actual rule needs.

### The formula

**Radius (distance from origin)**, useful whenever a label depends on how far a point is from some reference, not its raw coordinates:

```text
radius_feature(x, y) = sqrt(x^2 + y^2)
```

**Ratio**, useful whenever the RELATIONSHIP between two raw quantities matters more than either alone (price and square footage individually say little about "value for money"; their ratio says it directly):

```text
ratio_feature(numerator, denominator) = numerator / denominator
```

The general principle both illustrate: a model (especially a linear one) can only combine its inputs in the ways its own structure allows. `linear`, this curriculum's first question, can only form weighted SUMS of its inputs, it fundamentally cannot compute `x^2 + y^2` or `a / b` on its own, no matter how it's trained. Feature engineering does that nonlinear combination work UPFRONT, by hand, handing the model an input shape it's actually capable of using well. This is precisely why the raw `(x, y) -> circle` problem is unsolvable by a linear model but trivial once `radius_feature` is engineered in, the underlying information didn't change, only its packaging did.

### How PyTorch actually implements this

Hand-engineered features like these were the dominant approach in ML for decades, and remain essential for tabular data and classical models (`01-classical-ml`'s entire section leans on them implicitly). Deep learning's central appeal is largely that it can, in principle, LEARN nonlinear combinations like these automatically: a hidden layer with a nonlinear activation (`02-deep-learning-core`'s ReLU, GELU, etc.) followed by another linear layer can, given enough capacity and data, approximate something like `x^2 + y^2` on its own, without a human deriving it by hand. But this comes at a real cost: more data, more compute, and less certainty the network actually learns the "right" combination rather than some other one that happens to fit the training set. This is why hand-engineered features (this question's `radius_feature`, `ratio_feature`, and their real-world cousins like `07-evaluation/03-bias-variance-tradeoff`'s polynomial features) remain valuable even in the deep learning era, especially when data is scarce or the useful structure is already well understood.

## Explanation

`radius_feature` computes `np.sqrt(x**2 + y**2)`, the direct Euclidean distance formula, vectorized automatically since `x` and `y` are arrays.

`ratio_feature` computes `numerator / denominator` directly, elementwise division.
