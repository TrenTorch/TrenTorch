---
name: research-wavenet-mu-law-encode
title: 'WaveNet: Mu-law Companding'
tags: [research-papers, sequence-models, generative-audio, convolution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

WaveNet quantizes each audio sample to 256 levels, and mu-law companding spaces those levels so that quiet sounds get finer resolution. The compressed signal is what gets quantized.

### From theory to code

Implement `mu_law_encode(x, mu)`, the logarithmic compression of the signal.

### Constraints

- Input samples lie in [-1, 1].

### Hints

<details>
<summary>Hint 1</summary>

Compute the log of one plus mu times the magnitude, divide by the log of one plus mu, and restore the sign.

</details>

## Theory

### The simple version

Logarithmic spacing matches human hearing, which is sensitive to small amplitude changes, so quantization error is more evenly perceived.

### The formula

$$f(x) = \operatorname{sign}(x)\,\frac{\ln(1 + \mu|x|)}{\ln(1+\mu)}$$

### How NumPy/PyTorch actually implements this

Speech codecs use the same companding curve, and WaveNet inherits it for its 256-way output.

## Explanation

The function is odd and maps the unit interval onto itself, so the output stays in range.
