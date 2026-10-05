---
name: research-vit-seq-length
title: 'ViT: The Sequence Length With a Class Token'
tags: [research-papers, computer-vision, transformer, vision]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A ViT prepends a learnable class token to the patch tokens. The class token's final state is used for classification, so the sequence the transformer sees has one more entry than the patch count.

### From theory to code

Implement `vit_seq_length(img, p)`, the number of tokens the transformer processes.

### Constraints

- The class token is the first token.

### Hints

<details>
<summary>Hint 1</summary>

Count the patches, then add one.

</details>

## Theory

### The simple version

The class token gathers information from all the patches through attention, and the classifier reads it. The length is what determines the attention cost.

### The formula

$$L = \left(\frac{H}{P}\right)^2 + 1$$

### How NumPy/PyTorch actually implements this

timm and torchvision ViT implementations concatenate the class token before the transformer blocks.

## Explanation

Attention cost grows with the square of this length, which is why large images or small patches are expensive for ViT.
