---
name: dl-training-train-eval-mode
title: Train/eval mode switching
tags: [neural-networks, training, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[02-layers/03-dropout]` computes a genuinely DIFFERENT function depending on whether the network is currently training or being evaluated: during training, it randomly zeroes activations; during evaluation, it should pass everything through unchanged (no randomness at all, since you want a model's predictions on the same input to be deterministic and reproducible at inference time). Batch normalization (covered conceptually later in this Part, `Internal covariate shift, and what BatchNorm was actually designed to fix`) has an even sharper version of the same problem: it computes statistics from the CURRENT batch during training, but at inference time (often on a single sample, where "batch statistics" would be meaningless or wildly unstable) it needs to use FIXED statistics accumulated during training instead.

Both layers need to know, at the moment `forward` is called, which mode the network is currently in. Asking every training script to manually pass a `training=True/False` flag into every single layer's `forward` call, all the way through a deeply nested network, would be extremely error-prone (easy to forget for one layer buried three levels deep). The standard solution: give every layer a single shared `self.training` flag, and one recursive `train()`/`eval()` call on the TOP-LEVEL model that flips it for every layer in the whole tree at once.

### From theory to code

Implement `TrainableModule`, a subclass of `[02-layers/05-module-base-class]`'s `Module` (already provided, reused via `load_solution`), adding a `self.training` flag (starts `True`, since a freshly constructed model should default to training mode) and two methods: `train(mode=True)`, which sets `self.training = mode` on THIS module and recursively calls `.train(mode)` on every child module too (so calling `.train()` on the top-level model flips the flag for EVERY layer in the whole tree, no matter how deeply nested), and `eval()`, a convenience shortcut equal to `train(False)`.

### Constraints

- `train(mode)` must set `self.training` on the CURRENT module AND recursively propagate the same `mode` to every child module in `self._modules` (at any depth, since a child's own `train()` call recurses into ITS children too).
- `train()` (called with no arguments) must default to `mode=True`.
- `eval()` must be exactly equivalent to calling `train(False)`.
- Both `train` and `eval` should return `self`, so calls can be chained (matching PyTorch's own convention, e.g. `model.train().to(device)`).

### Hints

<details>
<summary>Hint 1</summary>

`self.training = mode` sets the flag on the current module. Then loop `for submodule in self._modules.values(): submodule.train(mode)`, calling the SAME method recursively, exactly the pattern `[05-module-base-class]`'s `parameters()` used for recursive parameter collection.

</details>

<details>
<summary>Hint 2</summary>

`eval` is a one-liner: `return self.train(False)`. Since `train` already returns `self`, `eval` gets the chaining behavior for free.

</details>

<details>
<summary>Hint 3</summary>

Don't forget `return self` at the end of `train`, after the loop, this is what allows `model.train()` to be chained with further calls.

</details>

## Theory

### The simple version

A restaurant kitchen switching between "prep mode" (before opening, chopping vegetables, testing new recipes, some steps deliberately randomized or exploratory) and "service mode" (during actual dinner service, every dish must come out exactly the same way, every time, no experimentation). The head chef flips ONE sign by the door, and every station in the kitchen, whether they read the sign directly or just follow the chef ahead of them, ends up behaving consistently with the same mode. `model.train()`/`model.eval()` is that one sign, propagated automatically to every layer.

### The formula

There's no numeric formula here, this is a tree-propagation pattern, structurally identical to `[05-module-base-class]`'s `parameters()` recursion, just setting a flag instead of collecting values:

```
train(module, mode):
    module.training = mode
    for child in module's children:
        train(child, mode)
```

### How PyTorch actually implements this

`torch.nn.Module.train(mode=True)` implements exactly this recursive flag-propagation, and `model.eval()` is literally defined as `return self.train(False)` in PyTorch's own source. Every built-in layer that behaves differently in training vs. eval, `nn.Dropout`, `nn.BatchNorm1d/2d/3d`, checks `self.training` directly inside its own `forward` method (an `if self.training: ... else: ...` branch), which is exactly why `TrainableModule`'s job is ONLY to keep that flag correctly synchronized across the whole tree, not to implement the different behaviors itself, those live inside each individual layer, exactly the separation of concerns `[02-layers/03-dropout]`'s `dropout_forward`/`dropout_backward` didn't need to handle directly, since a training script decides whether to CALL them at all (or call an eval-mode passthrough instead) based on this same flag. Forgetting `model.eval()` before running validation or test-set evaluation is one of the most common, and most silently-wrong, bugs in real PyTorch code: dropout stays active and batch norm keeps using batch statistics instead of its running averages, producing SYSTEMATICALLY different (and non-reproducible) numbers on data the model was never actually trained on incorrectly, just evaluated on incorrectly.

## Explanation

`TrainableModule.__init__` calls `super().__init__()` (setting up the inherited `_parameters`/`_modules` dicts) and additionally initializes `self.training = True`.

`train(mode)` sets `self.training = mode` on the current module, then loops over `self._modules.values()` and calls `submodule.train(mode)` on each one, recursively propagating the same mode to every descendant, before returning `self` for chaining. `eval()` is a one-line delegate to `self.train(False)`, inheriting both the propagation logic and the chaining return value for free.
