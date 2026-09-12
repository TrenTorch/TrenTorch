---
name: txf-llmeng-mixture-of-experts
title: 'Mixture of Experts: top-k gating, route each token to its best expert FFN'
tags: [transformers, nlp]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[01-transformer-block/04-feedforward-sublayer]`'s FFN applies the exact SAME weights to every single token, regardless of what that token actually is: every token pays the full compute cost of the entire FFN, whether or not it needed all of that capacity. Mixture of Experts (MoE) architectures ask a pointed question: what if, instead of one large FFN every token must pass through, a model had MANY smaller "expert" FFNs, and each token only needed to pass through a FEW of them, chosen dynamically based on the token's own content? A learned "gating" network scores every expert for every token, and only the top-scoring experts actually run for that token, letting the model have a HUGE total parameter count (many experts) while keeping the actual COMPUTE per token comparable to a much smaller dense model, since most experts are simply never invoked for any given token.

This is a genuinely different kind of scaling lever than everything earlier in this curriculum: `[01-transformer-block]`'s FFN scales compute and parameters TOGETHER (a bigger `d_ff` costs more compute for every token), while MoE scales PARAMETERS (more experts) largely independently of compute (still only `top_k` experts run per token, regardless of how many total experts exist).

### From theory to code

Implement `moe_gate(x, gate_weight, top_k)`, scoring every expert and keeping only the `top_k` highest-scoring ones (softmax-renormalized among just those `top_k`), and `moe_ffn_forward(x, gate_weight, expert_params, top_k)`, routing each token through its own selected experts and combining their outputs via the gate's weights.

### Constraints

- `moe_gate` scores ALL experts (`x @ gate_weight.T`), then keeps only the `top_k` highest scores per token, discarding the rest ENTIRELY (not merely down-weighting them).
- The kept `top_k` scores are re-normalized via softmax AMONG THEMSELVES, so they still sum to `1`, even though the full expert population was much larger.
- `moe_ffn_forward` runs each token's `top_k` selected experts' OWN independent FFN (via `[01-transformer-block/04-feedforward-sublayer]`'s `feedforward_sublayer`, one call per selected expert), and combines their outputs as a WEIGHTED SUM using the gate weights.
- A non-selected expert's weights must have NO effect on a token's output; only the `top_k` experts actually chosen for that specific token contribute anything.

### Hints

<details>
<summary>Hint 1: The gate</summary>

```python
gate_logits = x @ gate_weight.T          # (..., num_experts)
top_indices = np.argsort(gate_logits, axis=-1)[..., -top_k:]
top_logits = np.take_along_axis(gate_logits, top_indices, axis=-1)
top_weights = softmax_last_axis(top_logits)
```

</details>

<details>
<summary>Hint 2: Routing and combining</summary>

For each token, loop over its `top_k` selected expert indices, run `feedforward_sublayer` using THAT expert's own `weight1`/`bias1`/`weight2`/`bias2`, and accumulate `weight * expert_output` into that token's final output. A token's total output is the sum of exactly `top_k` (weighted) expert outputs, never all `num_experts` of them.

</details>

## Theory

### The simple version

`[04-feedforward-sublayer]`'s plain FFN is one single, all-purpose consultant every client must see, regardless of their actual question. A Mixture of Experts is instead a large firm with MANY specialist consultants, and a receptionist (the gate) who, for every individual client, quickly determines which `top_k` specialists are actually relevant to THIS client's specific question and routes them there, ignoring every other specialist entirely. The firm as a whole can employ far more specialists (far more total capacity/parameters) than any single client's consultation would ever require (compute per client stays bounded by `top_k`, not by the firm's total size).

### The formula

```
gate_logits = x @ gate_weight^T
top_k_indices, top_k_scores = top_k(gate_logits)
gate_weights = softmax(top_k_scores)

output = sum over i in top_k_indices of gate_weights[i] * Expert_i(x)
```

Only `top_k` of `num_experts` total experts ever run for any given token; every other expert contributes exactly `0` to that token's output.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements MoE gating directly (it lives in model-specific code, e.g. Mixtral's and DeepSeek-MoE's Hugging Face `transformers` implementations), but every real implementation performs essentially this "score all experts, keep top-k, softmax-renormalize, weighted-sum the selected experts' outputs" computation, typically with additional engineering (load-balancing losses to prevent the gate from always routing to the same few experts, and efficient batched dispatch across GPUs, since naively looping per-token as this question does would be far too slow at real scale) outside this question's pedagogical scope. Mixtral 8x7B (`8` experts, `top_k=2`) and DeepSeek-V3 (many more, smaller experts) are two prominent real examples of exactly this architecture choice, at very different points in the "how many experts, how large each" design space.

## Explanation

`moe_gate` computes a raw score for every expert (`x @ gate_weight.T`), uses `np.argsort` to find the indices of the `top_k` HIGHEST-scoring experts per token, gathers just those scores via `np.take_along_axis`, and re-normalizes them with `[03-softmax-last-axis]`'s softmax so the KEPT weights still sum to `1`, entirely independent of how many experts were discarded. `moe_ffn_forward` loops over each token, and for each of that token's `top_k` selected experts, calls `[04-feedforward-sublayer]`'s `feedforward_sublayer` using THAT expert's own independent weights, scaling the result by the gate's corresponding weight before accumulating it into the token's output. Because only the SELECTED experts' weights are ever read for a given token (every other expert's parameters are never touched during that token's computation), a token's output is mathematically completely insulated from whatever the non-selected experts' weights happen to be, the defining structural property that lets MoE models scale total parameter count far beyond what per-token compute would otherwise allow.
