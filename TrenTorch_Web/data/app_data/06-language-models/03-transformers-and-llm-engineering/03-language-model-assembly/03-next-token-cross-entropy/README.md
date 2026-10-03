---
name: txf-lm-next-token-cross-entropy
title: 'Next-token Cross-Entropy loss (reuses Part 1 loss)'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-output-projection]`'s logits give a score for every vocabulary word, at EVERY position in the sequence. Training a language model means adjusting its weights so that position `t`'s logits ASSIGN HIGH PROBABILITY to whatever token actually occurs at position `t + 1`, exactly the "predict the next token" framing that gives autoregressive language models their name. `[02-deep-learning-core/03-losses/02-cross-entropy]`'s `cross_entropy_forward` already implements the general "penalize low probability assigned to the correct class" loss; the only new work here is correctly SHIFTING logits and targets by one position before handing them to that already-built function.

### From theory to code

Implement `next_token_cross_entropy_loss(logits, token_ids)`: logits at positions `0` through `seq_len - 2` predict targets at positions `1` through `seq_len - 1` (`token_ids` shifted forward by one), flattened and passed to `[02-cross-entropy]`'s `cross_entropy_forward`.

### Constraints

- Position `t`'s logits are compared against `token_ids[t + 1]`, the token that ACTUALLY comes next, never `token_ids[t]` itself.
- The LAST position's logits have no "next token" to predict (there's nothing after the end of the sequence) and must be EXCLUDED, leaving `seq_len - 1` valid (prediction, target) pairs from a length-`seq_len` sequence.
- Any leading batch dimensions are flattened together with the sequence dimension before calling `cross_entropy_forward` (which expects a flat `(n, vocab_size)`/`(n,)` pair).

### Hints

<details>
<summary>Hint 1: The shift</summary>

`predicted_logits = logits[..., :-1, :]` (drop the LAST position, it has no target), `targets = token_ids[..., 1:]` (drop the FIRST position, it has no preceding prediction). Both now have length `seq_len - 1` along the sequence axis, correctly aligned: `predicted_logits[..., t, :]` pairs with `targets[..., t]`.

</details>

<details>
<summary>Hint 2: Flattening and calling cross_entropy_forward</summary>

```python
vocab_size = predicted_logits.shape[-1]
flat_logits = predicted_logits.reshape(-1, vocab_size)
flat_targets = targets.reshape(-1)
return cross_entropy_forward(flat_logits, flat_targets)
```

</details>

## Theory

### The simple version

Reading a sentence one word at a time and, at every word, being asked to GUESS the next word before actually seeing it, then getting graded on how much probability the guess assigned to whatever word turns out to be correct. The grading itself (cross-entropy, "how surprised was the guesser by the true answer") is identical at every position, exactly `[02-cross-entropy]`'s existing loss; the only new idea here is that the "correct answer" being graded against is always ONE WORD AHEAD of wherever the guess was made.

### The formula

```
predicted_logits = logits[:-1]      # positions 0 .. seq_len-2
targets          = token_ids[1:]     # positions 1 .. seq_len-1
loss = CrossEntropy(predicted_logits, targets)
```

A length-`seq_len` sequence produces exactly `seq_len - 1` (prediction, target) pairs: there's no "next token" to grade the very last position's prediction against.

### How PyTorch actually implements this

`torch.nn.functional.cross_entropy(logits[..., :-1, :].reshape(-1, vocab_size), token_ids[..., 1:].reshape(-1))` is essentially the exact PyTorch equivalent of this question's implementation, the standard training loss for virtually every decoder-only language model. Real implementations occasionally compute the shift slightly differently (shifting the LABELS by convention rather than the logits, mathematically equivalent), but the underlying computation, and the resulting loss VALUE, is identical either way. `[05-training-loop]`, later in this track, uses this exact function as the loss being minimized at every training step.

## Explanation

`next_token_cross_entropy_loss` drops the last position from `logits` (`logits[..., :-1, :]`, since it has no next token to be graded against) and the first position from `token_ids` (`token_ids[..., 1:]`, since it has no preceding position that predicted it), leaving two correctly-aligned arrays of length `seq_len - 1`: `predicted_logits[..., t, :]` is now the model's guess about what comes right after position `t`, and `targets[..., t]` is what ACTUALLY comes right after position `t`. Both are flattened (merging any leading batch dimension together with the shifted sequence dimension) into the flat `(n, vocab_size)`/`(n,)` shape `[02-cross-entropy]`'s `cross_entropy_forward` expects, which then computes the ordinary cross-entropy loss over every one of these `n` next-token predictions at once.
