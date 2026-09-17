---
name: ensembles-surge-gradient-boosted-trees
title: 'THE SURGE'
tags: [classical-ml, ensembles, gradient-boosting, trees, regularization]
difficulty: Advanced
---

## Statement

**Difficulty:** Medium–Hard
**Topic:** Gradient Boosted Trees (XGBoost-style), Regularized Split Gain, Production ML

---

### Story

You work on the dispatch team at a ride-hailing app. Every few minutes the system needs to
decide how many extra drivers to nudge into each zone before a demand spike hits — arrive
too late and riders wait forever, arrive too early and drivers idle for nothing. Historical
data shows demand is not linear in time-of-day, weather, or nearby event size: it stays flat
for long stretches, then jumps sharply, then plateaus again. That kind of shape is exactly
what gradient boosted regression trees are built for.

You'll implement a minimal but faithful XGBoost-style regressor from scratch — exact greedy
split finding with the regularized gain formula, L2-regularized leaf weights, and
learning-rate shrinkage — and use it to forecast demand at new query points so dispatch can
pre-position drivers before the surge, not after it.

---

### Input Format

```
n d
x_1,1 x_1,2 ... x_1,d y_1
x_2,1 x_2,2 ... x_2,d y_2
...
x_n,1 x_n,2 ... x_n,d y_n
T lambda gamma eta max_depth base_score
m
q_1,1 q_1,2 ... q_1,d
q_2,1 q_2,2 ... q_2,d
...
q_m,1 q_m,2 ... q_m,d
```

- `T` — number of boosting rounds (trees)
- `lambda` — L2 regularization on leaf weights (`≥ 0`)
- `gamma` — minimum gain required to keep a split (`≥ 0`)
- `eta` — learning rate / shrinkage (`0 < eta ≤ 1`)
- `max_depth` — maximum tree depth (root is depth `0`)
- `base_score` — initial prediction for every sample

### Output Format

Print `m` lines: the predicted `ŷ` for each query, with at least 6 digits after the decimal
point.

**Judging:** accepted if within `1e-4` absolute **or** relative error of the reference
solution (whichever is larger). Because split selection is a discrete, exactly-specified
process (fixed tie-breaking rules), the *structure* of every tree is uniquely determined —
there is no ambiguity to cause divergent predictions if you follow the algorithm exactly.

---

### Constraints

- `1 ≤ n ≤ 500`
- `1 ≤ d ≤ 20`
- `1 ≤ m ≤ 500`
- `1 ≤ T ≤ 30`
- `0 ≤ max_depth ≤ 4`
- `0 ≤ lambda ≤ 10^3`, `0 ≤ gamma ≤ 10^3`, `0 < eta ≤ 1`
- All feature values, targets, and `base_score` satisfy `|value| ≤ 10^4`, given with up to 6 decimal digits.
- Time limit: 2 seconds. Memory limit: 256 MB.

---

### Example 1

**Input**
```
4 1
1 1
2 1
3 10
4 10
1 0 0 1 1 0
2
2
3.5
```

**Output**
```
1.000000
10.000000
```

**Explanation:** `T=1`, `lambda=0`, `gamma=0`, `eta=1`, `max_depth=1`, `base_score=0`. With
`pred_i=0` for all, `g_i = -y_i = [-1,-1,-10,-10]`. Testing the three candidate thresholds
(1.5, 2.5, 3.5), the split at `t=2.5` gives the largest gain (`40.5`), separating
`{1,2}` from `{3,4}`. Leaf weights: left `= -(-2)/2 = 1`, right `= -(-20)/2 = 10`. With
`eta=1` these become the predictions directly. Query `x=2` falls left → `1.0`; query
`x=3.5` falls right → `10.0`.

---

### Example 2

**Input**
```
4 1
1 1
2 1
3 10
4 10
2 1 0 0.5 1 0
2
2
3.5
```

**Output**
```
0.555556
5.555556
```

**Explanation:** Same data, but now `T=2` rounds, `lambda=1`, `eta=0.5`. Round 1 again
splits at `t=2.5` (regularization changes the *magnitude* of the gain but not which split
wins here), giving leaf weights `2/3` (left) and `20/3` (right); after shrinkage,
`pred` becomes `1/3` for `{1,2}` and `10/3` for `{3,4}`. Round 2 recomputes gradients from
these new predictions, splits at `t=2.5` again, giving leaf weights `4/9` (left) and `40/9`
(right). Final predictions: left `= 1/3 + 0.5·(4/9) = 5/9 ≈ 0.555556`, right
`= 10/3 + 0.5·(40/9) = 50/9 ≈ 5.555556`.

