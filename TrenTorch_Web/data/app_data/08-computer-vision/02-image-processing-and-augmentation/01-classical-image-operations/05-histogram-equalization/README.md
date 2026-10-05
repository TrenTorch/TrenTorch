---
name: vision-histogram-equalization
title: Histogram Equalization
tags: [computer-vision, contrast, histogram]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A photo taken in fog or dim light uses only a narrow band of the available brightness range, so everything looks washed out. **Histogram equalization** stretches the used range so that brightness values are spread as evenly as possible across all 256 levels, which raises contrast. The trick is to map each gray level through the image's own **cumulative distribution function** (CDF): a level that is above 30% of the pixels maps to about 30% of the way up the output range. The mapping is a lookup table that depends only on the histogram, and it is monotone, so the order of brightness is preserved.

### From theory to code

Implement `equalize_histogram`.

### Constraints

- `img` is a 2-D `uint8` array. Compute the histogram of the 256 levels and its cumulative sum `cdf`.
- Let `cdf_min` be the CDF value at the smallest gray level present and `N = img.size`. The lookup table is `lut[v] = round((cdf[v] - cdf_min) / (N - cdf_min) * 255)` for levels `v`, clipped to `[0, 255]`. If `N == cdf_min` (a constant image) return the image unchanged.
- Return `lut[img]` as `uint8`. Use `np.round` (halves to even).

### Hints

<details>
<summary>Hint 1</summary>

`np.bincount(img.ravel(), minlength=256)` is the histogram.

</details>

<details>
<summary>Hint 2</summary>

The lowest present level always maps to 0 and the highest to 255.

</details>

## Theory

### The simple version

Imagine ranking all pixels from darkest to brightest and then repainting them so equal ranks are spaced evenly on the brightness scale. Pixels keep their order but gain separation.

### The formula

$$
h(v) = \frac{\text{cdf}(v) - \text{cdf}_{\min}}{N - \text{cdf}_{\min}}\cdot 255
$$

For a continuous image the transformed brightness is uniformly distributed; for 8-bit images the result is only approximately flat because pixels with the same level cannot be split.

### How this is done in practice

OpenCV's `cv2.equalizeHist` implements this formula. CLAHE applies it per tile with a clip limit to avoid amplifying noise, and is the standard choice for medical and satellite imagery.

## Explanation

Histogram, cumulative sum, table lookup. The lookup is why equalization is fast: the per-pixel work is one indexing operation.
