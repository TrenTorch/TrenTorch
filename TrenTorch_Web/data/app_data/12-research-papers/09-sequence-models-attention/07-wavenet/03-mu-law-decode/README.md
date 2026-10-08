---
name: research-wavenet-mu-law-decode
title: 'WaveNet: Mu-law Expansion'
tags: [research-papers, sequence-models, generative-audio, convolution]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Generating audio requires turning the predicted companded value back into a sample, which is the inverse of mu-law companding. Expansion is exponential, so small compressed values map to small amplitudes.

### From theory to code

Implement `mu_law_decode(y, mu)`, the inverse of the companding function.

### Constraints

- Mu-law decode inverts mu-law encode exactly.

### Hints

<details>
<summary>Hint 1</summary>

Raise one plus mu to the magnitude, subtract one, divide by mu, and restore the sign.

</details>

## Theory

### The simple version

Decoding the 256-way predictions this way recovers an amplitude per sample, which is the waveform WaveNet outputs.

### The formula

$$f^{-1}(y) = \operatorname{sign}(y)\,\frac{(1+\mu)^{|y|} - 1}{\mu}$$

### How NumPy/PyTorch actually implements this

Audio pipelines apply this expansion to model outputs before writing the wav file.

## Explanation

Encoding followed by decoding is the identity up to floating-point error, which the round-trip test checks.
