---
name: research-wavenet-receptive-field
title: 'WaveNet: Dilated Receptive Field'
tags: [research-papers, sequence-models, generative-audio, convolution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

WaveNet (van den Oord et al., 2016) models raw audio one sample at a time with stacked causal convolutions whose dilation doubles each layer. The receptive field grows exponentially with depth, so a few layers cover thousands of samples.

### From theory to code

Implement `wavenet_receptive_field(dilations, kernel)`, the number of past samples an output sees.

### Constraints

- Causal convolutions use only past samples.

### Hints

<details>
<summary>Hint 1</summary>

Start at one sample, then add (kernel minus one) times the dilation for each layer.

</details>

## Theory

### The simple version

Doubling the dilation each layer covers the past in logarithmic depth, which is why WaveNet can model long audio context cheaply.

### The formula

$$R = 1 + \sum_{\ell}(k-1)\,d_\ell$$

### How NumPy/PyTorch actually implements this

WaveNet implementations compute the same receptive field to size their causal padding.

## Explanation

With dilations 1 to 512 and kernel two, the field is 1024 samples, the paper's standard stack.
