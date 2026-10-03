---
name: ensemble-pairwise-disagreement
title: 'Disagreement measure between two classifiers'
tags: [classical-ml, ensembles, diversity, disagreement]
difficulty: Intermediate
---

## Statement

### How often do two classifiers get different examples right?

An ensemble only helps when its members make different mistakes. The disagreement measure compares two classifiers on the same examples, using only whether each one was correct.

Let `N_ab` count the examples where classifier 1 has correctness `a` and classifier 2 has correctness `b` (1 means correct, 0 means wrong). The disagreement measure is `(N_01 + N_10) / N`, where `N` is the number of examples.

Implement `disagreement(correct_a, correct_b)`, where both inputs are 1-D boolean or 0/1 arrays of the same length. Return the disagreement as a float between 0 and 1.

### Constraints

- Both inputs must be 1-D and the same length. Otherwise raise `ValueError`.
- Empty inputs raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Convert both inputs to booleans first. Then count the positions where they differ, which is the same as `N_01 + N_10`.

</details>

## Theory

Pairwise diversity measures look at how two members of an ensemble agree. Disagreement is simple to compute and does not need the true labels beyond the correctness indicator. Majority voting benefits when members are both accurate and different, so a pair with high disagreement but also high accuracy is the most useful pair to combine. Kuncheva and Whitaker showed that these measures track ensemble gain, but also that the best measure depends on the vote rule.

### Where this shows up in production

Ensemble teams use pairwise disagreement to decide which models to keep when they have a pool of candidates. Ranking pool members by disagreement against the current champion is a cheap way to find a model that fixes different errors. It is also used in model monitoring, where a rising disagreement between a new model and the old one flags a region of input space that needs review before rollout.

### Using it to make decisions

Use it to pick diverse ensemble members, and pair it with each model's accuracy. Two models with zero disagreement add nothing to a vote. Two models with high disagreement but low accuracy can still hurt, so require both. In a rollout, a spike in disagreement with the production model is a signal to look at a sample, not proof that the new model is worse.

### Pros and cons

**Pros:** it is cheap, it uses only correctness, and it is easy to explain to stakeholders as "how often do these two disagree on what is right".

**Cons:** the measure ignores which mistakes are made, so two models that are wrong on different examples in ways that do not help the vote can still look diverse. It does not tell you whether the vote will improve. It depends on the evaluation set, and small sets give noisy values.

## Explanation

The solution converts both correctness vectors to booleans, counts the positions where they differ, and divides by the sample count. The result is symmetric in the two classifiers and is zero exactly when they have the same correctness pattern.
