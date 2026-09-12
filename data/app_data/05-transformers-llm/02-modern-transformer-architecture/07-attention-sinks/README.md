---
name: txf-modern-attention-sinks
title: 'Note: attention sinks, why the first few tokens matter disproportionately'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[05-sliding-window-attention]`'s fixed window solves the compute problem cleanly, but Xiao et al. (2023, "StreamingLLM") discovered an unexpected practical failure when actually deploying it: once the FIRST few tokens of a sequence slide OUTSIDE the window (as later positions push them out of range), model quality often collapses sharply, even though those tokens' actual CONTENT rarely mattered semantically. Digging into WHY revealed something specific to how softmax works: softmax weights are required to sum to exactly `1` even when there's genuinely nowhere useful to "put" the leftover weight (a query with no strongly relevant key still has to distribute its probability mass somewhere), and empirically, models learn to dump this leftover weight onto whatever's EARLIEST and always-available, the first few tokens, turning them into a kind of attention "sink" regardless of what they actually contain. Removing those tokens from view doesn't just lose a little context, it breaks the mechanism the model was implicitly relying on to keep its softmax outputs well-behaved.

The practical fix requires no retraining: keep a small, fixed number of "sink" tokens (often just `1`-`4`) PERMANENTLY visible, in addition to `[05-sliding-window-attention]`'s ordinary sliding window, regardless of how far the sequence has moved on since. This lets a long-running generation stream stay bounded in memory (like ordinary sliding-window attention) while avoiding the quality collapse that dropping the very first tokens would otherwise cause.

### From theory to code

Implement `attention_sink_mask(seq_len, window_size, num_sink_tokens)`: `[05-sliding-window-attention]`'s bounded-window mask, but with the first `num_sink_tokens` positions marked as ALWAYS visible (subject only to ordinary causality), regardless of whether they'd otherwise fall outside the window.

### Constraints

- A position within `num_sink_tokens` of the start is visible to any LATER query (`j < num_sink_tokens` and `j <= i` implies visible), no matter how far outside the sliding window it would otherwise be.
- Causality still applies EVEN to sink tokens: a sink token in the FUTURE relative to the query (`j > i`) remains masked, exactly like every other position.
- Every position OUTSIDE both the sink range and the sliding window remains masked, unchanged from `[05-sliding-window-attention]`'s behavior.
- `num_sink_tokens=0` must reduce EXACTLY to `[05-sliding-window-attention]`'s ordinary sliding-window mask.

### Hints

<details>
<summary>Hint 1: Start from the sliding-window mask</summary>

`window_mask = build_sliding_window_mask(seq_len, window_size)` (from `[05-sliding-window-attention]`), then OVERRIDE specific entries to be visible, rather than building the whole mask from scratch.

</details>

<details>
<summary>Hint 2: Which entries to override</summary>

```python
positions = np.arange(seq_len)
is_causally_visible = positions[None, :] <= positions[:, None]  # j <= i
is_sink_token = positions[None, :] < num_sink_tokens             # j < num_sink_tokens
always_visible = is_sink_token & is_causally_visible
```

`always_visible[i, j]` is `True` exactly where a sink token should override the window's normal restriction.

</details>

<details>
<summary>Hint 3: Combining the two</summary>

`return np.where(always_visible, 0.0, window_mask)`: wherever `always_visible` is `True`, force the mask entry to `0.0` (visible); everywhere else, keep whatever `[05-sliding-window-attention]`'s ordinary window mask already computed.

</details>

## Theory

### The simple version

`[05-sliding-window-attention]`'s reader, working from only a small stack of the last few pages, discarding everything older. Attention sinks are that same reader deliberately keeping a small INDEX CARD from the very first page pinned to their desk at all times, even as every other early page gets discarded: not because that first page's specific content matters most, but because having SOMETHING stable and always-available to refer back to turns out to be structurally necessary for the reader's own note-taking process to stay well-behaved, regardless of what's actually written on that card.

### The formula

```
sink_visible(i, j) = (j < num_sink_tokens) AND (j <= i)
mask(i, j) = 0     if sink_visible(i, j) OR sliding_window_allows(i, j)
           = -inf   otherwise
```

The sliding window's own bound (`i - j < window_size`) and the sink override are combined with a logical OR: a position is visible if EITHER condition permits it.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements attention sinks directly (an inference-time serving technique, not a training-time architectural component), but production long-context serving systems (the original StreamingLLM implementation, and several inference frameworks since) implement exactly this "keep a small fixed prefix plus a sliding window" cache-eviction policy when running a model on a stream far longer than anything it saw during training. `[05-sliding-window-attention]`'s question already established the compute-saving mechanism; this question's entire contribution is the SPECIFIC, empirically-discovered exception (never evict the first few tokens) needed to make that mechanism actually work well in practice, over arbitrarily long streaming generation.

## Explanation

`attention_sink_mask` starts from `[05-sliding-window-attention]`'s ordinary sliding-window mask, then computes an `always_visible` boolean array marking exactly the entries where a position is BOTH a sink token (`j < num_sink_tokens`) AND causally valid (`j <= i`). `np.where(always_visible, 0.0, window_mask)` overrides those specific entries to `0.0` (fully visible) while leaving every other entry exactly as `[05-sliding-window-attention]`'s window mask already computed it, correctly preserving both the ordinary window's bound for non-sink positions and strict causality (a sink token still in the query's FUTURE stays masked, since `is_causally_visible` remains `False` there regardless of `is_sink_token`).
