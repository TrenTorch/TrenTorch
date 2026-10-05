---
name: ensembles-hard-and-soft-voting
title: Hard vs. soft voting
tags: [classical-ml, ensembles, combination-strategies]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Once several classifiers are trained, you still have to turn their separate answers into one. Hard voting counts class votes. Soft voting averages predicted probabilities, so a confident model can outweigh two lukewarm ones.

### From theory to code

Implement `hard_vote(predictions)` and `soft_vote(probabilities, weights=None)`. Both return one predicted class per sample.

### Constraints

- `predictions` has shape `(n_models, n_samples)` and holds integer class labels.
- `probabilities` has shape `(n_models, n_samples, n_classes)`; `weights` is an optional length-`n_models` array.
- On a hard-vote tie, return the smallest label. On a soft-vote tie, return the smallest class index.
- Return integer NumPy arrays of length `n_samples`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

For hard voting, `np.unique(column, return_counts=True)` lists labels in sorted order, so `np.argmax` over the counts already breaks ties toward the smallest label.

</details>

<details><summary>Hint 2</summary>

For soft voting, average over the model axis first (weighted if weights are given, divided by their sum), then take `argmax` over the class axis.

</details>

## Theory

### The simple version

Hard voting is a show of hands: each model gets one vote. Soft voting is an average of confidence: each model hands over its full probability estimate. They often agree, but can disagree when one model is very sure and the rest are barely leaning one way.

### The formula

$$H(x) = \arg\max_{c} \sum_{i=1}^{T} \mathbb{1}\big[h_i(x) = c\big]$$

$$H(x) = \arg\max_{c} \sum_{i=1}^{T} w_i \, h_i^{c}(x), \qquad w_i \ge 0,\ \sum_i w_i = 1$$

where $h_i^{c}(x)$ is model $i$'s probability for class $c$.

### How libraries implement this

scikit-learn's `VotingClassifier` offers `voting='hard'` and `voting='soft'` with optional `weights`. Soft voting needs models that expose calibrated-enough probabilities.

## Explanation

Column-wise `np.unique` is simple and tie-breaks for free. For soft voting, `np.tensordot(weights, probabilities, axes=(0, 0))` contracts the model axis in one step, producing `(n_samples, n_classes)` ready for `argmax`.
