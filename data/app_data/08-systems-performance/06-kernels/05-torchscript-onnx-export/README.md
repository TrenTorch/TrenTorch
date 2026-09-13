---
name: systems-perf-torchscript-onnx-export
title: 'Note: TorchScript and ONNX Export, Why Production Serving Does Not Run Eager Python'
tags: [mlops, kernels]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`05-acceleration` showed a Python `for` loop pays real, fixed overhead _per iteration_, purely for being interpreted. Eager-mode PyTorch has an analogous cost at a different level: every single tensor operation call pays its own fixed Python-and-framework "dispatch" overhead — deciding which underlying kernel to actually run, checking types and devices — completely separate from the actual math that operation performs. A model with hundreds of layers pays that dispatch tax hundreds of separate times, every single forward pass.

### From theory to code

Implement `eager_python_dispatch_overhead(num_ops, per_op_dispatch_seconds)`, `graph_mode_dispatch_overhead(per_op_dispatch_seconds)`, and `graph_mode_speedup_estimate(...)` — quantifying exactly the dispatch-overhead savings that exporting a model to TorchScript or ONNX (running as a compiled graph, not live Python) provides.

### Constraints

- `eager_python_dispatch_overhead` returns `num_ops * per_op_dispatch_seconds` — every op pays the dispatch cost separately.
- `graph_mode_dispatch_overhead` returns `per_op_dispatch_seconds` directly — paid exactly once, regardless of how many ops the underlying graph actually contains.
- `graph_mode_speedup_estimate` returns `eager_python_dispatch_overhead / graph_mode_dispatch_overhead`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This mirrors `04-torch-compile-graph-compilation`'s exact shape: one quantity that scales with `num_ops`, one quantity that stays flat regardless of `num_ops`, and a ratio between them.

</details>

<details>
<summary>Hint 2</summary>

`graph_mode_dispatch_overhead` doesn't even need `num_ops` as a parameter — the whole point is that a compiled graph's dispatch cost genuinely doesn't depend on how many operations are inside it.

</details>

## Theory

### The simple version

Imagine placing a hundred separate phone calls to a hundred different specialists to get a hundred small tasks done, versus placing one single phone call to a project manager who already knows to hand all hundred tasks to the right specialists internally. Both approaches get the same hundred tasks done — but the first pays the overhead of _placing a call_ a hundred separate times, while the second pays that same overhead exactly once. Eager-mode Python, dispatching one op call at a time, is the hundred separate phone calls; a compiled, exported graph is the single call to the project manager.

### The formula

```text
eager_python_dispatch_overhead(num_ops, per_op)  = num_ops * per_op
graph_mode_dispatch_overhead(per_op)             = per_op                    # paid once, ever
graph_mode_speedup_estimate                       = eager / graph = num_ops
```

### How PyTorch actually implements this

Context only, untested by your submission: `torch.jit.script`/`torch.jit.trace` (producing a TorchScript graph) and `torch.onnx.export` (producing an ONNX graph, runnable by a separate, non-Python ONNX Runtime) both exist specifically so a model's _entire_ computation graph can be handed to a runtime once, rather than re-dispatched one Python op call at a time on every single inference request — PyTorch's own deployment documentation names eliminating this per-op Python dispatch overhead as a specific, real motivation for exporting a graph rather than serving eager Python directly in production. This is a genuinely different benefit from `04-torch-compile-graph-compilation`'s operator fusion (which saves _memory traffic_): this savings is pure interpreter/framework bookkeeping overhead, present even for operations too different from each other to ever be fused together.

## Explanation

`eager_python_dispatch_overhead` is `num_ops * per_op_dispatch_seconds` directly — every operation in the forward pass independently pays the fixed cost of being dispatched from Python, and that cost accumulates linearly with however many operations the model calls.

`graph_mode_dispatch_overhead` returns `per_op_dispatch_seconds` on its own, with no multiplication by `num_ops` at all — this is the entire point: once a graph has been exported and handed to a runtime (TorchScript's own interpreter, or a separate ONNX Runtime), that runtime executes every operation inside the graph natively, without Python re-entering the picture between ops, so Python's own dispatch overhead is paid exactly once, for the single call into the runtime.

`graph_mode_speedup_estimate` divides the two, which reduces to exactly `num_ops` — the deeper a model's computation graph (the more individual ops its forward pass calls), the larger graph-mode execution's dispatch-overhead advantage over eager Python becomes.
