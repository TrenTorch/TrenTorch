---
name: vision-grayscale-channel-normalization
title: Grayscale & Channel Normalization
tags: [computer-vision, preprocessing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Two preprocessing steps appear in almost every vision pipeline. Converting color to **grayscale** collapses three channels into one brightness value, and it is not a plain average: the eye is most sensitive to green and least to blue, so the standard luma formula weights the channels `0.299`, `0.587` and `0.114`. **Channel normalization** then shifts and scales each channel to have roughly zero mean and unit variance across the dataset, which keeps the inputs of the first layer in a range where optimization is well behaved. The per-channel mean and standard deviation come from the training set, not from each image.

### From theory to code

Implement `to_grayscale` and `normalize_channels`.

### Constraints

- `to_grayscale(img)`: `img` has shape `(H, W, 3)`; return shape `(H, W)` equal to `img @ [0.299, 0.587, 0.114]`.
- `normalize_channels(img, mean, std)`: `img` has shape `(H, W, C)` and `mean`, `std` have shape `(C,)` with positive `std`; return `(img - mean) / std`.
- Neither function modifies its input.

### Hints

<details>
<summary>Hint 1</summary>

A dot product over the last axis does the weighted sum for every pixel at once.

</details>

<details>
<summary>Hint 2</summary>

`mean` and `std` broadcast over the leading axes automatically.

</details>

## Theory

### The simple version

A grayscale photo is what you see if you ignore colour but keep how bright each spot is. Normalization is converting each channel's units so that none of them shouts louder than the others.

### The formula

$$
Y = 0.299\,R + 0.587\,G + 0.114\,B, \qquad \hat x_{c} = \frac{x_c - \mu_c}{\sigma_c}
$$

The weights sum to 1, so a uniformly gray pixel keeps its value under the conversion.

### How this is done in practice

`torchvision.transforms.Grayscale` and `Normalize` implement exactly these two steps, and ImageNet pipelines use the dataset means `[0.485, 0.456, 0.406]` and standard deviations `[0.229, 0.224, 0.225]`. Forgetting to normalize at inference time with the same constants used in training is a classic silent bug.

## Explanation

Both operations are vectorized over pixels with broadcasting. The tests check the weights sum, the gray-preserving property and the statistics of a normalized random image.
