---
name: txf-block-swiglu-ffn
title: 'Stretch: SwiGLU-gated FFN'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[04-feedforward-sublayer]`'s "expand, activate, project" FFN applies the SAME activated projection to every hidden unit, with no way for the network to modulate, per-input, HOW MUCH of each hidden unit's signal should actually pass through. Shazeer (2020) proposed a GATED variant, borrowing the "gate" idea from LSTMs/GRUs (`[04-seq-modeling/03-recurrent-neural-networks]`): compute TWO separate linear projections of the input instead of one, pass ONE of them through an activation to act as a per-unit GATE (a soft "how much of this feature matters right now" signal, similar in spirit to an LSTM's forget/input gates), and multiply it elementwise against the OTHER (left un-activated). This gives the sublayer a genuinely richer function class than a plain activated MLP, letting different hidden units get dynamically, INPUT-DEPENDENTLY suppressed or amplified, and LLaMA, PaLM, Mistral and most other modern LLMs adopted this variant specifically because it measurably improves model quality for roughly the same parameter and compute budget as the plain FFN.

"SwiGLU" names the specific choice of gating activation: Swish (`[02-deep-learning-core/02-activations/06-swish]`, also called SiLU) applied to the gate branch, GLU (Gated Linear Unit) naming the elementwise-multiplication-of-two-projections pattern itself.

### From theory to code

Implement `swiglu_ffn(x, weight_gate, weight_up, weight_down)`. Compute TWO separate linear projections of `x` up to `d_ff`, using `weight_gate` and `weight_up` respectively (both WITHOUT a bias term, matching real LLaMA-style implementations, which drop biases from every linear layer). Pass the `weight_gate` projection through `[02-deep-learning-core/02-activations/06-swish]`'s `swish_forward`, multiply it ELEMENTWISE by the (un-activated) `weight_up` projection, then project the result back down to `d_model` with `weight_down` (also bias-free).

### Constraints

- `weight_gate` and `weight_up` are TWO SEPARATE weight matrices, each shape `(d_ff, d_model)`, computing two genuinely different projections of the same input `x`.
- Only the `weight_gate` branch passes through `swish_forward`; the `weight_up` branch stays purely linear.
- The two branches combine via ELEMENTWISE MULTIPLICATION (`gate * up`), not addition, not concatenation.
- No bias terms anywhere: `weight_gate`, `weight_up`, and `weight_down` are all used without an additive bias, matching real modern LLM implementations.

### Hints

<details>
<summary>Hint 1: The two branches</summary>

`gate = swish_forward(linear_forward(x, weight_gate, zero_bias))`, `up = linear_forward(x, weight_up, zero_bias)`, using a zero-filled bias array (shape `(d_ff,)`) since this variant has no biases. Both branches take the SAME input `x`, but use DIFFERENT weight matrices.

</details>

<details>
<summary>Hint 2: Gating and projecting back down</summary>

`hidden = gate * up` (elementwise, both shaped `(..., d_ff)`), then `return linear_forward(hidden, weight_down, zero_bias_d_model)`. Exactly `[04-feedforward-sublayer]`'s overall "expand then project down" shape, just with a gated expansion instead of a single activated one.

</details>

## Theory

### The simple version

`[04-feedforward-sublayer]`'s plain FFN was one person expanding their notes into a detailed draft and applying their own judgment uniformly across the whole draft. SwiGLU is that same person now working with a highlighter in one hand: they produce the SAME detailed draft (the "up" branch, left as-is), but SEPARATELY decide, sentence by sentence, how heavily to weight each part (the "gate" branch, run through Swish to produce a soft 0-to-mostly-1 emphasis value per sentence), then multiply the draft by that emphasis before condensing it into the final summary. The highlighting decision and the draft's actual content come from two INDEPENDENT passes over the same input, not one pass wearing two hats.

### The formula

```
gate = Swish(x @ Wgate^T)          # d_model -> d_ff, gating signal
up   = x @ Wup^T                    # d_model -> d_ff, content signal
hidden = gate * up                  # elementwise gating
output = hidden @ Wdown^T           # d_ff -> d_model
```

No biases anywhere, matching real LLaMA-style implementations. To keep the total parameter count comparable to a plain FFN despite having THREE weight matrices instead of two, real implementations typically shrink `d_ff` (e.g. to roughly `8/3 * d_model` rather than `4 * d_model`) when switching to a gated variant.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements SwiGLU directly (it lives in model-specific code, e.g. Hugging Face `transformers`' LLaMA implementation's `LlamaMLP`), but every real implementation performs exactly these three matrix multiplications and one elementwise product, generally as `self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))`, `F.silu` being PyTorch's name for the Swish/SiLU activation `[02-deep-learning-core/02-activations/06-swish]` implements. `[02-rmsnorm]` and this question are the two changes real LLaMA-style Transformer blocks make relative to `[04-feedforward-sublayer]`'s and `[01-layer-normalization-forward]`'s more "classic" (2017 original Transformer paper) choices, and the two tend to be adopted together in practice.

## Explanation

`swiglu_ffn` computes two independent projections of `x` up to `d_ff`: `gate`, via `weight_gate` and `swish_forward`, and `up`, via `weight_up` with no activation. Multiplying them elementwise (`gate * up`) lets each of the `d_ff` hidden units be dynamically scaled by its own input-dependent gate value (near `0` when Swish saturates low, closer to the raw "up" value when Swish is closer to its unsaturated region), a strictly richer per-position function than `[04-feedforward-sublayer]`'s single activated projection. The gated result is then projected back down to `d_model` via `weight_down`, exactly mirroring `[04-feedforward-sublayer]`'s "expand then project down" shape, just with a gated rather than plain expansion, and with every bias term dropped to match how real LLaMA-style FFNs are actually implemented.
