---
name: metric-contrastive-loss
title: 'Contrastive loss for a pair of embeddings'
tags: [classical-ml, metric-learning, contrastive-loss, siamese-networks]
difficulty: Intermediate
---

## Statement

### Pull similar pairs together and push dissimilar pairs apart

Metric learning trains an embedding so that the distance between two inputs matches whether they are the same. The contrastive loss (Hadsell, Chopra and LeCun, 2006) scores one pair given its distance `d` and a flag `s` (1 for similar, 0 for dissimilar):

`L = s * d^2 + (1 - s) * max(0, m - d)^2`

Similar pairs are penalized by their distance. Dissimilar pairs are penalized only while they sit inside the margin `m`.

Implement `contrastive_loss(distances, is_similar, margin=1.0)`, which applies the formula elementwise.

- `distances` and `is_similar` have the same shape. `is_similar` holds 0 or 1 values.
- Return an array of the same shape.

### Constraints

- Shapes must match. Otherwise raise `ValueError`.
- Any negative distance raises `ValueError`.
- `margin < 0` raises `ValueError`.
- `is_similar` values other than 0 and 1 raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.maximum(0.0, margin - d)` for the hinge. The dissimilar term is zero whenever `d` is at least the margin.

</details>

## Theory

Contrastive loss turns a pair problem into a smooth objective on an embedding network. The margin controls scale: once a dissimilar pair is far enough apart, it stops contributing, so the network spends its capacity on pairs that are still confused. The loss has no preference between a pair that is slightly close and one that is very close, beyond the squared penalty, which is why hard pair mining matters in practice.

### Where this shows up in production

Siamese networks trained with contrastive loss power face verification, duplicate question detection and product matching. The trained distance is then thresholded: pairs under a cut-off are declared the same item. Retrieval systems use the same idea to learn an embedding space where nearest neighbours are relevant items, and the margin is tuned together with the search threshold.

### Using it to make decisions

Use contrastive loss when you have labeled pairs and need a distance that you can threshold, such as a duplicate detector with a human-set precision target. Tune the margin on a validation set of pairs, since it sets how far apart dissimilar items are pushed. Sample hard negatives, meaning dissimilar pairs that are currently close, because random negatives are mostly easy and contribute almost nothing to the loss.

### Pros and cons

**Pros:** simple to implement, works directly with pairs of any origin, and gives a distance that can be thresholded for a precision target.

**Cons:** naive pair sampling grows quadratically with the dataset, easy negatives dominate the average loss, and the margin needs careful tuning. Triplet and softmax-based losses often use class-level structure more effectively.

## Explanation

The solution computes both branches for every element and combines them with the similarity flag. Because the flag is 0 or 1, one expression covers both cases, and the hinge keeps the dissimilar term at zero once the pair clears the margin.
