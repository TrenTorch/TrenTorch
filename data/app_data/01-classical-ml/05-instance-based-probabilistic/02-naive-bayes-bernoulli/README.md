---
name: instance-based-probabilistic-naive-bayes-bernoulli
title: 'Naive Bayes: Bernoulli log-likelihood'
tags: [classical-ml, probabilistic, naive-bayes]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-knn` predicts by comparing distances directly — it never asks "how likely is this class, probabilistically." Naive Bayes takes a fully probabilistic approach instead: given a document represented as which words appear in it (`input` entries of `0`/`1`, "does this word appear"), model how likely each class is given those features, and pick whichever class is most likely. The catch is that estimating "how likely are these exact features together, given the class" directly is hopeless — with enough binary features there are more possible feature combinations than there are training examples to have ever seen most of them. Naive Bayes sidesteps this with one deliberately simplifying assumption: treat every feature as independent of every other feature, once you already know the class.

### From theory to code

Theory below derives, from Bayes' rule plus that independence assumption, a log-space formula for how well a class explains a set of features, and how Laplace smoothing keeps that formula from breaking on features that happen to be constant within a class. `bernoulli_nb_fit` estimates the per-class, per-feature probabilities and priors from training data; `bernoulli_log_likelihood` scores one sample's features against one class's probabilities; `bernoulli_nb_predict` combines both to pick the best class per query.

### Constraints

- `input` entries are `0` or `1` (feature present/absent); `labels` can be any set of class values, not necessarily `{0, 1}`.
- `bernoulli_nb_fit(input, labels, alpha=1.0)` returns a `dict` with `"classes"`, `"log_priors"` (a `{class: float}` mapping), and `"feature_probs"` (a `{class: array of shape (n_features,)}` mapping).
- `alpha` is Laplace smoothing strength, added to the numerator; `2 * alpha` (not `alpha`) is added to the denominator when estimating each `feature_probs[c]`.
- `bernoulli_log_likelihood(x, feature_probs)` takes one sample's features (shape `(n_features,)`) and one class's feature probabilities (same shape), returns a single `float`.
- `bernoulli_nb_predict(model, queries)` returns shape `(n_queries,)`, one predicted class per row of `queries`, chosen by highest `log_prior + log_likelihood` score, never by comparing raw (non-log) probabilities.
- Every computation stays in log space once priors and likelihoods are combined — never multiply raw probabilities together, that underflows for more than a handful of features.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`feature_probs[c]` is one array covering every feature at once for class `c` — you don't need a per-feature loop. `input[mask].sum(axis=0)` (where `mask` selects class `c`'s rows) counts, per feature, how many of class `c`'s examples had that feature present.

</details>

<details>
<summary>Hint 2</summary>

`bernoulli_log_likelihood`'s formula has two terms per feature, and exactly one of them is "active" per feature depending on whether `x_i` is `0` or `1`. Instead of branching, multiply each term by `x` or `(1 - x)` — the inactive term gets multiplied by `0` and vanishes on its own.

</details>

<details>
<summary>Hint 3</summary>

`bernoulli_nb_predict` needs to compare each query against *every* class's `(log_prior, feature_probs)` pair and keep the best. Build a list or array of scores across `model["classes"]` for one query, then `np.argmax` picks the winning class index directly.

</details>

## Theory

### The simple version

Imagine sorting emails into spam and not-spam by checking, for each word in your vocabulary, "does this word show up unusually often in spam, or in real mail?" You'd never have seen every possible combination of words together, so instead of trying to model whole emails at once, you just multiply together how suspicious each individual word looks on its own, assuming (naively, but usefully) that a word's presence tells you nothing about whether another word is also present. Whichever category — spam or not — ends up with the higher combined suspicion score after checking every word wins.

### The formula

By Bayes' rule, `P(class | features) ∝ P(features | class) * P(class)`, so the class that maximizes the right-hand side also maximizes the left. The "naive" independence assumption factors `P(features | class)` into a product over features:

```text
P(features | class) = product over every feature i of P(feature_i | class)
```

For binary features, each `P(feature_i | class)` is a Bernoulli probability — "what fraction of class `c`'s training examples had feature `i` present," call it `p_i`. Multiplying many probabilities underflows quickly, so everything moves to log space, turning the product into a sum:

```text
log P(features | class) = sum over features i of [ x_i * log(p_i) + (1 - x_i) * log(1 - p_i) ]
```

where `x_i` is `0` or `1` (this feature's actual value). When `x_i = 1` only the `log(p_i)` term contributes; when `x_i = 0` only `log(1 - p_i)` does — the Bernoulli log-likelihood for one feature, summed across all of them.

`alpha` (Laplace smoothing) fixes a specific failure mode: a feature that happened to be `0` in every training example of some class would get `p_i = 0` exactly, making `log(p_i) = -inf` and permanently ruling out that class the instant the feature is ever seen as `1` — one unlucky small sample shouldn't create absolute certainty. Estimating `p_i` as `(count_present + alpha) / (class_count + 2*alpha)` instead of `count_present / class_count` nudges every estimate slightly toward `0.5` ("genuinely unknown" rather than "impossible").

Final prediction: `argmax` over classes of `log_prior[c] + log P(features | c)`.

### How PyTorch actually implements this

There's no PyTorch module for Naive Bayes — it isn't a differentiable, gradient-trained model, it's a closed-form frequency-counting estimator, so there's nothing here that maps onto an `nn.functional` call. The standard reference implementation is scikit-learn's `sklearn.naive_bayes.BernoulliNB`, and `tests.py`'s `test_matches_real_sklearn_bernoulli_nb_on_a_baked_dataset` bakes in an actual `BernoulliNB(alpha=1.0)` fit/predict run (generated offline, as documented in that test's comment) as ground truth this solution's output is checked against.

## Explanation

`bernoulli_nb_fit` loops once per distinct class (`for c in classes`), computing `log_priors[c] = float(np.log(class_count / n_samples))` — how common this class is overall — and `feature_probs[c] = (input[mask].sum(axis=0) + alpha) / (class_count + 2 * alpha)`, the smoothed fraction of class `c`'s examples that had each feature present, one value per feature computed for every feature at once via `.sum(axis=0)`. `test_fit_feature_probs_use_laplace_smoothing` and `test_smoothing_denominator_is_two_alpha_not_alpha` both check this exact `+alpha` / `+2*alpha` split against hand-computed values.

`bernoulli_log_likelihood` is the formula above translated directly: `float(np.sum(x * np.log(feature_probs) + (1 - x) * np.log(1 - feature_probs)))`. Because `x` is `0` or `1`, one of the two summands is always multiplied by zero and drops out per feature, and `np.sum` collapses the per-feature terms into the single scalar log-likelihood `test_log_likelihood_matches_hand_computation` checks.

`bernoulli_nb_predict` scores every class as `model["log_priors"][c] + bernoulli_log_likelihood(queries[i], model["feature_probs"][c])` inside a list comprehension over `classes`, then `classes[np.argmax(scores)]` picks the class Bayes' rule says is most probable given this query's features. Working entirely in log space means this is a sum, not a product, which is what keeps `bernoulli_nb_predict` numerically stable on `test_smoothing_avoids_zero_probability_for_an_always_absent_feature`'s case, where an unsmoothed model would otherwise hit `log(0)`.
