---
name: vision-history-efficientnet-compound-scaling
title: "Note: EfficientNet — Compound Scaling"
tags: [computer-vision, cnn, history, efficiency]
difficulty: Beginner
---

## Statement

### The problem, from first principles

If a CNN isn't accurate enough, the classic fix is to make it bigger — but "bigger" has three independent knobs: more layers (depth), more channels per layer (width), and larger input images (resolution). Scaling only one of these hits diminishing returns quickly: an extremely deep but narrow, low-resolution network wastes its depth on features too coarse to matter, and an extremely wide but shallow network can't build up the hierarchical features depth provides. EfficientNet's insight was that these three axes interact, so they should be scaled together, in a fixed, empirically-tuned ratio, controlled by a single number.

### From theory to code

Theory says: pick base per-step multipliers for depth, width, and resolution (`alpha`, `beta`, `gamma`), and scale all three simultaneously by raising each to the power of a single "compound coefficient" `phi` that the user chooses based on how much extra compute budget is available.

Implement `compound_scale(phi, alpha=1.2, beta=1.1, gamma=1.15)` against that reasoning.

### Constraints

- `phi`: a non-negative integer (`phi=0` means "the unscaled base model").
- `alpha`, `beta`, `gamma`: positive floats, each the base multiplier applied once per unit increase in `phi`.
- Returns a 3-tuple of floats: `(depth_mult, width_mult, resolution_mult)`.
- `phi=0` always returns `(1.0, 1.0, 1.0)` regardless of `alpha`/`beta`/`gamma`, since raising anything to the power 0 is 1.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Each multiplier is completely independent of the other two — there's no interaction between depth, width and resolution in the formula itself, only in how their base rates (`alpha`, `beta`, `gamma`) were chosen.

</details>

<details>
<summary>Hint 2</summary>

`alpha ** phi`, `beta ** phi`, `gamma ** phi` — that's the entire function.

</details>

## Theory

### The simple version

Imagine baking a cake and deciding it needs to serve more people. You could just make it deeper (more layers of cake), or just wider (bigger pan), or just increase the recipe's resolution (finer, more detailed frosting work) — but a chef scaling a recipe up for a bigger party adjusts every ingredient proportionally at once, not just one. EfficientNet applies the same idea to a CNN: `phi` is "how much bigger a party," and `alpha`, `beta`, `gamma` are the fixed proportions in which depth, width, and resolution should each grow to stay balanced as the network scales up.

### The formula

```text
depth_mult      = alpha ^ phi
width_mult      = beta  ^ phi
resolution_mult = gamma ^ phi
```

`alpha`, `beta`, `gamma` are chosen once (via a small grid search on a baseline model) subject to `alpha * beta^2 * gamma^2 ~= 2`, which keeps each unit increase of `phi` roughly doubling the model's total compute (FLOPs) — because compute scales linearly with depth but roughly quadratically with width and with resolution.

### How PyTorch actually implements this

`torchvision.models.efficientnet_b0` through `efficientnet_b7` are exactly one base architecture ("B0") scaled up by exactly this compound formula at seven different values of `phi` — the differences between B0 and B7 aren't different architectures, just different depth/width/resolution multipliers applied to the same building blocks (which are themselves built from depthwise-separable convolutions and squeeze-and-excitation blocks, an extension of the ideas in this curriculum's `04-modern-cnn-concepts` track). EfficientNet's original paper found this family to reach the same accuracy as much larger hand-scaled networks (like a naively-widened ResNet) using roughly an order of magnitude fewer parameters and FLOPs.

## Explanation

`alpha ** phi`, `beta ** phi`, and `gamma ** phi` are each an independent exponential — `phi` doesn't combine the three axes together in the formula itself, it simply tells each axis how many "steps" of its own fixed growth rate to apply. Because `phi=0` makes every exponent 0, all three multipliers collapse to `1.0` exactly, correctly representing "no scaling, this is the base model." The reason `alpha`, `beta` and `gamma` aren't picked arbitrarily is the compute-balance identity `alpha * beta^2 * gamma^2 ~= 2`: since width and resolution each affect two independent dimensions of the network's computation (a wider layer has both more input and more output channels; a higher-resolution input makes every convolution scan a proportionally larger spatial grid in both directions) while depth affects only one (more sequential layers), a unit increase in `phi` grows compute by roughly the same total factor regardless of which axis contributes the growth — that's what keeps the model "balanced" as it scales.
