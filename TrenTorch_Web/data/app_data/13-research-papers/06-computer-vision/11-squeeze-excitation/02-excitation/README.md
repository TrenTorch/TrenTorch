---
name: research-se-excitation
title: 'Squeeze-and-Excitation: The Excitation Gate'
tags: [research-papers, computer-vision, attention, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

The excitation step turns the channel summary into a gate for each channel. A small bottleneck with ReLU and a sigmoid output learns which channels to amplify and which to suppress.

### From theory to code

Implement `excitation(s, W1, W2)`, returning the sigmoid of the second projection applied to the ReLU of the first.

### Constraints

- The bottleneck width is C divided by a reduction ratio.

### Hints

<details>
<summary>Hint 1</summary>

Project down with `W1`, apply ReLU, project back up with `W2`, then take the sigmoid.

</details>

## Theory

### The simple version

The sigmoid bounds each gate between 0 and 1, so the block can only reweight channels, never flip their sign. The bottleneck keeps the parameter count low.

### The formula

$$s = \sigma\big(W_2\,\delta(W_1 z)\big), \qquad \delta = \text{ReLU}$$

### How NumPy/PyTorch actually implements this

SE implementations use two `Linear` layers and a `Sigmoid` for this exact computation.

## Explanation

The bottleneck reduction ratio in the paper is 16, which cuts the parameters of the gate by that factor.
