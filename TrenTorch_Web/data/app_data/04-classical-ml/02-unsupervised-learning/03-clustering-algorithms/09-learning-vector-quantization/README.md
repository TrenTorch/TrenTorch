---
name: lvq1-prototype-update
title: 'LVQ1 prototype update'
tags: [classical-ml, prototypes, learning-vector-quantization, online-learning]
difficulty: Intermediate
---

## Statement

### Pull the nearest prototype toward a matching example

Learning Vector Quantization (LVQ1) keeps a small set of labeled prototypes. For each training example, the nearest prototype wins. If the winner has the same label as the example, it moves toward the example. If the labels differ, it moves away.

Implement `lvq1_step(prototypes, proto_labels, x, y, lr)`.

- `prototypes` is a `K` by `d` array, `proto_labels` has length `K`, `x` has length `d`, `y` is the example's label, and `lr >= 0` is the learning rate.
- The winner is the prototype with the smallest squared Euclidean distance to `x`. On a tie, pick the lowest index.
- If `proto_labels[winner] == y`, set `p = p + lr * (x - p)`. Otherwise set `p = p - lr * (x - p)`.
- Return `(new_prototypes, winner_index)`. Do not modify the input array.

### Constraints

- `prototypes` must be a non-empty 2-D array. Otherwise raise `ValueError`.
- `proto_labels` must have length `K`, and `x` must have length `d`. Otherwise raise `ValueError`.
- `lr < 0` raises `ValueError`.

### Hints

<details>
<summary>Hint 1</summary>

Compute the distances to all prototypes with broadcasting, then use `argmin`, which already returns the lowest index on a tie.

</details>

## Theory

LVQ1 is an online rule that places prototypes where the decision boundary between classes needs them. Moving the correct prototype toward an example pulls the region of its class over that example. Moving a wrong prototype away pushes its region out of the way. Because each step touches one prototype, the rule is cheap, but the outcome depends strongly on initialization and on the learning rate schedule.

### Where this shows up in production

Prototype classifiers are used where a model must be small and readable. Examples include on-device classifiers that store a few dozen prototypes per class, quality inspection lines that want to show an operator the representative good and bad parts, and speech and handwriting systems in older deployments. Because a prototype is a real example in feature space, a reviewer can look at it directly.

### Using it to make decisions

Use LVQ when the number of classes is small, the classes form compact clusters, and the team needs a model that can be stored, inspected and updated one example at a time. Start with prototypes from k-means per class, not random points, and decay the learning rate over time. If accuracy stalls, a margin-based variant (LVQ2.1 or LVQ3) or a small neural network is the next step, and the prototypes can still serve as a baseline.

### Pros and cons

**Pros:** inference is a nearest-prototype lookup, prototypes are interpretable, the update is a single vector step, and the model can learn online.

**Cons:** results depend on initialization and learning rate, and the update uses only the winning prototype, so the boundary can drift. Plain LVQ1 has no margin objective, so accuracy usually trails margin-based classifiers on hard data.

## Explanation

The solution finds the winner with a vectorized distance computation and applies one signed step to that prototype only. It copies the prototype array first, so the caller's data is never changed.
