---
name: rl-alignment-adapter-methods-prefix-prompt-tuning
title: 'Note: Adapter Methods, Prefix Tuning and Prompt Tuning, Other Parameter-Efficient Approaches'
tags: [reinforcement-learning, nlp, neural-networks]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`14-qlora-quantized-lora`'s LoRA adds a trainable low-rank matrix INSIDE each `Linear` layer's computation. That's not the only way to fine-tune a frozen base model cheaply — a whole family of "adapter" methods instead adds small, trainable pieces AROUND the frozen model, without touching any of its weights at all. Prefix tuning and prompt tuning are the two simplest, most illustrative examples of this different strategy.

### From theory to code

Implement `prefix_tuning_augment` (prepending learnable K/V vectors to every attention layer) and `prompt_tuning_augment` (prepending learnable token embeddings, only at the input), plus their respective trainable-parameter counts.

### Constraints

- `prefix_tuning_augment(key, value, prefix_keys, prefix_values)` returns `(concat([prefix_keys, key]), concat([prefix_values, value]))` — the prefix comes FIRST in sequence order.
- `prompt_tuning_augment(input_embeddings, soft_prompt_embeddings)` returns `concat([soft_prompt_embeddings, input_embeddings])`.
- `count_trainable_parameters_prefix_tuning(num_layers, prefix_len, hidden_dim)` returns `num_layers * prefix_len * hidden_dim * 2` (the factor of `2` is for BOTH the key and value prefix).
- `count_trainable_parameters_prompt_tuning(prompt_len, hidden_dim)` returns `prompt_len * hidden_dim` — independent of the number of layers.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Prefix tuning needs its OWN learnable key/value prefix at EVERY attention layer of the network — that's why its parameter count scales with `num_layers`, while prompt tuning only ever touches the very first, input-embedding layer.

</details>

<details>
<summary>Hint 2</summary>

Once `prefix_tuning_augment` produces a longer key/value sequence, it can be fed directly into `01-scaled-dot-product-attention`'s existing attention function unchanged — the prefix tokens simply become extra "keys" every query can attend to, exactly like any other token in the sequence.

</details>

## Theory

### The simple version

Imagine two ways to give an experienced consultant extra context before every meeting, without letting them rewrite any of their existing expertise: (1) hand them a fresh set of reference notes to keep in mind at EVERY stage of the discussion — opening remarks, technical deep-dive, closing summary, all separately (prefix tuning: one set of "notes" per layer), versus (2) just hand them one set of background notes right at the START of the meeting, and let their own normal reasoning process carry that context forward naturally through the rest of the conversation (prompt tuning: notes only at the input). Both let you steer behavior with a small, easily swappable set of instructions, without touching the consultant's actual underlying knowledge — but option 2 needs to store far less total "extra material" than option 1.

### The formula

```text
prefix_tuning_augment(k, v, pk, pv) = (concat([pk, k]), concat([pv, v]))    -- new K/V prefix, PER LAYER

prompt_tuning_augment(x, soft) = concat([soft, x])                          -- new embedding prefix, INPUT ONLY

count_trainable_parameters_prefix_tuning(L, p, d) = L * p * d * 2
count_trainable_parameters_prompt_tuning(p, d)    = p * d
```

Because prefix tuning needs its own prefix at EVERY layer, its parameter count scales with `num_layers`; prompt tuning's doesn't scale with depth at all, making it (for the same prefix length) always strictly cheaper — this exercise's `tests.py` confirms this ordering directly across realistic model sizes.

### How PyTorch actually implements this

Context only, untested by your submission: prefix tuning comes from "Prefix-Tuning: Optimizing Continuous Prompts for Generation" (Li & Liang, 2021), and prompt tuning from "The Power of Scale for Parameter-Efficient Prompt Tuning" (Lester et al., 2021) — both papers found that, especially at very large model scale, these lightweight methods can approach full fine-tuning's performance while training orders of magnitude fewer parameters, forming (alongside LoRA/QLoRA) the broader family of "parameter-efficient fine-tuning" (PEFT) techniques implemented in libraries like Hugging Face's `peft`.

## Explanation

`prefix_tuning_augment` prepends the learnable prefix vectors before the real keys/values, in sequence order — `tests.py` confirms feeding the augmented K/V into `01-scaled-dot-product-attention`'s real attention function genuinely changes the output (the prefix tokens are actually attended to, not just padding), while a zero-length prefix leaves attention completely unchanged, confirming the augmentation degrades gracefully to a no-op.

`prompt_tuning_augment` does the analogous thing at the embedding level — `tests.py` confirms the original embeddings are preserved exactly, just shifted later in the sequence, with the soft-prompt tokens occupying the new leading positions.

`count_trainable_parameters_prefix_tuning` and `count_trainable_parameters_prompt_tuning` make the two methods' relative cost concrete — `tests.py` verifies prefix tuning's count scales linearly with `num_layers` (confirming the per-layer factor of 2 for K and V is genuinely included, not accidentally dropped), while prompt tuning's count is completely independent of depth, and that for realistic transformer sizes, prompt tuning trains dramatically fewer parameters than prefix tuning for the same prefix length.
