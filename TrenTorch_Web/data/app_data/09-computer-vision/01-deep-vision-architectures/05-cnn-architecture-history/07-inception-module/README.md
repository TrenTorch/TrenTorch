---
name: vision-inception-module
title: Inception Module
tags: [computer-vision, architectures, googlenet, multi-scale]
difficulty: Advanced
---

## Statement

### The problem, from first principles

How big should a convolution kernel be? A `1 x 1` kernel sees one position, a `3 x 3` sees a small neighbourhood and a `5 x 5` a wider one, and the right scale depends on the image. GoogLeNet's **Inception module** stops choosing: it runs several branches in parallel on the same input and **concatenates their outputs along the channel axis**, letting the next layer pick whatever is useful. Applying `5 x 5` kernels to every input channel would be expensive, so `1 x 1` convolutions first **reduce** the channel count (bottlenecks) before the larger kernels. A fourth branch max-pools and then projects with a `1 x 1` convolution. All branches keep the spatial size, so concatenation is possible.

### From theory to code

Implement `conv2d_same` and `inception_forward`.

### Constraints

- `x` has shape `(C, H, W)`. `conv2d_same(x, w)` with `w` of shape `(O, C, k, k)` (odd `k`) computes a stride-1 cross-correlation with zero padding `k // 2`, returning `(O, H, W)`. There is no bias.
- `inception_forward(x, p)` where `p` is a dict of weights: branch 1 is `relu(conv(x, p['b1']))` (1x1); branch 2 is `relu(conv(relu(conv(x, p['b2a'])), p['b2b']))` (1x1 reduce then 3x3); branch 3 is the same with `p['b3a']`, `p['b3b']` (1x1 then 5x5); branch 4 is a **3x3 max pool with stride 1 and padding 1** (pad with `-inf`) followed by `relu(conv(., p['b4']))` (1x1).
- Return the concatenation of the four branch outputs along axis 0, in the order 1, 2, 3, 4.

### Hints

<details>
<summary>Hint 1</summary>

Implement the convolution with a loop over the `k * k` shifts of the padded input, using `np.einsum('oc,chw->ohw', w[:, :, i, j], shifted)`.

</details>

<details>
<summary>Hint 2</summary>

Max pooling with stride 1 and padding 1 keeps `H x W`; pad with `-inf` so padding never wins.

</details>

## Theory

### The simple version

A committee of specialists looks at the same picture: one examines fine detail, another medium regions, another broad patches. Their reports are stacked together and the next committee decides which to trust.

### The formula

$$
\text{Inception}(x) = \big[\,f_{1\times1}(x)\;;\; f_{3\times3}(f_{1\times1}(x))\;;\; f_{5\times5}(f_{1\times1}(x))\;;\; f_{1\times1}(\text{maxpool}(x))\,\big]_{\text{channels}}
$$

Output channels $= O_1 + O_{2b} + O_{3b} + O_4$.

### How this is done in practice

GoogLeNet stacked nine such modules and won ImageNet 2014 with far fewer parameters than VGG. Inception-v3 factorizes `5 x 5` kernels into two `3 x 3` and `n x n` into `1 x n` followed by `n x 1`, and the bottleneck idea reappears in ResNet.

## Explanation

The convolution helper is reused for every branch. Tests verify the branches independently (a `1 x 1` convolution is a per-pixel matrix product) and the channel arithmetic of the concatenation.
