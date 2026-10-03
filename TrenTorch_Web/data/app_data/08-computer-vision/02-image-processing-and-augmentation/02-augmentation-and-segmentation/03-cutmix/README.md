---
name: vision-cutmix
title: CutMix
tags: [computer-vision, augmentation, regularization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Mixup blends whole images, producing ghostly overlays that never occur in real photos. **CutMix** instead cuts a rectangular patch out of one image and pastes it onto another, so every pixel still comes from a real image and the network must recognize objects from partial views. The label is mixed in proportion to the **actual area** each image contributes. The patch size comes from the mixing weight `lam`: the patch covers a fraction `1 - lam` of the image area, with width and height `sqrt(1 - lam)` times the image's. The patch centre is random, and clipping at the image border can shrink the patch, so the label weight is recomputed from the clipped area.

### From theory to code

Implement `cutmix_box`, `cutmix` and `adjusted_lambda`.

### Constraints

- `cutmix_box(H, W, lam, cy, cx)` returns `(y1, y2, x1, x2)` where `cut_h = int(H * sqrt(1 - lam))`, `cut_w = int(W * sqrt(1 - lam))`, `y1 = clip(cy - cut_h // 2, 0, H)`, `y2 = clip(cy + cut_h // 2, 0, H)` (same for `x` with `cx`).
- `cutmix(img_a, img_b, box)` returns a copy of `img_a` with the region `[y1:y2, x1:x2]` replaced by the same region of `img_b`. Images have shape `(H, W, ...)`.
- `adjusted_lambda(box, H, W)` returns `1 - (y2 - y1) * (x2 - x1) / (H * W)`, the fraction of the result that still comes from `img_a`.

### Hints

<details>
<summary>Hint 1</summary>

Compute the box first, then paste, then compute the label weight from the real pasted area, not from the requested `lam`.

</details>

<details>
<summary>Hint 2</summary>

`lam = 1` gives an empty box and leaves `img_a` untouched.

</details>

## Theory

### The simple version

Cutting a rectangle from one photograph and gluing it into another, then writing on the back "this picture is 75% beach, 25% mountain", counting the actual areas.

### The formula

$$
\tilde x = M \odot x_a + (1 - M) \odot x_b, \qquad \tilde y = \lambda' y_a + (1 - \lambda') y_b, \qquad \lambda' = 1 - \frac{\text{area}(M = 0)}{HW}
$$

### How this is done in practice

CutMix (Yun et al., 2019) is in `timm` and `torchvision.transforms.v2.CutMix`. It often outperforms mixup on image classification and is widely used in training recipes together with mixup, switched per batch.

## Explanation

The box arithmetic is the only subtle part: clipping near the border changes the pasted area, so the label must be recomputed afterwards, which is what the third function is for.
