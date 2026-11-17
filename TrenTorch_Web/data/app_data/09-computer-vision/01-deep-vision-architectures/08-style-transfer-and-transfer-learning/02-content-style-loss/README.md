---
name: vision-content-style-loss
title: Content & Style Losses
tags: [computer-vision, style-transfer, loss-functions, optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Style transfer is optimization over the **pixels** of a new image, not over network weights. The pretrained CNN is frozen and the image is the parameter. The objective has two parts. The **content loss** keeps the generated image's feature maps close to those of the content photo at a deep layer, so the objects and layout are preserved. The **style loss** keeps the generated image's Gram matrices close to those of the style painting at several layers, so textures and colours match. A weighted sum of the two (plus a smoothness term, covered next) is minimized by gradient descent on the image. The weights express the trade-off between "looks like the photo" and "looks like the painting".

### From theory to code

Implement `content_loss`, `style_loss` and `total_loss`.

### Constraints

- `content_loss(gen_feat, content_feat)` is the mean squared error between two feature arrays of the same shape.
- `style_loss(gen_feats, style_feats, layer_weights)`: lists of `(C, H, W)` feature arrays, one per style layer. For each layer compute the Gram matrix (`F @ F.T / (C * H * W)` with `F = feat.reshape(C, -1)`) and the mean squared error between the generated and style Grams. Return `sum(w * mse)` over layers.
- `total_loss(content, style, tv, w_content, w_style, w_tv)` returns `w_content * content + w_style * style + w_tv * tv`.

### Hints

<details>
<summary>Hint 1</summary>

Reuse the same Gram computation for both images.

</details>

<details>
<summary>Hint 2</summary>

All three functions return Python floats.

</details>

## Theory

### The simple version

Painting a copy of a photo in someone else's style: one measure checks that the shapes still match the photo, another that the brushwork matches the artist, and you balance them.

### The formula

$$
\mathcal{L} = \alpha\,\underbrace{\lVert \phi_\ell(x) - \phi_\ell(c)\rVert^2}_{\text{content}} + \beta\sum_\ell w_\ell\,\underbrace{\lVert G_\ell(x) - G_\ell(s)\rVert^2}_{\text{style}} + \gamma\,\text{TV}(x)
$$

### How this is done in practice

The original method (Gatys et al., 2015) uses VGG-19 with content at `conv4_2` and style at five layers, optimizing with L-BFGS. Feed-forward variants train a network to produce the stylized image in one pass, using the same loss.

## Explanation

The first two terms are plain mean squared errors in different spaces: feature space and Gram space. The tests check that identical inputs give zero loss and that style loss ignores spatial rearrangement.
