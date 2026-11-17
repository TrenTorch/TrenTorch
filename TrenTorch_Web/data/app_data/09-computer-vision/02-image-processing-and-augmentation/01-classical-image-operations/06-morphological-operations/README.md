---
name: vision-morphological-operations
title: Morphological Operations
tags: [computer-vision, morphology, binary-images]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

After thresholding an image or predicting a segmentation mask you often get a binary image with specks of noise and small holes. **Morphological operations** clean it up by sliding a small structuring element over it. **Erosion** keeps a pixel only if the _whole_ element fits inside the white region around it, so it shrinks shapes and deletes specks smaller than the element. **Dilation** turns a pixel white if the element touches _any_ white pixel, so it grows shapes and fills small holes. Eroding then dilating is an **opening**: it removes small noise while mostly restoring the size of the large shapes.

### From theory to code

Implement `erode`, `dilate` and `opening`.

### Constraints

- `binary` is a 2-D array of 0 and 1. The structuring element is a full `k x k` square of ones with odd `k`. Pixels outside the image count as **0**.
- `erode(binary, k)`: output is 1 where all pixels in the `k x k` window centred on the pixel are 1.
- `dilate(binary, k)`: output is 1 where any pixel in the window is 1.
- `opening(binary, k)` is `dilate(erode(binary, k), k)`. All outputs have the input's shape and integer dtype.

### Hints

<details>
<summary>Hint 1</summary>

Pad with `k // 2` zeros, then take the minimum (erosion) or maximum (dilation) over the `k * k` shifted slices.

</details>

<details>
<summary>Hint 2</summary>

Erosion treats the border as background, so a shape touching the border loses its border pixels.

</details>

## Theory

### The simple version

Erosion is peeling a layer off every shape, dilation is adding one. Peel then add back and the little crumbs vanish while the big shapes return to nearly their original size.

### The formula

$$
(A \ominus B)(p) = \min_{b \in B} A(p + b), \qquad (A \oplus B)(p) = \max_{b \in B} A(p + b), \qquad A \circ B = (A \ominus B) \oplus B
$$

### How this is done in practice

OpenCV (`cv2.erode`, `cv2.dilate`, `cv2.morphologyEx`) and `scipy.ndimage.binary_*` provide these. Opening and its dual, closing (dilate then erode, which fills holes), are standard cleanup after segmentation, thresholding or document binarization.

## Explanation

Min and max filters over shifted slices implement both operations. Opening's two defining properties, removing small objects and leaving large ones nearly intact, are exactly what the tests assert.
