---
name: dl-training-lazylinear
title: 'LazyLinear: infer in_features from the first real forward call'
tags: [neural-networks, layers, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-linear-forward]`'s `linear_forward` needs `weight` to already exist, with a specific `in_features` baked into its shape, before it can run at all. That's a real inconvenience when building a network: `in_features` for the FIRST layer of a network usually depends on the shape of your actual dataset (how many pixels an image has after flattening, how many features a tabular dataset has after preprocessing), which you may not want to compute and pass in by hand every time you experiment with a new dataset or a different preprocessing pipeline. `LazyLinear` removes this friction: you only ever specify `out_features` up front, and `in_features` gets figured out automatically, the FIRST time real data actually flows through the layer.

The tricky part isn't the inference itself (`x.shape[-1]` tells you `in_features` immediately), it's making sure the layer only does this ONCE: every forward call after the first one must reuse the exact same `weight` and `bias` it created on that first call, not silently reinitialize (and therefore erase any training progress) on every subsequent call.

### From theory to code

Implement `LazyLinear.forward(self, x)`. `self.weight` and `self.bias` start as `None` (already set up in `__init__`, along with `self.weight_init`/`self.bias_init`, the functions to call for generating fresh initial values). On the FIRST call to `forward`, if `self.weight is None`, infer `in_features = x.shape[-1]`, call `self.weight_init(in_features, self.out_features)` and `self.bias_init(self.out_features)` to create the actual arrays, register them as parameters (via the inherited `self.register_parameter`, from `[05-module-base-class]`), and store them on `self`. On every call (first and all subsequent), delegate the actual computation to `linear_forward` (already provided, reused from `[01-linear-forward]`).

### Constraints

- The very first call to `forward` must create `self.weight` with shape `(out_features, in_features)` and `self.bias` with shape `(out_features,)`, using `x`'s LAST dimension as `in_features`.
- Every subsequent call must reuse the SAME `weight`/`bias` objects created on the first call, never re-running the initializers again.
- The actual output computation, on every call, must delegate to `linear_forward`, not reimplement it.

### Hints

<details>
<summary>Hint 1: The "only once" check</summary>

`if self.weight is None:` is exactly the right guard: it's `None` only before the very first call, and becomes a real array immediately after, so this check alone prevents any re-initialization on later calls.

</details>

<details>
<summary>Hint 2: Inferring in_features</summary>

`x.shape[-1]` is the size of `x`'s LAST dimension, which for a batch of shape `(batch_size, in_features)` is exactly `in_features`, regardless of what `batch_size` happens to be.

</details>

<details>
<summary>Hint 3: Don't forget to register</summary>

After creating `self.weight` and `self.bias` inside the `if` block, call `self.register_parameter("weight", self.weight)` and `self.register_parameter("bias", self.bias)` so `.parameters()` (inherited from `Module`) picks them up, exactly like a normal, non-lazy layer would.

</details>

## Theory

### The simple version

Ordering a custom-tailored suit without first knowing your own measurements: instead of guessing a size up front and hoping it fits, the tailor takes your measurements at the FIRST fitting, cuts the suit to match exactly, and every future alteration works from that same, now-known, measurement, never re-measuring you from scratch each time you come in. `LazyLinear` defers "measuring" (`in_features`) until the first real data (the first "fitting") arrives, then locks it in permanently.

### The formula

There's no new numerical formula here beyond `[01-linear-forward]`'s: `y = x @ weight.T + bias`. The interesting part is the CONTROL FLOW around when `weight` and `bias` get created:

```
if weight is None:
    in_features = x.shape[-1]
    weight = weight_init(in_features, out_features)
    bias = bias_init(out_features)
return linear_forward(x, weight, bias)
```

### How PyTorch actually implements this

`torch.nn.LazyLinear` (and PyTorch's broader "lazy module" mechanism, `torch.nn.modules.lazy.LazyModuleMixin`) implements exactly this deferred-initialization pattern, and it's genuinely used in real code: it's common in quick prototyping, and PyTorch's own `torchvision` model definitions occasionally use lazy layers to avoid manually computing a flattened feature-map size after a stack of convolutions. Internally, PyTorch represents the not-yet-initialized weight as a special `UninitializedParameter` object rather than plain `None`, and the FIRST real forward call triggers a one-time `initialize_parameters` hook that swaps it out for a real, correctly-shaped `nn.Parameter`; a subtlety real PyTorch has to handle that this simplified version does not: `LazyLinear` can't be moved to a GPU device or wrapped in a `DataParallel` BEFORE its first forward call, since there's no real tensor yet to move, which is a common, well-documented gotcha for anyone using lazy layers in a real training pipeline.

## Explanation

`forward` starts by checking `if self.weight is None:`, true only before the first real call. Inside that block, it reads `in_features = x.shape[-1]` directly off the input, calls `self.weight_init` and `self.bias_init` to produce the actual arrays, assigns them to `self.weight`/`self.bias`, and registers both via `self.register_parameter`. After that block (which is skipped entirely on every call after the first, since `self.weight` is no longer `None`), the function calls `linear_forward(x, self.weight, self.bias)` and returns its result, exactly reusing `[01-linear-forward]`'s implementation rather than duplicating the matrix multiplication and bias-add logic here.
