---
name: research-resnet-depth-count
title: 'ResNet: Counting Layers in a Basic-block Network'
tags: [research-papers, computer-vision, cnn, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

ResNet names its models by depth, for example ResNet-18 and ResNet-34. In the basic-block design, the depth is a simple count: one stem convolution, two convolutions per residual block, and one classifier layer.

### From theory to code

Implement `resnet_depth(blocks)`, the nominal depth from the number of basic blocks per stage.

### Constraints

- Returns an integer.

### Hints

<details>
<summary>Hint 1</summary>

Two layers for the stem and classifier, plus two per block across all stages.

</details>

## Theory

### The simple version

The depth formula explains the names: ResNet-18 has eight basic blocks, and 2 + 2 * 8 = 18 layers counted as weight layers.

### The formula

$$D = 2 + 2\sum_{s} B_s$$

### How NumPy/PyTorch actually implements this

Model zoos name variants this way, and the depth is what the paper's table lists.

## Explanation

The count ignores the projection shortcuts, which are not counted as weight layers in the paper's naming.
