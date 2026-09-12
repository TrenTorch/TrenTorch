---
name: math-statistical-significance-p-values
title: Statistical significance and p-values, and what they do not mean
tags: [probability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`03-hypothesis-testing-t-test` and `04-ab-testing` both produce a p-value and a conventional cutoff, `p < 0.05`, is called "statistically significant." This question tackles the part of the picture those two questions left implicit and dangerously easy to misuse: what does `alpha = 0.05` actually promise, and what happens the moment you run more than one test?

The genuinely important, often-missed fact: `alpha = 0.05` means "a 5% chance of a FALSE POSITIVE on any single test where the null hypothesis is actually true." Run 100 such tests, and even if NOTHING real is going on anywhere, you'd still expect roughly 5 of them to falsely come back "significant," purely from chance. Testing dozens of features against a target, or running dozens of A/B test variants, and reporting only the "significant" ones without accounting for this, is one of the most common, genuinely misleading statistical mistakes in practice.

### From theory to code

Theory defines the significance threshold directly, and derives two consequences of running multiple tests: how many false positives to expect by chance alone, and a simple correction (Bonferroni) that keeps the overall false-positive rate under control.

Implement `is_statistically_significant(p_value, alpha=0.05)`, `expected_false_positives(num_tests, alpha=0.05)`, and `bonferroni_corrected_alpha(num_tests, alpha=0.05)` against that reasoning.

### Constraints

- `is_statistically_significant` is a strict `<` comparison, not `<=`.
- `expected_false_positives` and `bonferroni_corrected_alpha` are direct, one-line formulas, no simulation needed inside the functions themselves.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`expected_false_positives` is exactly `num_tests * alpha`, the expected count under "every null hypothesis is true."

</details>

<details>
<summary>Hint 2</summary>

`bonferroni_corrected_alpha` divides the original alpha by the number of tests, a stricter per-test bar that keeps the COMBINED false-positive rate near the original alpha.

</details>

## Theory

### The simple version

Buy 100 lottery scratch tickets that each have a genuinely tiny (but nonzero) chance of a "you're a winner!" misprint, purely from a printing defect, with no real prize behind it. Even though EVERY ticket is individually almost certainly a real loser, across 100 tickets you might well find a couple of misprints. Running 100 independent hypothesis tests, when there's truly no real effect anywhere, works the same way: `alpha = 0.05` promises a 5% false-positive rate PER TEST, so across 100 tests, expect roughly 5 misleading "significant!" results, not because anything real happened, but purely because you looked in enough places.

### The formula

```text
is_statistically_significant(p_value, alpha) = p_value < alpha

expected_false_positives(num_tests, alpha) = num_tests * alpha

bonferroni_corrected_alpha(num_tests, alpha) = alpha / num_tests
```

`alpha` (conventionally `0.05`) is the false-positive rate you're willing to accept ON A SINGLE TEST where the null hypothesis is true. It is NOT the probability the null hypothesis is true given a significant result, NOT the probability the observed effect is real, and NOT something that stays at `5%` once you've run many tests and are only looking at the ones that happened to come back significant, a subtle but critical distinction, since p-values are frequently, incorrectly described as "the probability the result is due to chance."

The Bonferroni correction is the simplest fix for the multiple-testing problem: dividing `alpha` by the number of tests makes each INDIVIDUAL test's bar stricter, keeping the OVERALL chance of at least one false positive across all tests combined close to the original `alpha`. It is deliberately conservative (it can make genuinely real effects harder to detect, a real cost), which is why more sophisticated corrections (not covered here) exist for situations with very many tests.

### How PyTorch actually implements this

There is no PyTorch API for this, it is a matter of statistical practice, not computation, and it applies directly to ML experimentation: trying many model variants, hyperparameter settings, or feature combinations and reporting only the "best" or "significant" ones is exactly the multiple-comparisons trap this question names. `12-nested-cross-validation` (Evaluation & Model Selection, Classical ML) exists specifically to prevent a related version of this mistake, hyperparameter search implicitly tries MANY configurations and can "get lucky" on a validation set the same way multiple hypothesis tests get lucky on pure noise, which is exactly why that question's nested structure keeps the final reported performance honest. The discipline that actually prevents both problems: decide your test (or your evaluation protocol) BEFORE looking at results, account explicitly for how many comparisons you're really making, and treat "it worked, once, on this particular split" with real skepticism.

## Explanation

`is_statistically_significant` returns `p_value < alpha`, the conventional threshold comparison.

`expected_false_positives` returns `num_tests * alpha`, the expected count of false "significant" results under the assumption every null hypothesis tested is actually true.

`bonferroni_corrected_alpha` returns `alpha / num_tests`, the stricter per-test threshold that keeps the combined false-positive rate near the original `alpha`.
