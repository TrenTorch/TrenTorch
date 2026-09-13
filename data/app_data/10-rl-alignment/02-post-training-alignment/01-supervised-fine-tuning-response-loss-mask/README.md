---
name: rl-alignment-supervised-fine-tuning-response-loss-mask
title: 'Supervised Fine-Tuning: Next-Token Loss, But Only on the Response Tokens'
tags: [reinforcement-learning, nlp, neural-networks]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Raw language-model pretraining trains next-token prediction on every single token in a corpus, with no notion of "the model's own turn" versus "context it was given". Supervised fine-tuning (SFT) — the first step of turning a raw pretrained model into something that follows instructions — reuses the exact same next-token loss, but with one crucial change: the loss is only computed on the tokens the model is actually supposed to have generated, never on the prompt it was handed.

### From theory to code

Implement `make_response_mask` (marking which positions count) and `sft_loss` (the loss, restricted to those positions), reusing `dl-core-cross-entropy-loss`'s per-token cross-entropy directly, plus `raw_pretraining_loss` as the contrasting baseline.

### Constraints

- `make_response_mask(prompt_len, total_len)` returns a length-`total_len` boolean array, `False` for the first `prompt_len` positions and `True` after.
- `sft_loss(logits, targets, prompt_len)` averages the per-token cross-entropy loss ONLY over the response (masked-`True`) positions.
- `raw_pretraining_loss(logits, targets)` is the ordinary mean cross-entropy over every position, with no masking at all.
- Corrupting the prompt-region logits must never change `sft_loss`'s value.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`cross_entropy_forward(logits, targets, reduction="none")` (from `dl-core-cross-entropy-loss`) gives you the loss at every position individually — `sft_loss` is just that array, indexed by the response mask, then averaged.

</details>

<details>
<summary>Hint 2</summary>

`make_response_mask` is one line: start with an all-`False` array of length `total_len`, then set the slice `[prompt_len:]` to `True`.

</details>

## Theory

### The simple version

Imagine grading a student's exam where the first half of the page is the QUESTION (printed by the teacher, not written by the student) and the second half is the student's ANSWER. It would be absurd to grade the student on how well they "predicted" the question text that was already printed for them — you only grade the answer. SFT applies exactly this logic to language model training: the "question" (the prompt) is context the model is given, not something it's being trained to generate, so only the "answer" (the response) counts toward the loss.

### The formula

```text
make_response_mask(prompt_len, total_len)[i] = (i >= prompt_len)

sft_loss(logits, targets, prompt_len) = mean(
    cross_entropy_forward(logits, targets, reduction="none")[make_response_mask(prompt_len, total_len)]
)

raw_pretraining_loss(logits, targets) = mean(cross_entropy_forward(logits, targets, reduction="none"))
```

The two losses use IDENTICAL per-token math — the only difference is which positions get averaged over. This is why SFT is often described as "just pretraining with a different data format and a loss mask" rather than a fundamentally new training objective.

### How PyTorch actually implements this

Context only, untested by your submission: real SFT implementations (Hugging Face's `SFTTrainer`, and most custom training loops) build exactly this kind of `loss_mask` (sometimes called `labels` with prompt positions set to `-100`, PyTorch's `cross_entropy`'s built-in "ignore this index" sentinel) at data-preprocessing time, then let the ordinary `nn.CrossEntropyLoss` skip masked positions automatically — the masking logic this exercise implements by hand is exactly what that sentinel value accomplishes under the hood.

## Explanation

`make_response_mask` builds the boolean mask directly: everything before `prompt_len` is prompt (masked out), everything from `prompt_len` onward is response (kept).

`sft_loss` reuses `dl-core-cross-entropy-loss`'s existing per-token loss computation with `reduction="none"`, then averages only the entries the response mask selects — `tests.py` confirms that corrupting the PROMPT region's logits arbitrarily has zero effect on the result, while corrupting the RESPONSE region's logits (specifically, the logit for the true target class, since a uniform shift across all classes is a softmax no-op) changes it — a real, targeted verification that the masking genuinely restricts which positions matter, not just a shape check.

`raw_pretraining_loss` is the same underlying cross-entropy computation with no masking at all, included specifically so `tests.py` can show the two losses are the same formula applied to different subsets, and that the SFT loss reduces to exactly the pretraining loss in the degenerate case of an empty prompt (`prompt_len=0`).
