---
name: ensemble-q-statistic
title: 'Q-statistic for a pair of classifiers'
tags: [classical-ml, ensembles, diversity, q-statistic]
difficulty: Advanced
---

## Statement

### Are the two classifiers' errors positively or negatively related?

The Q-statistic is a pairwise diversity measure built from the same four counts as disagreement. It compares the chance that both classifiers are right, or both wrong, against the chance that exactly one of them is right.

With `N_11`, `N_10`, `N_01` and `N_00` counting examples by the correctness pattern of the two classifiers (1 means correct), the statistic is

`Q = (N_11 * N_00 - N_01 * N_10) / (N_11 * N_00 + N_01 * N_10)`.

Implement `q_statistic(correct_a, correct_b)`, where both inputs are 1-D boolean or 0/1 arrays of the same length.

- Return `Q` as a float. It lies in `[-1, 1]`: `1` means the errors always coincide, `-1` means the classifiers are never right together and never wrong together.
- If the denominator is zero, raise `ValueError` because `Q` is undefined.

### Constraints

- Both inputs must be 1-D and the same length. Otherwise raise `ValueError`.
- Empty inputs raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Compute the four counts with boolean masks: `a & b`, `a & ~b`, `~a & b`, and `~a & ~b`.

</details>

## Theory

Kuncheva's Q is a correlation-like measure of the joint correctness of two classifiers. A value near 1 means the classifiers succeed and fail on the same examples, so combining them gives little gain. A value near zero or below means their errors are more spread out, which is what voting needs. Because Q is a ratio of products, it is sensitive to the counts in the denominator, and it becomes undefined when one of the two products is zero.

### Where this shows up in production

Q-statistics are used in ensemble design studies and in the selection step of pruned ensembles, where a team keeps a subset of a large pool with low pairwise Q. They appear in monitoring dashboards that track how correlated a deployed model's errors are with a backup model, so that a failover model is chosen for complementary errors rather than for accuracy alone.

### Using it to make decisions

Use Q to choose which models to combine when you have several accurate candidates. Check the counts before you trust Q: when one classifier is almost always right, the denominator is small and Q swings with a handful of examples. In those cases report the four counts next to Q so a reviewer can see the base rates. Do not use Q alone to claim the ensemble will beat its best member. It is a diagnostic, and the vote still needs to be evaluated on held-out data.

### Pros and cons

**Pros:** it is easy to compute from correctness, it reads as a correlation, and it separates "same mistakes" from "different mistakes" in one number.

**Cons:** it is undefined for some count patterns, it is unstable when one classifier is nearly perfect, and it does not measure how much the vote improves. Two pairs with the same Q can still behave differently under a weighted vote.

## Explanation

The solution computes the four joint counts with boolean masks and forms the ratio. The denominator check happens before the division, so an undefined case raises a clear error rather than producing a silent `nan`.
