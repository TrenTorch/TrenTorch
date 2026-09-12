---
name: vision-vit-triplet-loss
title: "Stretch: Triplet Loss (Metric/Representation Learning)"
tags: [computer-vision, transformers, contrastive-learning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`06-info-nce-loss` compares one anchor against many candidates at once (an entire batch). Triplet loss asks the simplest possible version of the same underlying question, using just three examples at a time: given an anchor, a "positive" example that should be similar to it, and a "negative" example that should be dissimilar, push the anchor closer to its positive than to its negative, by at least some margin. It doesn't care about absolute distances at all — only the *relative* ordering, which is exactly what makes it useful for learning an embedding space with no fixed set of classes (face recognition being the classic example: there's no finite list of "face classes," only "same person" vs. "different person" comparisons).

### From theory to code

Theory says: for each anchor/positive/negative triplet, compute the anchor's distance to its positive and its distance to its negative. If the negative is already farther away than the positive by at least `margin`, that triplet contributes nothing (loss 0) — the model already has it right, with room to spare. Otherwise, the loss is exactly how far short of that margin the triplet currently falls.

Implement `triplet_loss(anchor, positive, negative, margin=1.0)` against that reasoning.

### Constraints

- `anchor`, `positive`, `negative`: all shape `(N, D)` — row `i` across the three arrays forms one triplet.
- `margin`: a positive float, the minimum required gap between the two distances.
- Returns a single Python `float`: the mean per-triplet loss across all `N` triplets.
- None of the three inputs are modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.linalg.norm(anchor - positive, axis=1)` computes the Euclidean distance for every row at once — `axis=1` reduces across the feature dimension, leaving one distance per triplet.

</details>

<details>
<summary>Hint 2</summary>

`np.maximum(0.0, dist_to_positive - dist_to_negative + margin)` is the per-triplet hinge loss — then `.mean()` averages across triplets, and `float(...)` converts the resulting NumPy scalar to a plain Python float.

</details>

## Theory

### The simple version

Imagine training a photo-sorting assistant using flashcards: each flashcard shows three photos — "this person" (anchor), "the same person, different photo" (positive), and "a different person" (negative) — and the assistant's only job is to make sure the same-person photo always FEELS closer than the different-person photo, by a comfortable margin. It's never told "person A is class 7"; it only ever learns from these relative comparisons, which is exactly why triplet loss works even when there's no fixed, finite set of classes to predict — new people can be added forever without retraining the whole classification scheme.

### The formula

```text
dist_to_positive = ||anchor - positive||_2      # per row
dist_to_negative = ||anchor - negative||_2      # per row
loss_per_triplet  = max(0, dist_to_positive - dist_to_negative + margin)
loss              = mean(loss_per_triplet)
```

### How PyTorch actually implements this

`torch.nn.TripletMarginLoss(margin=1.0, p=2)` (and its functional form `torch.nn.functional.triplet_margin_loss`) implements exactly this formula, with `p` controlling which distance norm is used (`p=2` is Euclidean distance, matching this exercise). The hardest part of training with triplet loss in practice isn't the loss formula itself — it's "triplet mining," choosing which positive/negative pairs to actually train on, since most randomly-sampled triplets quickly become "easy" (already satisfy the margin, contributing zero gradient) and provide no useful training signal; real systems specifically seek out "hard" or "semi-hard" triplets where the negative is deceptively close to the anchor, to keep training effective.

## Explanation

`np.linalg.norm(anchor - positive, axis=1)` computes `sqrt(sum((anchor_i - positive_i)^2))` independently for every row `i`, giving the ordinary Euclidean distance between each anchor and its matching positive — the same computation, with `negative` substituted in, gives the anchor-to-negative distance. The hinge `max(0, dist_to_positive - dist_to_negative + margin)` is exactly zero whenever `dist_to_negative >= dist_to_positive + margin` (the negative is already comfortably farther away than required), and grows linearly larger the more that condition is violated — this is what makes triplet loss stop pushing on triplets the model already handles well, focusing its gradient entirely on triplets that are still too close together or, worse, inverted (negative closer than positive). Averaging over all `N` triplets with `.mean()` combines these into one scalar training signal, exactly matching how any per-sample loss in this curriculum (cross-entropy included) is reduced to a single number for backpropagation.
