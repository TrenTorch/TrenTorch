---
name: vision-network-in-network
title: Network in Network & Global Pooling
tags: [computer-vision, architectures, nin, global-average-pooling]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

AlexNet and VGG end with enormous fully connected layers that hold most of the network's parameters and overfit easily. **Network in Network** (NiN) replaces them with two ideas. First, after every ordinary convolution it adds two `1 x 1` convolutions with ReLUs: at each pixel these form a small multilayer perceptron applied to the channel vector, so every spatial position gets a deeper non-linear function. Second, the final convolutional layer produces **one feature map per class**, and the prediction is the **global average pool** of each map, a single number per class, fed directly to the softmax. No fully connected layer, almost no parameters in the head, and each map can be read as a heat-map of where the class evidence is.

### From theory to code

Implement `pointwise_mlp`, `global_avg_pool` and `nin_logits`.

### Constraints

- `x` has shape `(C, H, W)`. `pointwise_mlp(x, layers)` applies a list of `(W, b)` pairs, each a `1 x 1` convolution: `W` has shape `(C_out, C_in)` and `b` shape `(C_out,)`. The output of every layer except the last passes through ReLU; the last layer is linear. Return `(C_last, H, W)`.
- `global_avg_pool(x)` returns the length-`C` vector of spatial means.
- `nin_logits(x, layers)` applies `pointwise_mlp` and then `global_avg_pool`, returning one logit per output channel.

### Hints

<details>
<summary>Hint 1</summary>

A `1 x 1` convolution is `np.einsum('oc,chw->ohw', W, x) + b[:, None, None]`.

</details>

<details>
<summary>Hint 2</summary>

Because the last layer is linear, averaging after it equals applying it to the averaged input (a useful identity, tested).

</details>

## Theory

### The simple version

Instead of cramming the final picture through a huge funnel, each class gets its own heat-map and the verdict is the average brightness of the map.

### The formula

$$
h^{(\ell+1)}_{:,i,j} = \text{ReLU}\big(W^{(\ell)} h^{(\ell)}_{:,i,j} + b^{(\ell)}\big), \qquad z_k = \frac{1}{HW}\sum_{i,j} h^{(L)}_{k,i,j}
$$

### How this is done in practice

NiN's global average pooling head became standard: GoogLeNet, ResNet and nearly every modern CNN end with global average pooling and a single linear layer. The `1 x 1` convolutions are the same channel-mixing operation used in bottlenecks and in the depthwise-separable blocks of MobileNet.

## Explanation

Three small functions. The identity test (pooling commutes with the final linear layer) is a good way to see why global average pooling is parameter-free and shape-agnostic: it works for any input resolution.
