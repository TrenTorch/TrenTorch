---
name: txf-llmeng-speculative-decoding
title: 'Speculative decoding: draft-and-verify loop, accept/reject against a larger model'
tags: [transformers, nlp]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[03-language-model-assembly/07-greedy-decoding]`'s generation loop runs one FULL forward pass through the model for every SINGLE new token, an inherent bottleneck: a large model is expensive to run, and generating `100` tokens means paying that expense `100` separate times, sequentially, with no way to parallelize across steps (each step genuinely needs the previous step's output before it can even start). Speculative decoding (Leviathan et al. 2023, Chen et al. 2023) sidesteps this with a clever trick: use a much SMALLER, cheaper "draft" model to quickly propose SEVERAL tokens ahead, then run the large "target" model just ONCE, in parallel, to check ALL of those proposed tokens at once (a single forward pass over the whole draft sequence is exactly as expensive as one ordinary step, since a Transformer processes every position in a sequence simultaneously anyway).

The verification rule is what keeps this mathematically sound: a proposed token is ACCEPTED only if the target model's own greedy choice, at that exact position, agrees with what the draft proposed. The moment they disagree, the draft is wrong from that point on (the target's own choice there is used as the correction), and everything the draft speculated AFTER that point is discarded, since it was built on a now-abandoned assumption. When the draft and target happen to agree often (a good, well-matched draft model), MULTIPLE tokens get accepted from a SINGLE expensive target forward pass, real, measurable speedup, and critically, the FINAL output is always exactly what the target model's own greedy decoding would have produced on its own, speculative decoding changes nothing about WHAT gets generated, only how efficiently it gets generated.

### From theory to code

Implement `speculative_decode_step(token_ids, <draft model args>, <target model args>, num_draft_tokens)`: draft `num_draft_tokens` tokens greedily with the draft model (`[07-greedy-decoding]`), verify them all in ONE target-model forward pass, and accept the longest PREFIX of agreement, correcting the first disagreement (if any) to the target's own choice.

### Constraints

- The draft model's proposals come from `[07-greedy-decoding]`'s `greedy_decode`, run for exactly `num_draft_tokens` steps.
- The target model runs EXACTLY ONCE, on the ENTIRE drafted sequence at once (never once per drafted token), via `[04-full-forward-pass]`'s `full_lm_forward` with a causal mask.
- Acceptance is checked IN ORDER, starting from the first drafted token: a token is accepted only if the target's own `argmax` at that position matches the draft's proposal there, and checking STOPS at the first disagreement.
- The first disagreement is corrected to the TARGET's own choice (never the draft's rejected proposal), and nothing after it is included in the result.
- If every drafted token is accepted, the result is identical to running the TARGET model's own `greedy_decode` directly for `num_draft_tokens` steps.

### Hints

<details>
<summary>Hint 1: Drafting and verifying</summary>

```python
draft_sequence = greedy_decode(token_ids, ...draft args..., num_draft_tokens)
mask = build_causal_mask(draft_sequence.shape[-1])
target_logits = full_lm_forward(draft_sequence, ...target args..., mask=mask)
```

`target_logits[0, seq_len - 1 + i, :]`'s `argmax` is the target model's own prediction for what should come at position `seq_len + i`, exactly the position the draft's `i`-th proposed token occupies.

</details>

<details>
<summary>Hint 2: The accept/reject loop</summary>

```python
accepted = draft_sequence[:, :seq_len]
for i in range(num_draft_tokens):
    draft_token = draft_sequence[0, seq_len + i]
    target_prediction = np.argmax(target_logits[0, seq_len - 1 + i, :])
    if draft_token == target_prediction:
        accepted = concat(accepted, draft_token); num_accepted += 1
    else:
        accepted = concat(accepted, target_prediction); break   # correct and stop
```

</details>

## Theory

### The simple version

A busy executive (the target model, expensive to consult) working with a fast junior assistant (the draft model, cheap to consult). Instead of asking the executive one question at a time, waiting for each answer before asking the next, the assistant quickly drafts several proposed answers in a row, in advance, based on their own (cheaper, less reliable) judgment. The executive then reviews the WHOLE batch of drafted answers in one single pass, confirming whichever prefix they genuinely agree with, and correcting the very first place they'd have answered differently, discarding everything the assistant speculated beyond that point (since it was built on an assumption the executive just overturned).

### The formula

```
draft_sequence = GreedyDecode(DraftModel, token_ids, num_draft_tokens)
target_logits = TargetModel(draft_sequence)     # ONE forward pass, verifies all proposals at once

for i in 0 .. num_draft_tokens - 1:
    if draft_sequence[seq_len + i] == argmax(target_logits[seq_len - 1 + i]):
        accept it
    else:
        replace it with argmax(target_logits[seq_len - 1 + i]), then STOP
```

### How PyTorch actually implements this

`model.generate(input_ids, assistant_model=draft_model)` in Hugging Face `transformers` implements exactly this pattern (`assistant_model` is the draft), with additional production refinements this question omits (a probabilistic accept/reject rule for SAMPLING-based generation rather than pure greedy, which requires a more involved rejection-sampling scheme to remain provably equivalent to sampling from the target model alone). The core insight (verify many candidates in ONE parallel forward pass, since a Transformer processes a whole sequence's positions simultaneously regardless of length) is exactly why speculative decoding provides a genuine wall-clock speedup without changing the model's actual output distribution: the EXPENSIVE model still determines every single accepted token, it's just being asked to check several candidates per invocation instead of generating exactly one.

## Explanation

`speculative_decode_step` first calls `[07-greedy-decoding]`'s `greedy_decode` with the CHEAP draft model to propose `num_draft_tokens` tokens, then runs the EXPENSIVE target model exactly ONCE, via `[04-full-forward-pass]`'s `full_lm_forward` with a causal mask, over the entire drafted sequence at once, a single parallel forward pass that produces the target's own prediction at every drafted position simultaneously. The accept/reject loop then walks through the drafted tokens IN ORDER, comparing each one against the target's own `argmax` at that exact position: as long as they agree, the drafted token is accepted and the loop continues; at the first disagreement, the target's own choice replaces the rejected draft proposal, and the loop stops immediately, since everything the draft speculated beyond a disagreement was built on an assumption the target has just overturned. When draft and target always agree (the identical-models test case), every proposed token gets accepted, and the result is bit-identical to what `[07-greedy-decoding]`'s `greedy_decode` would have produced running the target model alone, the property that makes speculative decoding a pure EFFICIENCY optimization rather than a change in what actually gets generated.
