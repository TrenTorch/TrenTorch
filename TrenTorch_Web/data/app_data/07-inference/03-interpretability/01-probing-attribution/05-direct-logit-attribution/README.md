---
name: lm-direct-logit-attribution
title: Direct Logit Attribution
tags: [interpretability, attribution, residual-stream]
difficulty: Advanced
---

## Statement

### The problem, from first principles

The final residual stream is a **sum**: the embedding plus the output of every attention head and MLP layer, each added in turn. The final logits are a linear function of that sum, apart from the normalization scale. That means the logit difference between a correct and an incorrect answer token splits exactly into one contribution per component. Direct logit attribution reads those contributions off: positive for components pushing toward the correct answer, negative for those pushing away. It is the cheapest circuit-finding tool because it needs a single forward pass and no interventions, though it only sees _direct_ effects on the output, not effects mediated by later layers.

### From theory to code

Implement `direct_logit_attribution` and `attribution_total`.

### Constraints

- `components` has shape `(C, d)`: the vectors each component wrote into the final-position residual stream. `W_U` has shape `(d, V)`. `correct` and `wrong` are token ids. `scale` is the scalar final-normalization divisor (the final stream is `sum(components) / scale`).
- `direct_logit_attribution(components, W_U, correct, wrong, scale)` returns a length-`C` array: for each component, `(component @ (W_U[:, correct] - W_U[:, wrong])) / scale`.
- `attribution_total(contributions)` is the sum, which equals the logit difference of the full stream.
- Ignore any normalization gain or bias: the unembedding is exactly `W_U`.

### Hints

<details>
<summary>Hint 1</summary>

First build the direction `W_U[:, correct] - W_U[:, wrong]`, then take one matrix-vector product with the components.

</details>

<details>
<summary>Hint 2</summary>

Because the contributions are linear, they must sum to the logit difference of `components.sum(axis=0) / scale`.

</details>

## Theory

### The simple version

A restaurant bill is the sum of its items. Attribution reads the itemized receipt: which dishes drove the total up and which brought it down. It does not say why the kitchen cooked them, only what each one cost.

### The formula

$$
\text{logit}_a - \text{logit}_b = \frac{1}{s}\Big(\sum_{c} x_c\Big)^\top (u_a - u_b) = \sum_c \underbrace{\frac{x_c^\top (u_a - u_b)}{s}}_{\text{DLA}_c}
$$

where $u_a$ is the unembedding column of token $a$ and $s$ is the final normalization scale held fixed. Holding $s$ fixed is what makes the decomposition exact.

### How this is done in practice

TransformerLens' `decompose_resid` and `apply_ln_to_stack` produce the component stack, and attribution plots over heads are how early circuit papers (for example on indirect object identification) located the heads that mattered. Real models add per-head and per-position structure, and the attribution of a component can be zero even when intervening on it changes the output, because of downstream effects.

## Explanation

One matrix-vector product gives every component's contribution at once. The linearity check, `sum(contributions) == logit_diff(total stream)`, is the best test of both correctness and understanding.
