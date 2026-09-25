---
name: vision-cnn-one-block
title: 'One CNN Block: Convolution, Activation, Pooling'
tags: [computer-vision, cnn]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A convolution alone is just a linear operation — stack two of them back to back with nothing in between and they collapse into one bigger linear operation, no more expressive than a single layer. Real networks need a nonlinearity between layers to actually gain expressive power, and they need periodic downsampling or the spatial size never shrinks. The standard building block that does both is exactly three operations in sequence: convolve, activate, pool.

This is the repeating unit nearly every classic CNN (LeNet, AlexNet, VGG) is built from — stack a few of these blocks (`03-stack-multiple-blocks`) and you have a feature extractor.

### From theory to code

Theory says the block is a strict pipeline: the convolution's output feeds directly into the activation, and the activation's output feeds directly into pooling. No new math — every piece already exists.

Implement `cnn_block(image, kernel, pool_size=2)` against that reasoning, reusing `05-multiple-output-filters`'s convolution, `02-deep-learning-core/02-activations/01-relu`'s ReLU, and `01-max-pooling`'s pooling.

### Constraints

- `image`: shape `(C_in, H, W)`. `kernel`: shape `(C_out, C_in, kH, kW)`.
- Order is fixed: convolve, then ReLU, then max-pool — never a different order.
- `pool_size` is passed straight through to the pooling step as its `kernel_size` (non-overlapping, stride defaults to `pool_size`).
- `image` and `kernel` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Three function calls, each one's output feeding the next one's input — no loop, no new arithmetic.

</details>

<details>
<summary>Hint 2</summary>

`conv2d_multi_filter(image, kernel)` → `relu_forward(...)` → `max_pool2d(..., kernel_size=pool_size)`, in that exact order.

</details>

## Theory

### The simple version

A convolution asks "how strongly does each learned pattern show up, everywhere in the image?" ReLU then says "only keep the positive evidence — a pattern either fired or it didn't, ignore how strongly it 'didn't'." Pooling then compresses that evidence down spatially, keeping only the strongest signal per small region. Chain those three ideas together and you have the standard CNN building block.

### The formula

```text
conv_out  = conv2d_multi_filter(image, kernel)
activated = relu_forward(conv_out)
output    = max_pool2d(activated, kernel_size=pool_size)
```

Without the ReLU in between, stacking two convolutional blocks would be mathematically equivalent to one larger convolution — nonlinearity between layers is what actually lets a deep network represent more than a single linear layer could.

### How PyTorch actually implements this

A real `nn.Module` writes this exact sequence — `nn.Conv2d` → `nn.ReLU()` → `nn.MaxPool2d(pool_size)` — inside its `forward` method, or bundles all three into one `nn.Sequential`. Every classic CNN classifier is built from repeating exactly this three-operation pattern, varying only the number of filters and how many blocks are stacked (`03-stack-multiple-blocks`).

## Explanation

`conv2d_multi_filter(image, kernel)` computes the raw, unactivated feature maps — some entries positive (the filter's pattern is present), some negative (it's actively absent, in the linear-algebra sense of a negative dot product). `relu_forward` clips every negative entry to exactly 0, keeping only "this pattern is present, to this degree" evidence and discarding the sign information a network's later layers don't need. `max_pool2d` then compresses the now-nonnegative feature maps spatially, keeping the single strongest activation per pooling window — since every remaining value is already `>= 0`, the max operation is picking out "the strongest evidence of this pattern in this region," a well-defined, ReLU-dependent notion the raw (possibly negative) conv output wouldn't support as cleanly.
