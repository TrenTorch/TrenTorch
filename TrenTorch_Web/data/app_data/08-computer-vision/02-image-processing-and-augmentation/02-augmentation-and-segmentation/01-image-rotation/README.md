---
name: vision-image-rotation
title: Image Rotation & Inverse Mapping
tags: [computer-vision, augmentation, geometry]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Rotation is a common augmentation: a cat tilted by ten degrees is still a cat. The obvious way to implement it is to take every input pixel and write it to its rotated position, but that leaves holes and collisions in the output, because rotated positions rarely land on pixel centres. The standard fix is **inverse mapping**: loop over the _output_ pixels, rotate each coordinate _backwards_ to find where it came from in the input, and read the input there. With **nearest-neighbour** sampling, round the source coordinate to the closest pixel. Output pixels whose source falls outside the image are filled with zero.

### From theory to code

Implement `rotate_nearest`.

### Constraints

- `img` has shape `(H, W)`. Rotate counterclockwise by `angle_deg` degrees about the image centre `((H - 1) / 2, (W - 1) / 2)`. The output has the same shape.
- For output pixel `(r, c)` with `dy = r - cy` and `dx = c - cx`, the source is `sy = cos(a) * dy + sin(a) * dx + cy` and `sx = -sin(a) * dy + cos(a) * dx + cx`, rounded with `np.rint`.
- If the rounded source is outside the image, the output pixel is `0`. For a square image, `rotate_nearest(img, 90)` equals `np.rot90(img)`.
- Do not modify the input.

### Hints

<details>
<summary>Hint 1</summary>

Build the coordinate grids with `np.meshgrid(..., indexing='ij')` and gather with a boolean validity mask.

</details>

<details>
<summary>Hint 2</summary>

Rotating by 0 degrees must reproduce the image exactly.

</details>

## Theory

### The simple version

Instead of moving every ink dot of a drawing to where it should go, you place a transparent rotated grid over a blank page and, for each cell, look up which part of the original drawing shows through.

### The formula

$$
\begin{pmatrix} s_y \\ s_x \end{pmatrix} = \begin{pmatrix} \cos a & \sin a \\ -\sin a & \cos a \end{pmatrix}\begin{pmatrix} r - c_y \\ c - c_x \end{pmatrix} + \begin{pmatrix} c_y \\ c_x \end{pmatrix}
$$

The matrix is the inverse (transpose) of the forward rotation, so output pixels sample the source, and every output pixel receives exactly one value.

### How this is done in practice

`torchvision.transforms.functional.rotate` and OpenCV's `warpAffine` implement this with a choice of interpolation (nearest, bilinear). Bilinear sampling gives smoother results and is the default for training augmentation. Labels that depend on geometry, like bounding boxes and keypoints, must be transformed together with the image.

## Explanation

Inverse mapping guarantees a value for every output pixel. The 90-degree test pins down the sign convention against NumPy's own rotation.
