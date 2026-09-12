---
name: regularized-linear-models-elastic-net
title: 'Elastic Net: combining L1 and L2 penalties'
tags: [classical-ml, regression]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Ridge Regression (L2)` and `Lasso Regression (L1), contrasted against Ridge` each have a real, distinct weakness. Ridge never zeroes out irrelevant features, its shrinkage is smooth but never total. Lasso, when several features are strongly correlated with each other, tends to arbitrarily pick just ONE of them and zero out the rest, even when several of them are genuinely, similarly useful, an unstable, somewhat arbitrary selection that can change dramatically with tiny changes to the data.

Elastic Net asks: why not use both penalties at once, and let a tunable knob control the mix? The result inherits Lasso's genuine sparsity (some weights really do land at exactly zero) while inheriting Ridge's stability when features are correlated (it tends to keep or drop CORRELATED features together, rather than arbitrarily favoring one over the others).

### From theory to code

Theory adds Ridge's L2 term directly into Lasso's own coordinate descent update, reusing `Lasso Regression (L1), contrasted against Ridge`'s `soft_threshold` unchanged and its centering/coordinate-cycling structure unchanged, with one modification to the per-coordinate formula.

Implement `elastic_net_coordinate_descent(input, target, alpha=1.0, l1_ratio=0.5, epochs=200)` against that reasoning.

### Constraints

- `l1_ratio` controls the L1/L2 mix: `l1_ratio=1.0` is pure Lasso, `l1_ratio=0.0` is pure Ridge.
- Reuse the imported `soft_threshold` directly, don't reimplement it.
- Center `input`/`target` exactly like Lasso's own coordinate descent does.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Split `alpha` into two separate penalty strengths: `l1_penalty = alpha * l1_ratio`, `l2_penalty = alpha * (1 - l1_ratio)`.

</details>

<details>
<summary>Hint 2</summary>

The per-coordinate update becomes `soft_threshold(rho_j, l1_penalty) / (z_j + l2_penalty)`, Lasso's own update with `z_j` (the denominator) increased by the L2 penalty.

</details>

## Theory

### The simple version

Imagine two ways of trimming an overgrown hedge: Ridge trims every branch down proportionally, nothing removed entirely, just shorter overall. Lasso cuts entire branches off completely, but if two branches grow right next to each other and are nearly identical, it might arbitrarily cut one down to nothing and leave the other fully intact, an oddly unstable choice given how similar they were. Elastic Net blends the two strategies: it still cuts some branches entirely (Lasso's sparsity), but when branches are similar, it tends to trim them together rather than picking one arbitrarily (Ridge's stability under correlated features).

### The formula

Elastic Net's loss combines both penalties:

```text
elastic_net_loss = mse_loss(prediction, target) + alpha*l1_ratio*sum(|weight_i|) + 0.5*alpha*(1-l1_ratio)*sum(weight_i^2)
```

Coordinate descent's per-coordinate update (the same derivation Lasso uses, with the extra L2 term contributing directly to the denominator instead of the numerator):

```text
weight_j = soft_threshold(rho_j, alpha * l1_ratio) / (z_j + alpha * (1 - l1_ratio))
```

where `rho_j` and `z_j` are exactly Lasso's own partial-residual correlation and normalized sum-of-squares. Setting `l1_ratio = 1.0` makes the L2 term vanish entirely, recovering Lasso's own update exactly; setting `l1_ratio = 0.0` makes the numerator's `soft_threshold` degenerate to plain shrinkage with no exact zeros, recovering something proportional to Ridge's own smooth shrinkage.

The "correlated features" stability Elastic Net is specifically known for comes from that extra `z_j + l2_penalty` denominator: it prevents the update from being AS aggressive about picking exactly one of several similar features, the same smoothing effect Ridge's own penalty produces, now blended into Lasso's otherwise all-or-nothing coordinate updates.

### How PyTorch actually implements this

`sklearn.linear_model.ElasticNet` implements exactly this coordinate descent formula (this question's implementation matches it on real data). In deep learning, combining L1 and L2 penalties directly during gradient-based training is possible but far less common than Ridge's L2-only weight decay (`torch.optim`'s `weight_decay` parameter), since L1's non-smooth term still requires the same special handling (proximal gradient methods, or an explicit thresholding step after each gradient update) that made Lasso itself need coordinate descent rather than plain gradient descent in the first place, one more instance of the same "smooth penalties compose easily with gradient descent, non-smooth ones need extra machinery" pattern this entire regularized-linear-models track has been building toward.

## Explanation

`elastic_net_coordinate_descent` splits `alpha` into an L1 penalty (`alpha * l1_ratio`) and an L2 penalty (`alpha * (1 - l1_ratio)`), then runs the identical centering-and-cycling structure `Lasso Regression (L1), contrasted against Ridge` uses, with one change to the per-coordinate update: `soft_threshold(rho_j, l1_penalty) / (z_j + l2_penalty)`, the L2 penalty folded into the denominator alongside `z_j`.
