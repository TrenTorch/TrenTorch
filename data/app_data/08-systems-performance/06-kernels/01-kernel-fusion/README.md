---
name: systems-perf-kernel-fusion
title: 'Kernel Fusion: Fuse Two Elementwise Ops into One Pass, Measure the Win'
tags: [mlops, kernels]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every elementwise operation (`relu`, a scalar multiply, adding a bias) is, on real hardware, a separate "kernel" launched one at a time — each one reads its entire input array from main memory, computes, and writes its entire output back to main memory, only for the _next_ op to immediately read that same data straight back in. Chaining `n` such ops means the data makes `n` unnecessary round trips through memory it never actually needed to leave.

### From theory to code

Implement `unfused_memory_traffic(n_elements, n_ops, bytes_per_element=4)`, the total bytes moved when each op in a chain runs as its own separate pass, and `fused_memory_traffic(n_elements, bytes_per_element=4)`, the total bytes moved if all those ops were fused into a single kernel that never materializes the intermediates. `fusion_speedup_estimate` reports the ratio between the two.

### Constraints

- `unfused_memory_traffic`: `n_ops` separate passes, each reading and writing a full `n_elements`-sized array.
- `fused_memory_traffic`: exactly one read and one write of an `n_elements`-sized array, regardless of `n_ops`.
- `fusion_speedup_estimate` returns `unfused_memory_traffic / fused_memory_traffic` for the same `n_elements`/`n_ops`/`bytes_per_element`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

One pass over `n_elements` elements moves `2 * n_elements * bytes_per_element` bytes total (one read direction, one write direction) — `unfused_memory_traffic` is just that number, times `n_ops` passes.

</details>

<details>
<summary>Hint 2</summary>

`fused_memory_traffic` never multiplies by `n_ops` at all — a fused kernel's memory traffic is a flat `2 * n_elements * bytes_per_element`, exactly like a _single_ pass, because it never writes an intermediate result to memory only to immediately read it back.

</details>

## Theory

### The simple version

Picture an assembly line where, after every single step, the half-finished product gets shipped all the way back to the warehouse and then shipped right back out again for the next step — even though the next station is standing right next to the one that just finished. Kernel fusion is simply removing that pointless round trip: perform every step on the product while it's still sitting right there on the workbench, and only ship the _finished_ product back to the warehouse at the very end.

### The formula

```text
unfused_memory_traffic(n_elements, n_ops, bytes_per_element) = n_ops * 2 * n_elements * bytes_per_element
fused_memory_traffic(n_elements, bytes_per_element)          = 2 * n_elements * bytes_per_element

fusion_speedup_estimate = unfused_memory_traffic / fused_memory_traffic = n_ops
```

The speedup from fusing `n_ops` pointwise operations together is, in this idealized accounting, exactly `n_ops` — fusing more operations together is strictly more valuable, with zero extra memory cost for adding another op to the fused chain (only more on-chip compute, which is typically far cheaper than a trip to main memory).

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact reasoning `torch.compile`'s operator fusion (via its TorchInductor backend) is built around — it identifies chains of pointwise operations in a traced computation graph and fuses them into single Triton kernels, specifically to eliminate this intermediate-materialization memory traffic. `02-roofline-model`, this track's next question, formalizes exactly _when_ this kind of savings actually translates into wall-clock speedup versus when it doesn't matter at all.

## Explanation

`unfused_memory_traffic` computes the bytes moved by a single pass (`2 * n_elements * bytes_per_element`, one read plus one write) and multiplies by `n_ops`, since each op in an unfused chain independently pays that full read-and-write cost.

`fused_memory_traffic` computes exactly the same single-pass formula, but never multiplies by `n_ops` — this is the entire point: a fused kernel's memory traffic doesn't grow with how many operations got fused inside it, since intermediate results between fused ops live only in fast on-chip registers, never touching main memory at all.

`fusion_speedup_estimate` divides the two, which algebraically reduces to exactly `n_ops` — a direct, quantitative statement of how much memory-traffic overhead fusion eliminates for a chain of that length.
