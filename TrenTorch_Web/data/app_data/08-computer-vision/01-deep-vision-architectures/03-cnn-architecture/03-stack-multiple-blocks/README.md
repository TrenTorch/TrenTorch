---
name: vision-cnn-stack-blocks
title: Stacking Multiple CNN Blocks
tags: [computer-vision, cnn]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

One CNN block (`02-one-cnn-block`) extracts one level of features and shrinks the spatial size once. A single block rarely learns anything rich enough for a real task — real image classifiers chain several blocks in sequence, each one operating on the PREVIOUS block's output rather than the raw image, so later blocks combine earlier features into progressively higher-level ones (edges → textures → parts → objects) while the spatial size keeps shrinking toward something small enough to flatten.

### From theory to code

Theory says: the first block sees the original image, and every later block sees the previous block's output. Chain them, feeding one into the next.

Implement `stack_cnn_blocks(image, kernels, pool_size=2)` against that reasoning, reusing `02-one-cnn-block`'s `cnn_block` once per kernel in the list.

### Constraints

- `image`: shape `(C_in, H, W)`.
- `kernels`: a list of kernels, one per block. Kernel `i`'s input-channel dimension must match block `i`'s actual input (either `image`'s own channels, for the first block, or the previous block's output channel count).
- `pool_size` is passed to every block identically.
- An empty `kernels` list returns `image` unchanged — zero blocks means no computation at all.
- `image` and every kernel in `kernels` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A single loop over `kernels`, reassigning your running result each iteration — the same pattern as a training loop repeating one update rule.

</details>

<details>
<summary>Hint 2</summary>

Start with `x = image`, then for each `kernel` in `kernels`, set `x = cnn_block(x, kernel, pool_size=pool_size)`. Return `x` after the loop.

</details>

## Theory

### The simple version

Imagine an assembly line where each station refines whatever the previous station handed it — the first station works on raw material (the image), every later station works on the PREVIOUS station's output, never the original material again. By the end of the line, what comes out has been refined through every station in sequence.

### The formula

```text
x = image
for kernel in kernels:
    x = cnn_block(x, kernel, pool_size)
return x
```

With `N` blocks, each one halving spatial size (for `pool_size=2`) and each convolution shrinking it a little further, spatial size drops fast — this is exactly why real CNN classifiers only need a handful of blocks before the feature map is small enough to flatten directly into a classifier head (`04-full-cnn-classifier`).

### How PyTorch actually implements this

`nn.Sequential(block1, block2, block3, ...)` does exactly this chaining — each block's `forward` output becomes the next block's input automatically, with no manual loop needed once the blocks are registered as an `nn.Sequential`. Every classic CNN architecture (LeNet, AlexNet, VGG) is, at its core, a specific choice of how many blocks to stack and how many filters each one uses — this question is that architectural decision reduced to its simplest possible form.

## Explanation

The loop reassigns `x` to each block's output before the next iteration reads it — this is exactly what "feed one block's output into the next block's input" means mechanically: there's no separate variable per block, just one running value threaded through every `cnn_block` call in order. An empty `kernels` list means the loop body never executes, so `x` stays exactly `image` — the "zero blocks" edge case falls out of the loop structure for free, with no special-case branch needed.
