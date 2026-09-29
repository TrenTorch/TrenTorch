---
name: dl-training-module-base-class
title: Minimal Module base class (parameter collection)
tags: [neural-networks, layers, architecture]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every optimizer question in this Part, `sgd_step`, `adam_step`, `adamw_step`, all take a flat list of `params` and a matching flat list of `grads`. A real network is never that flat: it's built by nesting layers inside layers inside layers, a `Sequential` container (`[06-sequential-container]`, next in this track) might hold three `Linear` layers, each of which holds its own `weight` and `bias`. Somewhere, all of that nested structure needs to get flattened into the simple list the optimizer actually wants. Doing this by hand, walking every layer and manually collecting `layer.weight`, `layer.bias`, `layer2.weight`, ... for every layer in the network, would be repetitive and error-prone (easy to forget one layer), and would break the moment the network's architecture changed at all.

The standard solution, which every real deep learning framework uses in some form, is to give every layer a common base class that knows how to register its own parameters AND how to register child layers, then implement ONE recursive method, `parameters()`, that walks the whole nested structure and collects everything, no matter how deep the nesting goes.

### From theory to code

Implement `Module`, a class with three pieces: `__init__` sets up two empty dictionaries, `self._parameters` (name -> parameter array, for this module's OWN parameters) and `self._modules` (name -> child `Module`, for parameters that live one level deeper). `register_parameter(name, value)` and `register_module(name, module)` just store into those two dictionaries. `parameters()` does the actual work: return every value in `self._parameters`, PLUS every parameter returned by calling `.parameters()` on every child in `self._modules` (recursively, since a child could itself have children).

### Constraints

- `parameters()` must return parameters from this module AND from every descendant, at any nesting depth, not just direct children.
- The order doesn't need to match any particular convention, but every registered parameter (from every level) must appear exactly once.
- `register_parameter` and `register_module` are separate: a `Module` should never be stored in `self._parameters`, and a raw array should never be stored in `self._modules`.

### Hints

<details>
<summary>Hint 1</summary>

`self._parameters.values()` already gives you this module's own parameters as a plain list-like view; wrap it in `list(...)` to start building the result.

</details>

<details>
<summary>Hint 2: The recursive step</summary>

For each child module in `self._modules.values()`, call `child.parameters()`, NOT `child._parameters.values()`: calling the METHOD (not reaching directly into the dict) is what makes this work no matter how many levels deep the nesting goes, since each child's own `parameters()` call recurses into ITS children too.

</details>

## Theory

### The simple version

Think of a company's org chart. The CEO doesn't personally track every individual employee's timesheet; instead, each manager reports their own team's total hours up to THEIR manager, who adds it to their own team's total and reports further up. By the time it reaches the CEO, one single number reflects the whole company, without the CEO ever needing to know the org chart's exact shape or depth. `parameters()` works the same way: each `Module` reports its own parameters plus whatever its children report, and this same pattern, applied recursively, correctly flattens a tree of any depth without ever needing to know that depth in advance.

### The formula

There's no numerical formula here, this is a tree-traversal pattern rather than a math derivation, but it's worth writing out precisely because the recursive structure IS the insight:

```
parameters(module) = own_parameters(module) + concat(parameters(child) for child in module's children)
```

This is a textbook post-order tree traversal: each node's own contribution is combined with the RESULTS of recursing into its children (not with the children's raw data directly).

### How PyTorch actually implements this

`torch.nn.Module.parameters()` implements exactly this recursive pattern, though the real implementation is a `yield`-based generator (`self.named_parameters()` walks the module tree lazily rather than building the whole flat list up front) and additionally tracks a `requires_grad` flag per parameter (only parameters with `requires_grad=True` are yielded by default, since some parameters, like a frozen embedding layer's weights during fine-tuning, deliberately opt OUT of being trained). The reason `register_parameter` in real PyTorch is a full method rather than just direct dictionary assignment: PyTorch's `nn.Module.__setattr__` is actually OVERRIDDEN so that writing `self.weight = nn.Parameter(...)` inside any `nn.Module` subclass automatically calls the equivalent of `register_parameter` behind the scenes, and similarly, assigning `self.layer1 = nn.Linear(...)` automatically calls the equivalent of `register_module`, which is why real PyTorch code never needs to call either method explicitly. `optimizer = torch.optim.SGD(model.parameters(), lr=0.01)` is the direct real-world payoff of everything this question builds: the optimizer receives exactly the flat list this recursive `parameters()` produces.

## Explanation

`Module.__init__` sets up `self._parameters` and `self._modules` as empty dicts. `register_parameter` and `register_module` are thin wrappers that just assign into the corresponding dict under the given name.

`parameters()` starts with `list(self._parameters.values())`, this module's own parameters, then iterates `self._modules.values()` and, for each child, calls `child.parameters()` (recursively) and extends the running list with whatever comes back. Because each child's own `parameters()` call performs the identical recursive step for ITS children, this single method correctly collects every parameter at every depth of nesting, no matter how deep the module tree goes.
