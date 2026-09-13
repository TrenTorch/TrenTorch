---
name: systems-perf-autocast-concept
title: 'Autocast Concept: Which Ops Run in Reduced Precision, Which Stay in FP32'
tags: [mlops, neural-networks, mixed-precision]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`02-loss-scaling` fixed one specific failure mode (gradients underflowing during backward), but it didn't answer a more basic question: should EVERY operation in a model actually run in `float16`? `01-fp16-bf16-representable-range` already showed `float16` has real numerical hazards — running every single op at reduced precision would hit those hazards constantly, especially in operations that sum many values or exponentiate a wide range of numbers.

### From theory to code

Implement `should_run_in_fp16(op_name)`, which classifies a named operation as safe for `float16` or requiring `float32`, and `autocast_dtype_for(op_name)`, which turns that classification directly into a dtype string.

### Constraints

- `should_run_in_fp16` returns `True` for matmul-family ops (`matmul`, `linear`, `conv2d`, `relu`), `False` for reduction/normalization ops (`softmax`, `log_softmax`, `layer_norm`, `batch_norm`, `cross_entropy`, `sum`, `mean`, `exp`, `log`).
- An op name in neither list raises `ValueError`.
- `autocast_dtype_for` returns `"float16"` or `"float32"` directly, built on `should_run_in_fp16`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Two fixed sets of known op names is all the "classification" here really is — no clever heuristic, just a lookup against two explicit lists.

</details>

<details>
<summary>Hint 2</summary>

Check the `_FP32_REQUIRED_OPS` set first: if an op is in neither set, it's genuinely unknown and should raise, not silently default to one side or the other.

</details>

## Theory

### The simple version

Autocast doesn't run an entire model in `float16` — it runs each individual operation at whichever precision is actually safe for that specific kind of math. Matrix multiplications and convolutions are dominated by huge numbers of small multiply-adds, each individually tolerant of `float16`'s reduced precision, and they're also the actual computational bottleneck `float16` speeds up the most (modern GPUs have dedicated hardware that runs `float16` matmuls dramatically faster than `float32` ones). Reductions and exponentials — summing many values together, or exponentiating a wide range of numbers, exactly what softmax and layer/batch norm do internally — are numerically fragile in `float16` and need `float32`'s extra range and precision to avoid the underflow/overflow hazards `01-fp16-bf16-representable-range` studied.

### The formula

```text
should_run_in_fp16(op_name):
    if op_name in FP32_REQUIRED_OPS: return False
    if op_name in FP16_SAFE_OPS:     return True
    raise ValueError(unknown op)

autocast_dtype_for(op_name) = "float16" if should_run_in_fp16(op_name) else "float32"
```

### How PyTorch actually implements this

`torch.autocast` (and its older alias `torch.cuda.amp.autocast`) maintains exactly this kind of per-op categorization internally, published in PyTorch's own documentation as "Ops that autocast to `float16`" (matmul-family: `matmul`, `addmm`/`linear`, `conv2d`, and similar) versus "Ops that autocast to `float32`" (`softmax`, `layer_norm`, `batch_norm`, `cross_entropy`/`nll_loss`, and other reduction-heavy ops) — this exercise's two sets mirror those real, published categories rather than inventing a new classification scheme. Wrapping a forward pass in `with torch.autocast(device_type="cuda", dtype=torch.float16):` applies this per-op dispatch automatically, so a model author never has to manually cast individual layers.

## Explanation

`should_run_in_fp16` checks `_FP32_REQUIRED_OPS` first — if the op is there, it needs `float32` and the function returns `False` immediately. Otherwise, it checks `_FP16_SAFE_OPS`; if found there, it's safe for `float16` and returns `True`. Any op name matching neither set is genuinely unrecognized, and raising `ValueError` rather than guessing prevents a typo'd or unsupported op name from silently defaulting to the wrong precision.

`autocast_dtype_for` is a one-line wrapper around `should_run_in_fp16`, turning its boolean answer directly into the dtype string a real casting call would actually need — the same `True`/`False` decision, expressed as `"float16"`/`"float32"` instead.
