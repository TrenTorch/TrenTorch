---
name: eval-normalized-expected-cost
title: 'Normalized expected cost for a classifier'
tags: [classical-ml, evaluation, cost-sensitive, cost-curves, decision-making]
difficulty: Advanced
---

## Statement

### Summarize a classifier's cost over every operating point

Drummond and Holte (2006) showed that a classifier's error rates are only meaningful together with the class prior and the cost of each error. The normalized expected cost (NEC) turns a classifier at one operating point into a number between 0 and 1, where 0 is a perfect classifier and 1 is a trivial one.

With false negative rate `FNR`, false positive rate `FPR`, and the normalized positive-class cost fraction

`PC = p * C_FN / (p * C_FN + (1 - p) * C_FP)`,

the NEC is `NEC = FNR * PC + FPR * (1 - PC)`.

Implement `normalized_expected_cost(fnr, fpr, pos_prior, cost_fn, cost_fp)` and return the NEC as a float.

### Constraints

- `fnr` and `fpr` are in `[0, 1]`. Otherwise raise `ValueError`.
- `pos_prior` is strictly between 0 and 1.
- `cost_fn` and `cost_fp` are strictly positive.
- Do not modify any inputs (they are scalars, so this only means no hidden state).

### Hints

<details>
<summary>Hint 1</summary>

Compute `PC` first. Then the NEC is a weighted average of the two error rates, weighted by `PC` and `1 - PC`.

</details>

## Theory

A single error rate hides how much each mistake costs. The NEC folds the class prior and the cost ratio into one normalized weight `PC`, so the same pair of error rates can be good or bad depending on the deployment. With equal costs and a balanced prior, `PC = 0.5` and the NEC is the average of the two error rates. Cost curves plot the NEC against `PC` for all thresholds, which shows where each classifier wins.

### Where this shows up in production

Fraud and medical screening teams use cost-weighted error because a missed case and a false alarm have very different business costs. The NEC gives a single number to compare two thresholds on the same model, and the cost curve shows which operating region each candidate is best in.

### Using it to make decisions

Start from a real estimate of the cost ratio, such as the expected loss from a missed fraud case versus the review cost of a false alarm. Pick the threshold that minimizes the NEC at that `PC`, then check it against the rates you expect in production, since the prior drifts. If the cost ratio is uncertain, plot the cost curve and choose a threshold that performs well across the plausible range, not just at the point estimate.

### Pros and cons

**Pros:** explicit about cost and prior, normalized so it is comparable across problems, and it extends naturally to full cost curves.

**Cons:** needs a defensible estimate of the cost ratio, which is often the hardest part, it assumes costs are constant across cases, and it summarizes a single operating point unless you plot the whole curve.

## Explanation

The solution computes the normalized positive weight from the prior and the costs, then averages the two error rates by that weight. Keeping the weight normalized is what makes the result fall in `[0, 1]` regardless of the cost scale.
