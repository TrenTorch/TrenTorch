---
name: research-googlenet-conv-params
title: 'GoogLeNet: Counting Convolution Parameters'
tags: [research-papers, computer-vision, cnn, inception]
difficulty: Beginner
---

## Statement

### The problem, from first principles

GoogLeNet (Szegedy et al., 2015) builds inception modules from several parallel convolutions, using 1x1 convolutions to cut channels before the bigger kernels. Counting parameters per convolution shows where the cost sits.

### From theory to code

Implement `conv_params(c_in, c_out, k)`, the number of weights and biases in one convolution layer.

### Constraints

- Returns an integer.

### Hints

<details>
<summary>Hint 1</summary>

Multiply input channels, output channels and the kernel area, then add one bias per output channel.

</details>

## Theory

### The simple version

The first layer of GoogLeNet has 9472 parameters, so almost all of the network's cost sits in the deeper inception modules rather than the stem.

### The formula

$$P = c_{\text{in}}\,c_{\text{out}}\,k^2 + c_{\text{out}}$$

### How NumPy/PyTorch actually implements this

`sum(p.numel() for p in conv.parameters())` returns the same count in PyTorch.

## Explanation

Bias terms are one per output filter because each filter has a single shared offset.
