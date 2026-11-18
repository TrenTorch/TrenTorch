---
name: research-vgg-conv-macs
title: 'VGG: Multiply-accumulates of a Convolution'
tags: [research-papers, computer-vision, cnn, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

VGG's cost is dominated by its convolutions. Counting multiply-accumulates per layer tells you where the compute goes, which matters when comparing it with later architectures.

### From theory to code

Implement `conv_macs(h, w, c_in, c_out, k)`, the multiply-accumulate count of one convolution.

### Constraints

- Default kernel is 3.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the output area, input channels, output channels and kernel area.

</details>

## Theory

### The simple version

Early VGG layers operate on large feature maps, so their cost is high even with few channels. The arithmetic makes that trade-off explicit.

### The formula

$$\text{MACs} = h\,w\,c_{\text{in}}\,c_{\text{out}}\,k^2$$

### How NumPy/PyTorch actually implements this

Profilers such as `fvcore` report exactly this count per convolution.

## Explanation

Each output value takes `c_in * k^2` multiply-accumulates, and there are `h * w * c_out` output values.
