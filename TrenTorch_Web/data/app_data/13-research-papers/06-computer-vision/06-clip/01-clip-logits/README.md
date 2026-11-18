---
name: research-clip-logits
title: 'CLIP: The Similarity Matrix'
tags: [research-papers, computer-vision, vision-language, contrastive]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

CLIP (Radford et al., 2021) trains an image encoder and a text encoder so that matching pairs have high similarity. The first step is the full matrix of similarities between every image and every caption in the batch.

### From theory to code

Implement `clip_logits(img, txt, temp)`, returning the scaled cosine similarity matrix.

### Constraints

- Normalize each embedding before the dot products.

### Hints

<details>
<summary>Hint 1</summary>

Divide each row by its norm, multiply the image matrix by the transposed text matrix, then divide by the temperature.

</details>

## Theory

### The simple version

Diagonal entries are the true pairs, and off-diagonal entries are the in-batch negatives. The contrastive loss is built from this matrix.

### The formula

$$\ell_{ij} = \frac{\langle u_i, v_j\rangle}{\tau}, \qquad u, v \text{ unit-normalized}$$

### How NumPy/PyTorch actually implements this

CLIP's forward pass computes `image_features @ text_features.T * logit_scale` with the same normalization.

## Explanation

The temperature is learned in CLIP and typically starts near 0.07, which the logits divide by.
