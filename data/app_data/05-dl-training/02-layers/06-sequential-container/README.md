---
name: dl-training-sequential-container
title: 'Sequential container: stack layers, one forward pass through all of them'
tags: [neural-networks, layers, architecture]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Most simple networks are just a straight chain: input goes through layer 1, that output goes through layer 2, and so on, until the final layer produces the network's output. Writing this chain out by hand every time, `x = layer1.forward(x); x = layer2.forward(x); x = layer3.forward(x)`, works, but it means the network's ARCHITECTURE (how many layers, in what order) is hardcoded into a specific block of code rather than being data you can construct, inspect, and reuse. `Sequential` turns "a chain of layers" into an actual object: something you build once from a list of layers, that then knows how to run the full chain itself.

`[05-module-base-class]`'s `Module` already solved half the problem: how to collect parameters from nested layers automatically. `Sequential` is where that machinery gets put to real use for the first time: it IS a `Module`, and each layer it holds is registered as one of ITS child modules, so `sequential_model.parameters()` transparently returns every layer's parameters, without `Sequential` itself needing to know anything about what kind of layers it's holding.

### From theory to code

Implement `Sequential`, a subclass of `Module` (already provided, reused from `[05-module-base-class]` via `load_solution`). `__init__(self, *layers)` accepts any number of layer objects (each with its own `.forward(x)` method), stores them in order, and registers each one as a child module using the inherited `register_module` method (so `self.parameters()`, inherited from `Module`, picks them all up automatically). `forward(self, x)` runs `x` through every layer in order, feeding each layer's output as the next layer's input, and returns the final result.

### Constraints

- Layers must be called in the exact order they were passed to `__init__`.
- Each layer must be registered as a child module (via `self.register_module`), using a distinct name for each (its index, as a string, works well).
- `forward` must work for any number of layers, including zero (in which case it should return `x` unchanged) and one.

### Hints

<details>
<summary>Hint 1</summary>

Store `self.layers = list(layers)` in `__init__`, then loop over `enumerate(self.layers)` and call `self.register_module(str(i), layer)` for each one, `str(i)` gives each layer a distinct registration name.

</details>

<details>
<summary>Hint 2</summary>

`forward` is a simple loop: `for layer in self.layers: x = layer.forward(x)`, then `return x`. Each iteration REPLACES `x` with that layer's output, which is exactly what feeds it into the next layer.

</details>

## Theory

### The simple version

An assembly line, where each station performs one operation on the part in front of it and passes the RESULT down the line to the next station, the final product coming off the end of the line is the accumulated effect of every station's own operation, applied in order. `Sequential.forward` is that same assembly-line pattern: each layer is a station, and `x` is the part moving down the line, transformed a little more at each stop.

### The formula

For layers `L1, L2, ..., Ln` and input `x`:

```
h1 = L1.forward(x)
h2 = L2.forward(h1)
...
output = Ln.forward(h_{n-1})
```

Or, more compactly, as a composition of functions: `output = Ln(...(L2(L1(x))))`.

### How PyTorch actually implements this

`torch.nn.Sequential` implements exactly this pattern, and, being a real `nn.Module` subclass, its `forward` (called automatically whenever you do `model(x)`, via `nn.Module.__call__`) is literally a loop over `self._modules.values()`, calling each one in order. Because `Sequential` inherits `parameters()` from `nn.Module` unchanged, `torch.optim.SGD(sequential_model.parameters(), lr=0.01)` transparently receives every layer's weights, exactly the payoff `[05-module-base-class]`'s recursive parameter collection was built for. One real limitation `Sequential`'s simplicity trades away: it can only express architectures that are a straight chain, one input, one output, per layer, so any architecture with a SKIP connection (like a ResNet's residual connections, or a Transformer's residual stream) needs a custom `nn.Module` subclass with its own hand-written `forward`, since `Sequential`'s rigid one-layer-feeds-the-next structure has no way to express "also add the ORIGINAL input back in later."

## Explanation

`__init__` stores the passed-in layers as `self.layers`, a plain list preserving their order, and separately registers each one under a string index via `self.register_module(str(i), layer)`, inherited unchanged from `Module`, which is what makes `.parameters()` (also inherited, unchanged) recursively collect every layer's parameters.

`forward` loops over `self.layers` in order, reassigning `x` to each layer's own `forward(x)` output before moving to the next layer, so by the time the loop finishes, `x` holds the result of every layer applied in sequence, which is then returned directly.