## Theory

### The Math

You are given `n` training examples, each with `d` real-valued features and a real-valued
target `y_i` (observed ride demand in that zone/window). The loss is **squared error**:

$$
L(y, \text{pred}) = 0.5 \cdot (\text{pred} - y)^2
$$

so for every sample `i` at any point in training, the gradient and hessian w.r.t. its current
prediction are:

$$
g_i = \text{pred}_i - y_i \qquad h_i = 1
$$

(`h_i` is always exactly `1` for squared error and never changes.)

#### Boosting loop

Maintain `pred_i` for every training sample, initialized to a given constant `base_score` for
all `i`. For round `t = 1 .. T`:

1. Compute `g_i = pred_i - y_i` for every training sample (using the *current* `pred_i`).
2. Grow **one regression tree** on the full training set using the algorithm below.
3. For every training sample `i`, let `w_i` be the weight of the leaf it falls into. Update:
   `pred_i ← pred_i + eta * w_i`.
4. Store the tree — it will be needed for predicting query points later.

#### Growing one tree

Start at the root with the full sample set `S` (all `n` samples), depth `0`. At any node with
sample set `S` and depth `k`:

- Let `G = Σ g_i`, `H = Σ h_i = |S|` over `i ∈ S`.
- **The node is a leaf** if `k == max_depth`, or `|S| < 2`, or (after checking all candidate
  splits below) the best candidate split has gain `≤ 0`. A leaf's weight is:

$$
w = \frac{-G}{H + \lambda}
$$

- **Otherwise, find the best split.** For every feature `j = 0 .. d-1`: take the samples in
  `S`, sort their distinct values of feature `j`. For every pair of **adjacent distinct
  values** `a < b` in that sorted list, form the candidate threshold `t = (a + b) / 2`, and
  split `S` into `L = {i ∈ S : x_i,j ≤ t}` and `R = {i ∈ S : x_i,j > t}`. (If feature `j` has
  fewer than 2 distinct values in `S`, it contributes no candidate thresholds.) Compute:

$$
\text{Gain}(j, t) = 0.5 \cdot \left[ \frac{G_L^2}{H_L+\lambda} + \frac{G_R^2}{H_R+\lambda} - \frac{G^2}{H+\lambda} \right] - \gamma
$$

  where `GL, HL, GR, HR` are the `G, H` sums restricted to `L` and `R`.

  Pick the `(j, t)` with the **maximum** `Gain(j, t)` over all features and all candidate
  thresholds. **Tie-breaking:** if several `(j, t)` achieve the exact maximum gain, choose the
  smallest feature index `j` first, then the smallest threshold `t`.

  If this maximum gain is `≤ 0`, the node becomes a leaf (formula above). Otherwise split the
  node on `(j, t)`: build a left child from `L` and a right child from `R`, each at depth
  `k + 1`, recursively.

#### Prediction

For a query feature vector `q`, route it through every one of the `T` trees in order: at each
internal node with split `(j, t)`, go left if `q_j ≤ t`, else right, until reaching a leaf with
weight `w_tree`. The final prediction is:

$$
\hat{y}(q) = \text{base\_score} + \eta \sum_{t=1}^{T} w_{\text{tree}_t}(q)
$$

## Explanation

`build_regression_tree` computes `G = sum(g)` and `H = sum(h)` for the current node, then
returns a leaf (weight `-G/(H+lam)`) if the depth limit or minimum-sample-count is hit.
Otherwise it scans every feature's distinct values, forms the midpoint threshold between each
adjacent pair, computes the regularized gain for splitting there, and keeps whichever
`(feature, threshold)` achieves the strict maximum (iterating features and thresholds in
increasing order with a strict `>` comparison naturally gives the required tie-break). If the
best gain found is at most `gamma`, it returns a leaf instead of splitting; otherwise it
partitions the samples and recurses into left and right children one depth deeper.
`gbdt_predict` maintains a running `pred` array starting at `base_score`, and for each of `T`
rounds recomputes gradients from the *current* predictions, grows one tree via
`build_regression_tree`, and shrinks every training sample's prediction by `eta` times the
leaf weight it routes to. Predicting a query replays the same per-tree routing (starting from
`base_score` again) and sums the shrunk leaf weights across every stored tree.
