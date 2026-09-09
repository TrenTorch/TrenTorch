# Theory: ReLU

## What

ReLU (Rectified Linear Unit) is `relu(x) = max(0, x)`: pass positive values through unchanged, zero out everything else. Its gradient is a step function -- 1 where `x > 0`, 0 where `x <= 0`.

## Why this became the default

Before ReLU, sigmoid and tanh were the standard hidden-layer activations, and both saturate: for large |x|, their gradient shrinks toward 0. Stack enough saturating layers and the gradient reaching the first layer during backpropagation vanishes almost entirely -- the network stops learning. ReLU's gradient is exactly 1 for every positive input, no matter how large, so it doesn't saturate on that side at all. That single property is most of why deep networks became trainable in practice.

## How it maps onto real PyTorch

`torch.relu(x)` and `torch.nn.functional.relu(x)` compute the forward pass exactly as implemented here. `nn.ReLU()` wraps it as a module. The backward pass you implement here is what PyTorch's autograd engine calls automatically when you call `.backward()` on a tensor that passed through a ReLU -- you're hand-writing the gradient rule that `torch.autograd.Function` would otherwise generate for you.

## When to use it (and when not to)

Default to ReLU for hidden layers in most feedforward and convolutional networks -- it's cheap (a single comparison, no `exp`) and avoids vanishing gradients on the positive side. Avoid it when a bounded or smooth output actually matters (an output layer producing a probability wants sigmoid or softmax, not ReLU) and watch for "dying ReLUs": a unit whose input is always negative for every training example gets a gradient of exactly 0 forever and never updates again. Variants like Leaky ReLU and GELU exist specifically to patch that failure mode.

## Pros and cons

- **Pros:** cheap to compute, no vanishing gradient for positive inputs, induces sparsity (exactly-zero activations), which real networks benefit from.
- **Cons:** gradient is exactly 0 for any negative input -- a unit can "die" and never recover; the function isn't differentiable at `x = 0` (in practice, implementations just pick a subgradient there, usually 0 or 1, and it doesn't matter).

## At scale

ReLU's simplicity is a real performance win, not just a training-stability one: `max(0, x)` is a single elementwise comparison, versus an exponential for sigmoid/tanh. Across a network with hundreds of millions of activations per forward pass, that difference in raw compute per element adds up, which is part of why ReLU (and its cheap variants) remain common even in architectures far larger than the ones where it was first shown to matter.
