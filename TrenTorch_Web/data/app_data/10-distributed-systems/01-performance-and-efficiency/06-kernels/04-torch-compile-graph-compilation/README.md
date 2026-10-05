---
name: systems-perf-torch-compile-graph-compilation
title: 'Note: torch.compile / Graph Compilation, Why a JIT-Compiled Graph Beats Eager Mode'
tags: [mlops, kernels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

PyTorch's default execution mode is "eager": each line of Python that calls a tensor operation runs, and finishes, _immediately_, before Python even reaches the next line — exactly `01-kernel-fusion`'s "unfused" case, since nothing has the chance to look ahead at what's coming next and fuse anything together. `torch.compile` changes this: it traces a whole chunk of computation into a graph _first_, then compiles that entire graph, giving its compiler (TorchInductor) the opportunity to fuse chains of operations it can see coming.

### From theory to code

Implement `eager_mode_traffic(n_elements, n_ops, bytes_per_element=4)`, `compiled_graph_traffic(n_elements, n_ops, bytes_per_element=4)`, and `compiled_speedup_estimate(...)` — directly reusing `01-kernel-fusion`'s `unfused_memory_traffic`/`fused_memory_traffic`, since eager-vs-compiled execution is exactly unfused-vs-fused kernels applied to a whole model instead of just two ops.

### Constraints

- `eager_mode_traffic` is `01-kernel-fusion`'s `unfused_memory_traffic`, called with the same arguments.
- `compiled_graph_traffic` is `01-kernel-fusion`'s `fused_memory_traffic` — note it does _not_ actually use `n_ops` internally, even though it accepts the parameter (for a fair, same-signature comparison against `eager_mode_traffic`).
- `compiled_speedup_estimate` returns `eager_mode_traffic / compiled_graph_traffic`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This entire question is a thin wrapper — every function here is a direct call-through to `01-kernel-fusion`'s already-built functions, renamed to match this question's own vocabulary (eager vs. compiled, instead of unfused vs. fused).

</details>

<details>
<summary>Hint 2</summary>

`compiled_graph_traffic` accepts `n_ops` in its signature purely so it can be called with the exact same arguments as `eager_mode_traffic` at any call site — but it should never actually use that parameter in its own computation, matching `fused_memory_traffic`'s own behavior.

</details>

## Theory

### The simple version

Think of eager mode as following a recipe one instruction at a time, fully finishing (and cleaning up) each step before even reading the next instruction. `torch.compile` is like reading the _entire_ recipe first, noticing that three consecutive steps can actually be done together in one motion without ever putting the mixing bowl down in between, and then executing that combined, optimized version — the final dish is identical, but far less time was spent putting things down and picking them back up between steps.

### The formula

```text
eager_mode_traffic(n_elements, n_ops, bytes_per_element)     = unfused_memory_traffic(...)   # 01-kernel-fusion
compiled_graph_traffic(n_elements, n_ops, bytes_per_element) = fused_memory_traffic(...)      # 01-kernel-fusion, n_ops unused

compiled_speedup_estimate = eager_mode_traffic / compiled_graph_traffic = n_ops
```

The longer the chain of pointwise operations `torch.compile` can see in one traced graph, the bigger its fusion advantage — this is exactly why `torch.compile`'s speedup tends to be most dramatic on models built from many small operations (activation functions, normalization layers, elementwise arithmetic) rather than on a model dominated by one enormous matrix multiplication, which has nothing nearby to fuse with in the first place.

### How PyTorch actually implements this

Context only, untested by your submission: `torch.compile` traces a model's forward pass into an `FX` graph, then hands that graph to `TorchInductor`, which performs exactly this kind of pointwise-operator fusion (among other optimizations) before generating final Triton or C++ kernels — PyTorch's own `torch.compile` documentation cites this operator fusion as one of its primary sources of speedup over eager execution, the same memory-traffic accounting `01-kernel-fusion` already verified against the published literature.

## Explanation

`eager_mode_traffic` and `compiled_graph_traffic` are direct pass-throughs to `01-kernel-fusion`'s `unfused_memory_traffic` and `fused_memory_traffic` respectively — this question deliberately introduces no new computation, only new vocabulary, because eager-vs-compiled execution _is_ unfused-vs-fused kernel execution, applied to an entire traced graph rather than just two chained operations.

`compiled_speedup_estimate` divides the two, inheriting `01-kernel-fusion`'s exact conclusion: the speedup from compiling (fusing) a chain of `n_ops` pointwise operations together is, in this idealized memory-traffic accounting, precisely `n_ops` — the longer the fusable chain `torch.compile`'s graph tracing can see, the larger its advantage over running the same chain eagerly, one operation at a time.
