---
name: rl-alignment-full-finetune-vs-lora-comparison
title: 'Compare: Full Fine-Tune vs. LoRA, on Parameter Count and Memory'
tags: [reinforcement-learning, mlops, neural-networks]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`rl-alignment-lora-low-rank-adapters` built LoRA's forward and backward passes — this question quantifies exactly WHY anyone would bother: how many fewer parameters LoRA actually trains compared to a full fine-tune of the same layer, and — a second, often-overlooked source of savings — how much less optimizer memory that translates into, since a frozen parameter needs no optimizer state at all.

### From theory to code

Implement `full_finetune_parameter_count`, `lora_parameter_count`, `optimizer_state_bytes`, and `compare_full_finetune_vs_lora`, bundling all four numbers together for a single layer.

### Constraints

- `full_finetune_parameter_count(in_features, out_features)` returns `in_features * out_features + out_features` (weight matrix plus bias).
- `lora_parameter_count(in_features, out_features, rank)` returns `rank * in_features + out_features * rank`.
- `optimizer_state_bytes(num_trainable_params)` returns `num_trainable_params * 8` — Adam's fp32 momentum plus fp32 variance, 4 bytes each, PER TRAINABLE parameter only.
- `compare_full_finetune_vs_lora` bundles both parameter counts and both optimizer-memory figures, plus their ratio, into one dict.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Optimizer state is only ever computed for TRAINABLE parameters — a full fine-tune's optimizer memory scales with `full_finetune_parameter_count`, while LoRA's scales with the much smaller `lora_parameter_count`, since the frozen base weight needs zero bytes of optimizer state, not just zero gradient computation.

</details>

<details>
<summary>Hint 2</summary>

`compare_full_finetune_vs_lora` doesn't need any new math beyond calling the three other functions with the right arguments and packaging the results — the interesting part is just seeing all four numbers side by side.

</details>

## Theory

### The simple version

Imagine renovating a huge building: a full renovation means re-certifying and re-inspecting (the "optimizer state") every single room in the building, even the ones that aren't actually being changed. LoRA is like adding one small, self-contained new wing instead — you only need to certify and inspect the NEW wing's rooms, since the rest of the building was never touched at all. The savings come from two places at once: fewer rooms being changed, AND zero inspection overhead for the untouched ones.

### The formula

```text
full_finetune_parameter_count(in, out) = in * out + out

lora_parameter_count(in, out, r) = r * in + out * r = r * (in + out)

optimizer_state_bytes(n) = n * 8    -- fp32 momentum (4 bytes) + fp32 variance (4 bytes), per trainable param

parameter_reduction_factor = full_finetune_parameter_count / lora_parameter_count
```

For realistic transformer layer sizes (`in`/`out` in the thousands, `rank` in the single or low double digits), `lora_parameter_count` ends up a tiny fraction of `full_finetune_parameter_count` — but this isn't automatic for ANY rank: once `rank` gets large enough relative to `in`/`out` (specifically once `rank > in*out / (in+out)`), the low-rank factorization can actually need MORE parameters than the full matrix, which is exactly why real LoRA setups always keep `rank` small relative to the layer's dimensions.

### How PyTorch actually implements this

Context only, untested by your submission: this exact tradeoff — dramatically fewer trainable parameters, and correspondingly less optimizer state memory — is the headline practical justification given in the LoRA paper (Hu et al., 2021) for why it makes fine-tuning very large models tractable on modest hardware, and it's the same underlying idea `rl-alignment-qlora-quantized-lora` builds further on top of by also compressing the frozen base weight itself.

## Explanation

`full_finetune_parameter_count` and `lora_parameter_count` compute the two raw parameter counts directly from the layer's dimensions — `tests.py` confirms both formulas against hand computation and confirms LoRA's count is dramatically smaller for realistic dimensions.

`optimizer_state_bytes` scales a parameter count by Adam's fixed per-parameter overhead — `tests.py` confirms it's applied to the CORRECT (trainable-only) parameter count in each case, meaning a full fine-tune's optimizer memory is always strictly larger than LoRA's for the same layer, not just its parameter count.

`compare_full_finetune_vs_lora` packages everything together, and `tests.py`'s final oracle test confirms the full fine-tune's parameter count genuinely includes the bias term (`+ out_features`) rather than just the weight matrix's entries — a small but real detail that a careless implementation could easily drop.
