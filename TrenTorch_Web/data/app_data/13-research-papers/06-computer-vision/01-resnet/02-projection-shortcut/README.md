---
name: research-resnet-projection-shortcut
title: 'ResNet: When the Shortcut Needs a Projection'
tags: [research-papers, computer-vision, cnn, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

The identity shortcut adds a block's input to its output. That works only when the shapes match. When the channel count or spatial size changes, ResNet uses a 1x1 projection on the shortcut so the addition is valid.

### From theory to code

Implement `needs_projection(c_in, c_out, stride)`, returning True when the shortcut cannot be an identity.

### Constraints

- Returns a bool.

### Hints

<details>
<summary>Hint 1</summary>

Compare the channel counts and check whether the stride is 1.

</details>

## Theory

### The simple version

A projection costs a few parameters but keeps the shortcut's addition well-defined, so the residual structure survives downsampling.

### The formula

$$\text{projection} \iff c_{\text{in}} \ne c_{\text{out}} \;\lor\; s \ne 1$$

### How NumPy/PyTorch actually implements this

torchvision's `BasicBlock` uses a 1x1 convolution with batch norm exactly when this condition holds.

## Explanation

The paper uses option B, a 1x1 convolution with the block's stride, for these shortcuts.
