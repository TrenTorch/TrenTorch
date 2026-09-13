---
name: vision-history-vgg-stack
title: 'VGG: Stacking Small 3x3 Convolutions'
tags: [computer-vision, cnn, history, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A single 5x5 convolution and two stacked 3x3 convolutions both let a pixel's output "see" a 5x5 neighborhood of the original input (their receptive fields match) — but they are not equivalent networks. The two-3x3 version has a ReLU sandwiched between the two convolutions, giving the network an extra nonlinearity for the same receptive field, and it has fewer parameters: `2 * (C^2 * 3 * 3) = 18*C^2` versus `C^2 * 5 * 5 = 25*C^2` for equal channel counts `C`. VGG's core insight, which became the default choice for essentially every CNN architecture afterward, is: stop reaching for large kernels — just stack more small (3x3) ones.

### From theory to code

Theory says: apply a same-padded 3x3 convolution, then a ReLU, then repeat with the next kernel in the stack, feeding each layer's output into the next as input.

Implement `vgg_stack(x, kernels)` against that reasoning, reusing this track's existing multi-filter convolution and ReLU.

### Constraints

- `x`: shape `(C, H, W)`.
- `kernels`: a list of 3x3 kernels, each shape `(C, C, 3, 3)` (channel count stays fixed through the stack).
- Every convolution uses padding 1 (so spatial size never changes, no matter how many layers are stacked).
- An empty `kernels` list returns `x` unchanged.
- Returns an array the same shape as `x`.
- `x` and every kernel are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A plain `for kernel in kernels:` loop, reassigning `x` to the result of each iteration, is all the "stacking" is — each layer's output becomes the next layer's input.

</details>

<details>
<summary>Hint 2</summary>

Inside the loop: `np.pad` by 1 pixel on H and W, run `conv2d_multi_filter`, then `relu_forward` the result, and that becomes the new `x` for the next iteration.

</details>

## Theory

### The simple version

Think of receptive field growth like word-of-mouth: after one 3x3 conv, each output pixel "knows about" its immediate 3x3 neighborhood. After a second 3x3 conv on top of that, each of ITS input pixels already summarized a 3x3 neighborhood of the original image, so the second layer's output pixel effectively knows about a 5x5 neighborhood of the very first input — the receptive field grows by 2 pixels per stacked 3x3 layer. Stack three and you match a 7x7 kernel's receptive field, but with three ReLUs (more expressive nonlinearity) and dramatically fewer parameters (`27*C^2` vs `49*C^2`).

### The formula

```text
x_0 = x
x_i = relu(conv2d_multi_filter(pad(x_{i-1}, 1), kernels[i]))   for i = 1 .. len(kernels)
return x_{len(kernels)}
```

Receptive field after `n` stacked 3x3 layers: `1 + 2*n` pixels per side.

### How PyTorch actually implements this

`torchvision.models.vgg16`/`vgg19` are literally `nn.Sequential` stacks of exactly this pattern — repeated blocks of `Conv2d(kernel_size=3, padding=1)` + `ReLU`, punctuated by max-pooling to reduce spatial size between blocks (this track's `02-pooling` questions). The "use small 3x3 kernels everywhere" convention VGG established is still the overwhelming default choice in modern CNN design: it's rare to see a hand-designed CNN reach for anything larger than 3x3, or occasionally 5x5, precisely because of this parameter-efficiency argument.

## Explanation

The `for kernel in kernels` loop reassigns `x` each iteration, which is exactly what "stacking" layers means computationally: layer `i`'s output becomes layer `i+1`'s input, with no other connection between them. `np.pad(x, ((0,0),(1,1),(1,1)))` pads only the spatial axes by 1 pixel per side, which is precisely what makes a 3x3 convolution "same"-padded — its output has the identical `(H, W)` as its input — so the spatial size survives the whole stack no matter how many layers are chained. Running `conv2d_multi_filter` then `relu_forward` at every step reuses the exact same convolution and activation this curriculum already built and tested independently — a VGG stack adds no new mathematics, only the repetition and the resulting receptive-field growth that repetition produces.
