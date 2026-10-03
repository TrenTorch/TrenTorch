---
name: vision-freeze-by-depth
title: Layer Freezing
tags: [computer-vision, transfer-learning, fine-tuning, parameter-efficiency]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The cheapest form of transfer learning is to **freeze** most of a pretrained network and train only the top. Frozen parameters receive no gradient updates, which saves memory (no optimizer state), time (no backward pass through frozen early layers is needed for their weights) and reduces overfitting when the new dataset is small. The choice is a spectrum: freeze everything except a new head (feature extraction), freeze only the first few blocks, or freeze nothing. Deciding which parameters are trainable from their names is a few lines of logic, and the number of trainable parameters is the headline number reported for any fine-tuning recipe.

### From theory to code

Implement `trainable_mask` and `count_trainable`.

### Constraints

- Parameters are named `embed.<...>`, `layers.<i>.<...>` or `head.<...>`. `trainable_mask(names, n_frozen)` returns a list of booleans: `embed` and `layers.i` for `i < n_frozen` are frozen (`False`), everything else (`layers.i` with `i >= n_frozen`, and `head`) is trainable (`True`). Any other name is trainable.
- `count_trainable(sizes, mask)` is the sum of `sizes[k]` over the entries where `mask[k]` is true, as an int, and `fraction_trainable(sizes, mask)` is that count divided by the total number of parameters.

### Hints

<details>
<summary>Hint 1</summary>

Parse `layers.<i>` by splitting on `.` and converting the second component to an integer.

</details>

<details>
<summary>Hint 2</summary>

With `n_frozen = 0` the embedding is still frozen by this rule only if you freeze it explicitly: for this exercise, `embed` is frozen whenever `n_frozen >= 1`.

</details>

## Theory

### The simple version

Learning a new dialect: you keep your grammar and vocabulary (frozen) and practice only the new idioms (trainable). The fewer things you retrain, the less data you need.

### The formula

$$
m_k = \mathbf{1}\big[\,\text{depth}(k) \ge n_{\text{frozen}}\,\big], \qquad \text{trainable fraction} = \frac{\sum_k m_k\, s_k}{\sum_k s_k}
$$

where the embedding counts as depth $0$ and block $i$ as depth $i + 1$, the head as the deepest.

### How this is done in practice

In PyTorch you set `param.requires_grad = False` for the frozen group and pass only the trainable parameters to the optimizer. Parameter-efficient methods such as LoRA keep the base weights frozen and add a small trainable module, so the trainable fraction is often below 1%.

## Explanation

The depth rule is the same indexing used for layer-wise learning rates. A single pass over names gives the mask, and a weighted sum gives the headline statistic.
