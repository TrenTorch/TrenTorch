---
name: dl-training-representation-learning
title: 'Representation learning: why depth learns hierarchical features, not one big lookup'
tags: [neural-networks, theory]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-universal-approximation]` showed that a single wide hidden layer CAN, in principle, approximate any function. But "can, in principle" and "is a good idea in practice" are very different claims, and this question is about the gap between them. Imagine trying to classify images by a simple lookup table: store the correct label for every possible image you might ever see. This fails catastrophically for a completely obvious reason: the number of possible images (even small ones) is astronomically, exponentially large, so a lookup table would need to be unimaginably huge, and would have learned NOTHING about any image it hadn't seen during "training" (it's not really learning at all, just memorizing).

Real neural networks avoid this trap through SHARING: a feature detected at one layer (a low-level pattern, like "this looks like an edge going diagonally") can be REUSED by every combination of higher-level features that happens to depend on it, instead of that edge-detection logic being re-derived, or separately memorized, for every possible image that happens to contain a diagonal edge somewhere. This is the core intuition behind why depth (stacking layers, each building on features the previous layer already extracted) tends to work far better in practice than one enormous, un-shared lookup table: a shared feature layer's PARAMETER COUNT grows only proportionally to the number of underlying features, while the number of possible COMBINATIONS of those features (what a lookup table would need to separately store) grows exponentially.

### From theory to code

Implement `lookup_table_size(num_features)` (the number of entries a pure lookup table needs, one per possible combination of `num_features` binary features: `2^num_features`), `shared_feature_layer_size(num_features, num_hidden)` (the number of parameters a single shared `(num_features -> num_hidden)` linear layer needs, reusable across every combination), and `capacity_ratio(num_features, num_hidden)` (how many times larger the lookup table is than the shared layer).

### Constraints

- `lookup_table_size` must compute `2 ** num_features` exactly (one entry per distinct binary combination of `num_features` features).
- `shared_feature_layer_size` must compute the SAME parameter count `[02-layers/01-linear-forward]`'s `linear_forward` would need for a `(num_features -> num_hidden)` layer: `weight` has `num_features * num_hidden` entries, `bias` has `num_hidden` entries.
- `capacity_ratio` must be `lookup_table_size(num_features) / shared_feature_layer_size(num_features, num_hidden)`, reusing both functions above.

### Hints

<details>
<summary>Hint 1</summary>

`lookup_table_size(num_features) = 2 ** num_features`: with `num_features` independent binary switches, there are exactly `2^num_features` distinct ways they can be set, and a lookup table needs one stored entry per distinct setting.

</details>

<details>
<summary>Hint 2</summary>

`shared_feature_layer_size(num_features, num_hidden) = num_features * num_hidden + num_hidden`: `num_features * num_hidden` for the weight matrix (`out_features x in_features`, matching `[02-layers/01-linear-forward]`'s convention), plus `num_hidden` for the bias vector.

</details>

<details>
<summary>Hint 3</summary>

`capacity_ratio` is a one-line division of the two functions above: `lookup_table_size(num_features) / shared_feature_layer_size(num_features, num_hidden)`.

</details>

## Theory

### The simple version

A phrasebook that memorizes a fixed translation for every possible FULL SENTENCE you might ever want to say, versus a phrasebook that just teaches you the words and grammar rules, letting you COMPOSE any sentence you need. The number of possible sentences is essentially unbounded (exponential in sentence length), while the number of words and grammar rules is small and fixed. Once you actually know the words and rules (a shared, compositional "representation"), you can construct sentences you've NEVER seen before, something a fixed table of memorized sentences could never do, no matter how large it grew.

### The formula

```
lookup_table_size(num_features) = 2^num_features
shared_feature_layer_size(num_features, num_hidden) = num_features * num_hidden + num_hidden
capacity_ratio = lookup_table_size / shared_feature_layer_size
```

The key qualitative fact: `lookup_table_size` grows EXPONENTIALLY in `num_features`, while `shared_feature_layer_size` grows only LINEARLY in `num_features` (for fixed `num_hidden`). This means `capacity_ratio` grows without bound as `num_features` increases, the gap between "memorize every combination" and "share a compositional representation" widens explosively as the problem gets richer.

### How PyTorch actually implements this

There's no single PyTorch API for "representation learning" itself, it's an architectural PRINCIPLE, not a specific function, but it's directly visible in how real convolutional networks are structured: a convolutional kernel (learned once, in `torch.nn.Conv2d`) is applied at EVERY spatial position in an image, sharing the exact same small set of weights (the "edge detector," "texture detector," etc.) across the whole image rather than learning a separate detector for every possible position, this is precisely the "shared feature layer, reused across many combinations" pattern this question makes numerically concrete, applied to spatial position instead of feature combinations. Depth compounds this effect further: a network's SECOND layer builds compositional features out of the FIRST layer's shared vocabulary (an "eye" detector built by combining edge and curve detectors from layer 1), and a THIRD layer builds on the second's vocabulary in turn (a "face" detector built from eyes, nose, mouth detectors), so the total representational richness grows combinatorially with depth even though the actual parameter count at each layer grows only linearly, exactly the "lookup table vs. shared, composable representation" gap this question demonstrates numerically, now stacked across multiple layers rather than just one.

## Explanation

`lookup_table_size` returns `2 ** num_features` directly, the count of distinct binary combinations `num_features` independent switches can take.

`shared_feature_layer_size` returns `num_features * num_hidden + num_hidden`, the parameter count of a single shared linear layer (`num_features * num_hidden` weight entries, `num_hidden` bias entries), matching `[02-layers/01-linear-forward]`'s exact parameter-shape convention.

`capacity_ratio` divides the two: `lookup_table_size(num_features) / shared_feature_layer_size(num_features, num_hidden)`, a number that grows explosively as `num_features` increases (since the numerator is exponential and the denominator is only linear in `num_features`), making the "shared representation beats memorization" gap concrete and numerically measurable.
