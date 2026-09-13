---
name: systems-distributed-tensor-parallel-matmul
title: "Note: Tensor Parallelism, Splitting One Layer's Matmul Across GPUs"
tags: [mlops, neural-networks, distributed-training]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`02-pipeline-parallelism-bubble-fraction` split a model _between_ layers, putting different layers on different GPUs. Tensor parallelism goes a level deeper: it splits a SINGLE layer's matmul itself across GPUs, so even one `Linear` layer too big to fit on one GPU can still run — but naively splitting a matmul can silently produce the wrong answer unless you split it along the right axis, and know when the pieces can be combined by simple concatenation versus when they need to be summed.

### From theory to code

Implement `column_parallel_linear` and `row_parallel_linear` — the two standard ways (from Megatron-LM) to split a `Linear` layer's weight matrix across GPUs — plus the `split_weight_by_output_features`/`split_by_input_features` helpers that set each scheme up correctly.

### Constraints

- `column_parallel_linear`: each GPU holds a _row_-slice of the weight matrix (a slice of the OUTPUT features) and sees the SAME full input; the GPUs' outputs are concatenated along the last axis to reconstruct the full output — no communication needed mid-computation.
- `row_parallel_linear`: each GPU holds a _column_-slice of the weight matrix (a slice of the INPUT features) and only its matching slice of the input; each GPU computes a partial output, and the partials are summed (an all-reduce, `04-collective-communication-primitives`) before the (un-split) bias is added once.
- Both schemes must reconstruct `linear(input, weight, bias)` (`01-hypothesis-function`'s function) exactly, for any number of GPUs, including uneven splits.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Column-parallel splits the weight the same way `05-zero-optimizer-state-sharding` splits data — cleanly, with no cross-GPU math needed until the very last concatenation step, because each GPU's output columns don't depend on any other GPU's slice.

</details>

<details>
<summary>Hint 2</summary>

Row-parallel is different: each GPU's partial output is only PART of the correct answer (it's missing the contribution from every other GPU's input features), so a plain sum across GPUs — not a concatenation — is what reconstructs the true result.

</details>

## Theory

### The simple version

Imagine computing a long dot product, `a·w = a[0]*w[0] + a[1]*w[1] + ... + a[9]*w[9]`, by giving the first five terms to one person and the last five to another — each person's PARTIAL sum is meaningless on its own, but adding the two partial sums together gives the exact right answer. That's row-parallelism. Column-parallelism is different: it's like computing 10 SEPARATE, INDEPENDENT dot products (each against a different weight vector) on 10 different people — each person's single number is already a complete, correct piece of the final answer, so you just line the 10 answers up side by side.

### The formula

```text
column_parallel_linear(x, [W_1, ..., W_k], [b_1, ..., b_k]) = concat(linear(x, W_1, b_1), ..., linear(x, W_k, b_k))
    where each W_i is a ROW-slice of W (a slice of out_features)   -- no cross-GPU math needed

row_parallel_linear([x_1, ..., x_k], [W_1, ..., W_k], b) = sum(linear(x_i, W_i) for i in 1..k) + b
    where each W_i is a COLUMN-slice of W and x_i the matching INPUT slice   -- partials MUST be summed
```

Both schemes reconstruct the exact same full matmul — they just move the "seam" to a different place. Real transformer implementations chain them deliberately: Megatron-LM uses column-parallelism for a feed-forward block's first linear layer (whose output needs no cross-GPU communication going into the activation function) and row-parallelism for its second (whose output needs to be summed before it can be added back into the residual stream), minimizing the number of all-reduces needed per block.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact strategy from "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism" (Shoeybi et al., 2019). Frameworks like Megatron-LM and DeepSpeed's tensor-parallel modules implement `ColumnParallelLinear`/`RowParallelLinear` layers directly on top of this same column/row splitting logic, letting a single `Linear` layer's weight matrix span many GPUs' memory at once.

## Explanation

`column_parallel_linear` calls the existing `linear` function once per GPU shard (using that shard's own weight-and-bias slice against the _full_, un-split input), then concatenates the results along the last axis — since each shard computes entirely distinct output columns, concatenation alone reconstructs the true output exactly, with zero cross-GPU communication.

`row_parallel_linear` calls `linear` once per GPU shard too, but WITHOUT a bias (each shard's `x_i @ W_i.T` is only a partial contribution to every output element, using only that shard's slice of the input features), sums all the partials together, and adds the bias exactly once at the end — `tests.py` confirms the per-GPU partials genuinely differ from each other (so the sum step is doing real, necessary work) and that the final summed result exactly matches the true full-input, full-weight computation.

`split_weight_by_output_features` and `split_by_input_features` set up each scheme's inputs correctly — splitting along `axis=0` (rows) for column-parallelism versus `axis=1`/`axis=-1` (columns) for row-parallelism — and both are verified to work correctly even when the number of GPUs doesn't evenly divide the feature count.
