---
name: vision-mixup
title: Mixup
tags: [computer-vision, augmentation, regularization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Neural networks tend to memorize training images and become overconfident between them. **Mixup** is an augmentation that teaches them to behave linearly between examples: build a new training example as a weighted average of two images, and give it the same weighted average of their (one-hot) labels. A picture that is 70% cat and 30% dog gets the label "0.7 cat, 0.3 dog". The mixing weight `lam` is drawn from a Beta distribution with parameter `alpha`. Small `alpha` means `lam` is usually near 0 or 1 (a mild mix), and `alpha = 1` makes it uniform on `[0, 1]`.

### From theory to code

Implement `sample_lambda` and `mixup`.

### Constraints

- `sample_lambda(alpha, rng)` returns `rng.beta(alpha, alpha)` with exactly one call to `rng.beta`, where `rng` is a `np.random.RandomState`.
- `mixup(x1, y1, x2, y2, lam)` returns `(lam * x1 + (1 - lam) * x2, lam * y1 + (1 - lam) * y2)`. Images and one-hot label vectors are NumPy arrays of matching shapes.
- `lam` is a float in `[0, 1]`. Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Mixup is a convex combination, so every pixel and label entry stays within the range of its two parents.

</details>

<details>
<summary>Hint 2</summary>

Labels must be one-hot (or soft) vectors, not integer class ids, so they can be averaged.

</details>

## Theory

### The simple version

Mixing two paint colours in a ratio and writing the ratio on the tin. The network learns that the half-way colour deserves a half-way label.

### The formula

$$
\tilde x = \lambda x_i + (1 - \lambda) x_j, \qquad \tilde y = \lambda y_i + (1 - \lambda) y_j, \qquad \lambda \sim \text{Beta}(\alpha, \alpha)
$$

### How this is done in practice

Mixup (Zhang et al., 2018) is available in `timm` and `torchvision.transforms.v2.MixUp`. It improves calibration and robustness to label noise. In practice the second sample is usually a shuffled copy of the same batch, which is why one `lam` is used for the whole batch.

## Explanation

Two lines of arithmetic. The sampling function is separated so that tests can pin the random stream with a seed.
