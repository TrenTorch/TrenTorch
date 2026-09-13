---
name: ensembles-adaboost
title: 'AdaBoost: reweighting misclassified samples each round'
tags: [classical-ml, ensembles, boosting]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A single decision stump (a tree of `max_depth=1`) can only ask one question about one feature before it has to commit to an answer. That makes it a weak learner almost by definition — better than a coin flip, but not by much. `03-gradient-boosting-negative-gradient` and `04-full-boosting-loop` already showed one way to chain weak learners into a strong one: fit each new tree to the previous ensemble's residual. AdaBoost, historically the earlier idea, chains weak learners a different way. It never touches what a tree predicts — it changes which training samples the _next_ tree is trained to care about, by making the hard-to-classify samples louder in the training data each round.

### From theory to code

Theory below derives three things: how much to trust a round's tree (`alpha`), how to make the next round pay more attention to this round's mistakes (the weight update), and how to combine every round's tree into one final prediction. `adaboost_train` runs the round loop and produces the list of `(tree, alpha)` pairs; `adaboost_predict` implements the final weighted vote. Neither reimplements tree-building — both call `03-best-split-minimal-tree`'s `build_tree`/`predict_tree` directly.

### Constraints

- `labels` are `{-1, +1}`-valued, AdaBoost's standard convention, not `{0, 1}`.
- `adaboost_train(input, labels, n_rounds, max_depth=1, seed=None)` returns a `list` of exactly `n_rounds` `(tree, alpha)` pairs, one per round, in round order.
- `max_depth=1` by default: a shallow decision stump, AdaBoost's classic weak learner.
- Sample weights start uniform (`1/n_samples`) and must stay a valid probability distribution (renormalized to sum to `1`) after every round's update.
- Resampling for tree training is done via `rng` built once from `seed` before the loop starts, not re-seeded each round, so results are reproducible for a fixed `seed`.
- The weighted error rate must be clipped away from exactly `0` or `1` before it's used in `alpha`'s formula, to avoid `log(0)` or division by zero.
- `adaboost_predict(ensemble, input)` returns an array of `{-1, +1}` predictions, one per row of `input`, never anything else.
- Reuse `03-best-split-minimal-tree`'s `build_tree`/`predict_tree`, don't reimplement tree construction.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The weak learner doesn't train on all the data equally every round — it trains on a _resample_ of the data, drawn according to the current sample weights, so heavily-weighted (hard) samples are more likely to appear multiple times. `np.random.Generator.choice` takes a `p=` argument for exactly this.

</details>

<details>
<summary>Hint 2</summary>

The weighted error rate is not computed on the resample — it's measured by running the freshly-trained tree back over the _full_ original `input`/`labels`, then summing the weights of the samples it got wrong. The resample was just a training-time trick; evaluation needs to reflect every sample's true current importance.

</details>

<details>
<summary>Hint 3</summary>

`labels * predictions` is `+1` wherever a prediction agrees with the true label and `-1` wherever it disagrees — that single elementwise product is the entire "did this sample get harder or easier" signal the weight-update formula needs. Feed it straight into `exp(-alpha * labels * predictions)`.

</details>

## Theory

### The simple version

Think of a study group that gets one true/false question at a time, always from a very simple guesser who can only look at one topic per question. After each question, the group tracks who's still getting the guesser's advice wrong. Wherever guesses have been wrong repeatedly, those specific cases get flagged as "pay more attention here" for the next guesser. A guesser who cleared a genuinely hard batch of confusing cases gets more say in the final answer; a guesser who barely beat a coin flip barely counts at all. The final answer is a vote, weighted by how much each guesser earned that trust.

### The formula

Each round, given the current sample weights `w`:

```text
1. Resample n_samples indices with replacement, using w as sampling probabilities.
2. tree = build_tree(resampled input, resampled labels, max_depth)
3. predictions = predict_tree(tree, full original input)
4. weighted_error = clip(sum(w[predictions != labels]), 1e-10, 1 - 1e-10)
5. alpha = 0.5 * log((1 - weighted_error) / weighted_error)
6. w = w * exp(-alpha * labels * predictions)
7. w = w / sum(w)
```

`alpha` is monotonically decreasing in `weighted_error`: near `0` error, `(1-e)/e` is huge, `alpha` is large and positive; at `weighted_error = 0.5` (chance), the ratio is `1`, `log(1) = 0`, `alpha = 0`, the tree gets no vote; past `0.5` (worse than chance), `alpha` goes negative — the tree's vote is actively inverted.

`labels * predictions` is `+1` when a sample is correctly classified and `-1` when it isn't. So `exp(-alpha * labels * predictions)` is `exp(-alpha)` (shrinks the weight, since `alpha > 0` for a decent learner) on correct samples, and `exp(+alpha)` (grows the weight) on incorrect ones — exactly the "make the next round care more about today's mistakes" mechanism.

Final prediction, across every `(tree_i, alpha_i)` in the ensemble:

```text
sign( sum_i( alpha_i * tree_i(x) ) )
```

a weighted majority vote where more-accurate rounds count for more.

### How PyTorch actually implements this

AdaBoost has no PyTorch tensor-op equivalent — it's a discrete, tree-based ensemble method, not a differentiable computation, so there's nothing here that lowers to an `nn.functional` call the way earlier questions in this curriculum do. The standard reference implementation is scikit-learn's `sklearn.ensemble.AdaBoostClassifier`, which follows the same round structure (resample or reweight, fit a weak learner, compute `alpha`, update weights) implemented here.

## Explanation

`adaboost_train` builds `rng = np.random.default_rng(seed)` once, before the loop, so results are reproducible for a fixed `seed` across separate calls (`test_reproducible_with_the_same_seed` checks exactly this). Each round, `sample_idx = rng.choice(n_samples, size=n_samples, replace=True, p=weights)` draws the resample by weight, and `build_tree(input[sample_idx], labels[sample_idx], max_depth)` trains the round's stump on it — this is what makes the weak learner actually pay more attention to previously-hard samples.

The weighted error, though, is measured on the _full_ original data: `predictions = predict_tree(tree, input)`, `incorrect = predictions != labels`, `weighted_error = np.clip(np.sum(weights[incorrect]), 1e-10, 1 - 1e-10)`. The `np.clip` guards `alpha`'s formula against `log(0)` or a division by zero — an error rate of exactly `0` or `1` is a real edge case a small, discrete decision stump can hit (e.g. `test_a_good_weak_learner_gets_a_positive_alpha`'s easily-separable data, where a perfect stump is plausible).

`alpha = 0.5 * np.log((1 - weighted_error) / weighted_error)` is Theory's formula verbatim. `weights = weights * np.exp(-alpha * labels * predictions)` is the single line that does the reweighting — `labels * predictions` is `+1` when they agree and `-1` when they don't, exactly the mechanism Theory describes. `weights = weights / weights.sum()` renormalizes so `weights` stays a valid distribution for the next round's `rng.choice`. Finally `ensemble.append((tree, alpha))` records the round.

`adaboost_predict` accumulates `scores += alpha * predict_tree(tree, input)` across every `(tree, alpha)` pair — each individual prediction is `-1` or `+1`, scaled by that round's vote strength — then `np.sign(scores).astype(int)` collapses the weighted sum back down to a single `{-1, +1}` decision per row, which is why `test_predictions_are_only_plus_or_minus_one` holds regardless of how many rounds ran.
