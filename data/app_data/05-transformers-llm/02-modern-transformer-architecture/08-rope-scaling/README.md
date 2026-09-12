---
name: txf-modern-rope-scaling
title: 'RoPE scaling: extending a model past its trained context length'
tags: [transformers]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[04-seq-modeling/02-embeddings/06-rope]`'s RoPE encodes position as a ROTATION angle, growing linearly with position index. A model trained ONLY on sequences up to some `trained_max_len` never sees rotation angles beyond whatever that length produces; when run on a LONGER sequence at inference time, positions past `trained_max_len` produce rotation angles the model's learned weights have simply never encountered during training, and quality typically degrades sharply, exactly the practical problem this question's title names.

Chen et al. (2023, "Position Interpolation") proposed a strikingly simple, training-free (or cheap-to-fine-tune) fix: instead of letting positions run up to the new, longer `target_max_len` directly, COMPRESS them first, dividing every position by `scale_factor = target_max_len / trained_max_len` before computing RoPE's angles. The position at the very end of the EXTENDED sequence then produces the exact SAME angle the position at the very end of the ORIGINAL trained range used to produce, so every angle the model now encounters falls back WITHIN the range it was actually trained on, even though the sequence itself is now much longer. The tradeoff: positions are now more densely packed into that same angular range (less angular separation between adjacent tokens than during training), which is why Position Interpolation-style scaling often benefits from a short period of further fine-tuning at the new length, even though it can work reasonably well with NO fine-tuning at all.

### From theory to code

Implement `compute_rope_angles_scaled(seq_len, dim, scale_factor)`: `[06-rope]`'s `compute_rope_angles`, with every position divided by `scale_factor` before the angle computation.

### Constraints

- `scale_factor=1.0` must reduce EXACTLY to `[06-rope]`'s unscaled `compute_rope_angles`.
- Positions are DIVIDED by `scale_factor` (compressing the range), never multiplied (which would do the opposite, expanding it).
- The per-dimension frequency formula (`10000^(-2i/dim)`) is unchanged from `[06-rope]`; only the POSITION fed into it is scaled.
- The relative-position dot-product invariance property `[06-rope]` established must still hold after scaling: two pairs of vectors with the same relative offset must still produce the same dot product, regardless of their absolute positions.

### Hints

<details>
<summary>Hint 1: The one-line change</summary>

`position = np.arange(seq_len)[:, None] / scale_factor` (compare directly against `[06-rope]`'s `position = np.arange(seq_len)[:, None]`), then compute `freq` and the final `position * freq` exactly as `[06-rope]`'s `compute_rope_angles` already does.

</details>

<details>
<summary>Hint 2: Choosing scale_factor</summary>

`scale_factor = target_max_len / trained_max_len` is the standard choice: it guarantees position `target_max_len` (the far end of the new, extended range) maps EXACTLY onto position `trained_max_len` (the far end of the range the model actually trained on).

</details>

## Theory

### The simple version

A ruler the model was trained to read ONLY up to the `100`cm mark. Position Interpolation doesn't extend the ruler; it takes a longer, `400`cm measurement and COMPRESSES it, remarking every `4`cm as `1`cm, so the whole extended measurement now fits back onto the original, familiar `100`cm ruler the model already knows how to read, at the cost of each of the ruler's original centimeter-marks now standing for `4` real centimeters instead of `1` (a real loss of fine-grained positional resolution, which is exactly why some further fine-tuning at the new scale often helps).

### The formula

```
scale_factor = target_max_len / trained_max_len
scaled_position = position / scale_factor
angle(position, dim_pair_i) = scaled_position * 10000^(-2i/dim)
```

Compare directly against `[06-rope]`'s unscaled `angle(position, dim_pair_i) = position * 10000^(-2i/dim)`: identical formula, just with `position` replaced by `position / scale_factor`.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements RoPE scaling directly (like RoPE itself, it lives in model-specific extrapolation code), but Hugging Face `transformers`' `rope_scaling` configuration option on LLaMA and similar models implements essentially this formula (`"type": "linear"`, i.e. Position Interpolation) as one of several supported scaling strategies; `"type": "dynamic"` (NTK-aware scaling) is a more sophisticated variant that scales different RoPE FREQUENCIES by different amounts rather than uniformly compressing every position, preserving more resolution for nearby tokens at the cost of a more involved derivation. `[04-seq-modeling/02-embeddings/06-rope]`'s original relative-position dot-product invariance property (verified directly in this question's own tests) is exactly what makes any UNIFORM rescaling of position, this linear scheme included, mathematically safe: scaling every position by the same constant preserves every RELATIVE offset's proportional relationship to every other, so the model's learned understanding of "how far apart are these two tokens" degrades gracefully rather than breaking outright.

## Explanation

`compute_rope_angles_scaled` divides every raw position index by `scale_factor` before computing angles, otherwise reusing `[06-rope]`'s exact frequency formula unchanged. With `scale_factor = target_max_len / trained_max_len`, the LARGEST position in the extended sequence (`target_max_len`) divides down to EXACTLY `trained_max_len`, the largest position the model actually trained on, so every angle the model encounters at inference time, however long the input sequence has grown, falls within the same range of angles it already learned to interpret during training. Because the scaling is a single UNIFORM constant applied to every position alike, the relative-offset-only dot-product invariance `[06-rope]` originally established survives entirely intact: two pairs of positions separated by the same (now uniformly-compressed) relative distance still produce identical dot products, regardless of where in the (extended) sequence that pair happens to sit.
