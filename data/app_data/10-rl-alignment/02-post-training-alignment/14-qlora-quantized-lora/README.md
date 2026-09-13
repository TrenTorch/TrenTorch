---
name: rl-alignment-qlora-quantized-lora
title: 'QLoRA: LoRA on Top of a Quantized Base Model'
tags: [reinforcement-learning, mlops, neural-networks]
difficulty: Advanced
---

## Statement

### The problem, from first principles

LoRA already makes fine-tuning cheap by training only a small pair of low-rank matrices while the base model's weights stay frozen. But "frozen" doesn't mean "small" — the base model still has to be loaded, in full precision, taking up exactly as much memory as it always did. QLoRA's contribution: since the base weights are frozen anyway, store them QUANTIZED (far less memory), only ever dequantizing on the fly for the forward pass's matmul, while the small LoRA matrices stay in full precision and train normally.

### From theory to code

Implement `compute_int8_scale`/`quantize_int8`/`dequantize_int8` (a self-contained int8 quantization scheme), `lora_delta` (LoRA's low-rank update), `qlora_linear_forward` (combining both), and `count_trainable_parameters`, quantifying just how few parameters QLoRA actually trains.

### Constraints

- `compute_int8_scale(weight)` returns `max(abs(weight)) / 127.0`.
- `quantize_int8(weight, scale)` returns `clip(round(weight / scale), -128, 127)` as `int8`; `dequantize_int8` reverses it (approximately — quantization is lossy).
- `lora_delta(input, lora_A, lora_B, alpha, rank)` returns `(alpha / rank) * (input @ lora_A.T) @ lora_B.T`, where `lora_A` has shape `(rank, in_features)` and `lora_B` has shape `(out_features, rank)`.
- `qlora_linear_forward` returns `input @ dequantize_int8(quantized_weight, scale).T + lora_delta(...)`.
- `count_trainable_parameters(in_features, out_features, rank)` returns `{"full_finetune": in_features * out_features, "qlora": rank * in_features + out_features * rank}`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The quantized base weight and the LoRA matrices play completely different roles: the base weight is dequantized and used EXACTLY like an ordinary (frozen) `Linear` layer's weight; the LoRA delta is added ON TOP, as a separate, small, trainable contribution.

</details>

<details>
<summary>Hint 2</summary>

`lora_delta`'s output can never have a matrix rank higher than `rank`, no matter how large the batch — `input @ lora_A.T` collapses each input row down to a `rank`-dimensional vector before `lora_B.T` expands it back up, which is exactly LoRA's "low-rank" name.

</details>

## Theory

### The simple version

Imagine a huge reference book that you're never allowed to rewrite (the frozen base model), but you're allowed to keep a small notepad of your OWN annotations alongside it (the LoRA matrices) that adjust how you interpret the book. QLoRA adds one more trick: since you're never rewriting the book anyway, why not store it in a much more compact, compressed form (quantized) on your shelf, only "decompressing" a page in your head right when you need to actually read it? Your notepad stays full-detail and fully editable; only the untouched reference material gets compressed.

### The formula

```text
compute_int8_scale(W) = max(abs(W)) / 127
quantize_int8(W, scale) = clip(round(W / scale), -128, 127)          -- lossy, stored as int8
dequantize_int8(Q, scale) = Q * scale                                  -- approximate reconstruction

lora_delta(x, A, B, alpha, r) = (alpha / r) * (x @ A.T) @ B.T          -- A: (r, in), B: (out, r)

qlora_linear_forward(x, Q, scale, A, B, alpha, r) = x @ dequantize_int8(Q, scale).T + lora_delta(x, A, B, alpha, r)

count_trainable_parameters(in, out, r) = {full_finetune: in*out, qlora: r*(in + out)}
```

Because `r` is typically tiny (often 4-64) relative to `in_features`/`out_features` (often thousands), `qlora`'s parameter count is usually a tiny fraction of `full_finetune`'s — but this isn't automatic: for `r` large enough relative to the dimensions (specifically once `r > in*out / (in+out)`), the low-rank factorization can actually need MORE parameters than the full matrix, which is exactly why real LoRA/QLoRA setups always use a small rank relative to the layer's dimensions.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact idea from "QLoRA: Efficient Finetuning of Quantized LLMs" (Dettmers et al., 2023), which combines LoRA with 4-bit (NF4) quantization of the frozen base weights specifically to make fine-tuning very large models feasible on a single consumer GPU — the paper reports fine-tuning 65-billion-parameter models this way, something a full-precision full fine-tune of the same model couldn't fit in memory for at all.

## Explanation

`compute_int8_scale`/`quantize_int8`/`dequantize_int8` implement a standard, self-contained per-tensor int8 quantization scheme — this exercise's `tests.py` confirms the round-trip recovers the original weight closely (not exactly, since quantization is inherently lossy) and that the quantized representation genuinely uses the `int8` dtype.

`lora_delta` computes the low-rank update directly — `tests.py` verifies its result independently against `np.linalg.matrix_rank`, confirming the delta's rank never exceeds the LoRA rank `r` regardless of batch size, a real structural guarantee that comes purely from factoring the update through a `rank`-dimensional bottleneck.

`qlora_linear_forward` combines both pieces: dequantize the frozen base weight just long enough to compute the base matmul, then add the LoRA delta on top — `tests.py` confirms the result closely matches a full-precision equivalent (`x @ W.T + lora_delta(...)`) despite the base weight having spent the entire time compressed in memory.

`count_trainable_parameters` makes QLoRA's efficiency concrete: `tests.py` confirms that for realistic (small) ranks relative to typical layer dimensions, the trainable parameter count is a tiny fraction of a full fine-tune's — while also being honest that this isn't true unconditionally, since it depends on `r` staying small relative to the layer's actual dimensions.
