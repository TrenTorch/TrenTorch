---
name: lm-temperature-data-mixtures
title: Data Mixture Temperature
tags: [pretraining, data-mixture, sampling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A pretraining corpus mixes sources of very different sizes: huge web crawls, medium code collections and small, high-quality book or math sets. Sampling in proportion to size means the small sets are almost never seen, while sampling uniformly would repeat tiny sets thousands of times. A standard compromise is **temperature sampling**: raise each source's size to the power `1 / T` and renormalize. `T = 1` reproduces the natural proportions, larger `T` flattens toward uniform and `T < 1` sharpens toward the largest source. It is the same temperature idea used for softmax sampling, applied to dataset sizes.

### From theory to code

Implement `mixture_weights` and `epochs_per_source`.

### Constraints

- `mixture_weights(sizes, temperature)` returns weights proportional to `sizes ** (1 / temperature)`, normalized to sum to 1. `sizes` are positive token counts and `temperature > 0`.
- `epochs_per_source(sizes, weights, total_tokens)` returns, per source, how many times its data is repeated: `weights * total_tokens / sizes`.
- Return NumPy float arrays.

### Hints

<details>
<summary>Hint 1</summary>

Compute `s = sizes ** (1 / T)` and divide by `s.sum()`.

</details>

<details>
<summary>Hint 2</summary>

A source with epochs well above 1 is being repeated; the last test shows how raising the temperature increases this for small sources.

</details>

## Theory

### The simple version

A recipe with ingredients in very different quantities: using them in raw proportion lets flour drown the saffron, using equal amounts wastes the flour. Temperature is the dial between the two.

### The formula

$$
w_i = \frac{n_i^{1/T}}{\sum_j n_j^{1/T}}, \qquad \text{epochs}_i = \frac{w_i\, D}{n_i}
$$

with $n_i$ the size of source $i$ and $D$ the total training tokens.

### How this is done in practice

Multilingual models (mT5, XLM-R) use temperature or exponent sampling so that low-resource languages are not drowned. Modern data recipes also cap repetition (few epochs per source) and tune mixtures with small proxy runs, which is why the epochs function is part of the exercise.

## Explanation

Two lines per function. The interesting content is behavioural: how weights and repetition move together as the temperature changes.
