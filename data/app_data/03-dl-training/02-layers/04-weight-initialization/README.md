---
name: dl-training-weight-initialization
title: 'Weight initialization: Xavier/Glorot, He/Kaiming'
tags: [neural-networks, layers, initialization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Vanishing and exploding gradients: why a deep, badly-initialized net fails to train`, later in this track, names the failure mode directly: stack enough layers together, and if each layer's output is even slightly too large or too small relative to its input, that small multiplicative factor compounds across every layer, and by the time the signal reaches the last layer (on the forward pass) or the first layer (on the backward pass), it has either exploded to a huge number or vanished to essentially zero. Where you START the weights, before training even begins, is the single biggest lever for avoiding this: initialize every layer so that the VARIANCE of its output roughly matches the variance of its input, and that compounding effect never gets a foothold in the first place.

The exact right initialization scale depends on how many inputs a neuron has (`fan_in`, since summing more terms naturally increases variance) and, for some schemes, how many outputs (`fan_out`) and what nonlinearity comes right after the layer. Xavier/Glorot initialization (Glorot & Bengio, 2010) derived the right scale assuming a roughly linear activation (or tanh, which is close to linear near zero) and BOTH the forward AND backward pass need to preserve variance, hence it depends on both `fan_in` and `fan_out`. He/Kaiming initialization (He et al., 2015) derived a DIFFERENT scale specifically for ReLU, because ReLU zeroes out roughly half of its input (everything negative), which itself halves the output variance relative to a linear activation, so Kaiming compensates with extra variance to make up for that loss.

### From theory to code

Implement four small functions that each compute a single scalar: `xavier_uniform_bound`, `xavier_normal_std`, `kaiming_uniform_bound`, and `kaiming_normal_std`. Each one returns either a uniform-distribution bound `a` (weights sampled from `[-a, a]`) or a normal-distribution standard deviation, given the layer's fan-in (and, for Xavier, fan-out).

### Constraints

- `xavier_uniform_bound(fan_in, fan_out)` and `xavier_normal_std(fan_in, fan_out)` must use BOTH `fan_in` and `fan_out`.
- `kaiming_uniform_bound(fan_in, gain)` and `kaiming_normal_std(fan_in, gain)` must use ONLY `fan_in`, not `fan_out`, and must accept a `gain` parameter (default `sqrt(2)`, the standard ReLU gain).
- All four must return a strictly positive float for any positive `fan_in`/`fan_out`.
- A uniform distribution on `[-a, a]` has variance `a^2 / 3`; use this relationship to derive each uniform bound from its corresponding variance target.

### Hints

<details>
<summary>Hint 1: Xavier's variance target</summary>

Xavier's derivation targets `Var(W) = 2 / (fan_in + fan_out)` (averaging the forward-pass requirement, `1/fan_in`, and the backward-pass requirement, `1/fan_out`). For the normal variant, `std = sqrt(Var(W))` directly.

</details>

<details>
<summary>Hint 2: Converting a variance target into a uniform bound</summary>

If `Var(W) = a^2 / 3` for a uniform distribution on `[-a, a]`, then `a = sqrt(3 * Var(W))`. Applied to Xavier's `Var(W) = 2 / (fan_in + fan_out)`, this gives `a = sqrt(6 / (fan_in + fan_out))`.

</details>

<details>
<summary>Hint 3: Kaiming's variance target</summary>

Kaiming's derivation targets `Var(W) = gain^2 / fan_in` (only `fan_in`, and scaled up by `gain^2` to compensate for whatever nonlinearity follows, `gain = sqrt(2)` for ReLU). Apply the same `a = sqrt(3 * Var(W))` conversion for the uniform variant, and `std = sqrt(Var(W))` for the normal variant.

</details>

## Theory

### The simple version

Think of passing a whispered message down a long line of people. If each person, on average, repeats the message a little LOUDER than they heard it, by the end of a long line the message has become a shout. If each repeats it a little QUIETER, by the end it's inaudible. The only way the message survives a long chain intact is if each person repeats it at very close to the same volume they heard it. A layer's weights are exactly this "repeat at the same volume" factor for the ACTIVATIONS flowing through the network; a good initialization scheme picks the weight scale so that volume stays constant, layer after layer, right from the very first forward pass, before any training has adjusted anything.

### The formula

Xavier/Glorot (targets `Var(W) = 2 / (fan_in + fan_out)`):

```
xavier_uniform_bound(fan_in, fan_out) = sqrt(6 / (fan_in + fan_out))
xavier_normal_std(fan_in, fan_out)    = sqrt(2 / (fan_in + fan_out))
```

He/Kaiming (targets `Var(W) = gain^2 / fan_in`, `gain = sqrt(2)` for ReLU):

```
kaiming_uniform_bound(fan_in, gain) = gain * sqrt(3 / fan_in)
kaiming_normal_std(fan_in, gain)    = gain / sqrt(fan_in)
```

The `sqrt(3 * variance)` step that turns a variance target into a uniform bound comes directly from the variance formula of a uniform distribution: `Var(Uniform(-a, a)) = a^2 / 3`, so `a = sqrt(3 * Var)`.

### How PyTorch actually implements this

`torch.nn.init.xavier_uniform_`, `xavier_normal__`, `kaiming_uniform_`, and `kaiming_normal_` implement exactly these four formulas (this question's four functions compute precisely the scalar each of those in-place functions uses before sampling). `torch.nn.Linear`'s DEFAULT initialization (applied automatically when you construct a layer, with no explicit call needed) is actually `kaiming_uniform_` with `a = sqrt(5)` for the weight, which works out to a scale close to, but not identical to, the ReLU-`gain=sqrt(2)` Kaiming default computed here; PyTorch's own maintainers have noted in the source comments that this particular default is a historical accident rather than a deliberately chosen best practice, and many practitioners explicitly re-initialize with `nn.init.kaiming_normal_(layer.weight, nonlinearity='relu')` for exactly the ReLU-tuned scale this question derives. `fan_in` and `fan_out` for a `[01-linear-forward]`-style weight of shape `(out_features, in_features)` are computed by `torch.nn.init._calculate_fan_in_and_fan_out` as `in_features` and `out_features` respectively, the same convention used throughout this question.

## Explanation

`xavier_uniform_bound` and `xavier_normal_std` both implement Xavier's `Var(W) = 2/(fan_in+fan_out)` target: the normal variant returns `sqrt` of that variance directly, and the uniform variant additionally multiplies inside the square root by `3` (from `Var(Uniform(-a,a)) = a^2/3`, so `a = sqrt(3 * Var)`), giving `sqrt(6/(fan_in+fan_out))`.

`kaiming_uniform_bound` and `kaiming_normal_std` implement Kaiming's `Var(W) = gain^2/fan_in` target the same way: the normal variant is `gain/sqrt(fan_in)` directly, and the uniform variant applies the same `sqrt(3 * Var)` conversion, giving `gain * sqrt(3/fan_in)`.
