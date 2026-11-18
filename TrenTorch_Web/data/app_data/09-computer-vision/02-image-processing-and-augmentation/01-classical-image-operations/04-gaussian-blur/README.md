---
name: vision-gaussian-blur
title: Gaussian Blur
tags: [computer-vision, filtering, convolution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Blurring averages each pixel with its neighbours, which suppresses noise and fine detail. A box blur weights all neighbours equally, which leaves visible blocky artifacts. A **Gaussian blur** weights neighbours by a bell curve centred on the pixel, so near pixels count more than far ones, and the result looks smooth and natural. The width of the bell is the standard deviation `sigma`, and the kernel's size should cover about three standard deviations on each side. The kernel must sum to 1 so that blurring preserves overall brightness. Because the 2-D Gaussian is the product of two 1-D Gaussians, it is **separable**: blurring rows then columns with a 1-D kernel gives the same result as one 2-D convolution at a fraction of the cost.

### From theory to code

Implement `gaussian_kernel` and `gaussian_blur`.

### Constraints

- `gaussian_kernel(size, sigma)` returns the 1-D kernel of odd length `size`: `w[k] = exp(-(k - r)**2 / (2 sigma**2))` for `k = 0..size-1` with `r = size // 2`, normalized to sum to 1.
- `gaussian_blur(img, size, sigma)` blurs a 2-D image by applying the 1-D kernel along rows and then along columns. Pad by `size // 2` pixels with **edge replication** (`np.pad(mode='edge')`) so the output has the same shape as the input.
- Use cross-correlation; the kernel is symmetric so flipping makes no difference.

### Hints

<details>
<summary>Hint 1</summary>

Along an axis, the blurred value is a weighted sum of `size` shifted slices of the padded image.

</details>

<details>
<summary>Hint 2</summary>

A single bright pixel in a zero image becomes a copy of the 2-D kernel `outer(w, w)`.

</details>

## Theory

### The simple version

Looking at the photo through frosted glass whose frosting is thickest at the centre of each point: nearby details bleed together, far ones do not.

### The formula

$$
G(x, y) = \frac{1}{2\pi\sigma^2}e^{-(x^2 + y^2)/(2\sigma^2)} = g(x)\,g(y), \qquad
(I \star G) = (I \star_x g) \star_y g
$$

Separability turns an $O(k^2)$ per-pixel operation into $O(2k)$.

### How this is done in practice

OpenCV's `GaussianBlur` and `torchvision.transforms.GaussianBlur` are separable implementations. In vision pipelines blur is used for denoising, as the first step of edge detectors and to build scale-space pyramids for feature detection.

## Explanation

The kernel is a sampled and normalized bell curve. The blur reuses it twice with edge padding. The impulse-response test confirms that separable filtering equals the full 2-D kernel.
