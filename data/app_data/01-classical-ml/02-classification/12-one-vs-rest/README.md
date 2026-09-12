---
name: classification-one-vs-rest
title: 'Multiclass via One-vs-Rest, contrasted against Softmax'
tags: [classical-ml, classification]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Stretch: Softmax + Categorical Cross-Entropy` handles multiclass classification with one unified model: a single weight matrix, one softmax, trained jointly on all classes at once. But `Full Training Loop`'s binary logistic regression came first, and it turns out you don't strictly NEED softmax to handle more than two classes at all, a much simpler idea works too: train a SEPARATE binary "is it this class, or not" classifier for every class, independently, and at prediction time just ask all of them and go with whichever is most confident.

This is One-vs-Rest (also called One-vs-All), and building it here, entirely out of `Full Training Loop`'s own binary machinery, makes the contrast with Softmax's single joint model concrete rather than abstract: two genuinely different ways of solving the same multiclass problem, with real, different tradeoffs.

### From theory to code

Theory trains `num_classes` independent binary classifiers by reusing `Full Training Loop`'s `train_logistic_regression` once per class (each time treating one class as positive, everything else as negative), then predicts by comparing all classifiers' confidence scores and picking the winner.

Implement `train_one_vs_rest(input, target, num_classes, lr, epochs)` first, then `predict_one_vs_rest(input, weights, biases)` on top of it.

### Constraints

- Each binary classifier is trained completely independently (no shared parameters, no joint loss).
- `weights` is `(num_classes, in_features)`, `biases` is `(num_classes,)`, stacked in the shape `linear`'s general multi-output convention already expects.
- Prediction picks the class with the single highest score, no thresholding at `0.5`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

For each class `k`, build a binary target array: `1` where `target == k`, `0` everywhere else, then call `train_logistic_regression` on that binary target exactly like `Full Training Loop` already does.

</details>

<details>
<summary>Hint 2</summary>

`linear(input, weights, biases)` with `weights` shaped `(num_classes, in_features)` computes every class's raw score for every input row in one matmul, exactly the general multi-output convention `Hypothesis Function` was built for.

</details>

## Theory

### The simple version

Imagine sorting mail into "bills," "personal letters," and "junk" using three separate, independently-trained sorters instead of one unified sorting machine: a "bill-or-not" sorter, a "personal-or-not" sorter, a "junk-or-not" sorter. Each one only ever answers its own yes/no question, entirely unaware the other sorters exist. To classify a new piece of mail, run it through all three and trust whichever sorter is most confident. That's One-vs-Rest: `num_classes` completely independent binary decisions, standing in for one genuinely multiclass decision.

### The formula

```text
for each class k in 0..num_classes-1:
    binary_target = 1 where target == k, else 0
    train a SEPARATE logistic regression classifier on binary_target

predict(x) = argmax_k( sigmoid(classifier_k(x)) )
```

The contrast with Softmax + Categorical Cross-Entropy is the real point of this question. Softmax trains ONE joint model where every class's score is computed from the SAME shared weights, and the classes' probabilities are coupled, they're forced to sum to exactly `1` (`04-softmax`, Deep Learning Core, made this "rows sum to zero" structural property explicit for its backward pass). One-vs-Rest's classifiers are trained in complete isolation, each optimizing its own independent binary loss, with no such constraint, each class's sigmoid score is its own number in `[0, 1]`, and there's no guarantee they sum to anything in particular across classes. This can occasionally leave "confidence gaps" (every classifier unconfident) or "confidence conflicts" (multiple classifiers confident) that a jointly-trained softmax model, by construction, cannot produce.

One-vs-Rest's real practical advantage: it's trivially parallelizable (every classifier trains completely independently, no coordination needed) and lets you reuse ANY binary classifier as a building block, not just logistic regression, `07-lda`'s Linear Discriminant Analysis, `01-classical-ml/05-instance-based-probabilistic`'s Naive Bayes and k-NN, or even a Support Vector Machine, none of which have a native multiclass formulation the way softmax does, can all be turned multiclass via exactly this same One-vs-Rest wrapper.

### How PyTorch actually implements this

`sklearn.multiclass.OneVsRestClassifier` is a real, general-purpose wrapper implementing exactly this pattern around ANY binary classifier, used specifically for algorithms (SVMs being the classic example) that don't have a natural multiclass extension the way softmax-based neural networks do. Deep learning code almost always reaches for softmax + cross-entropy instead (`02-cross-entropy`, Deep Learning Core), precisely because joint training is both more parameter-efficient (one shared representation instead of `num_classes` entirely separate models) and produces genuinely calibrated, properly-normalized class probabilities, exactly the property One-vs-Rest's independent classifiers don't guarantee.

## Explanation

`train_one_vs_rest` loops over every class index, builds that class's binary target (`1` where `target == class_index`, else `0`), trains an independent binary classifier via the imported `train_logistic_regression`, and stacks each classifier's weight/bias into row `class_index` of the returned `weights`/`biases` arrays.

`predict_one_vs_rest` runs every class's classifier on `input` in one call via `sigmoid(linear(input, weights, biases))` (using `linear`'s general multi-output convention: `weights` shaped `(num_classes, in_features)` produces one column of scores per class), then returns `np.argmax` along the class axis, the single most confident class per row.
