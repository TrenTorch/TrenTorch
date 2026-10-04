---
name: lm-sft-loss-mask
title: SFT Loss Masking
tags: [fine-tuning, sft, loss-masking]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Supervised fine-tuning shows a pretrained model examples of a prompt followed by a good response and trains it with the ordinary next-token loss. One detail decides what the model actually learns: the loss must be counted **only on the response tokens**. If prompt tokens are counted too, the model spends capacity learning to reproduce questions, and it gets credit for copying text that was handed to it. Padding must be excluded for a different reason, because it carries no information at all. This question builds the mask and the masked loss, including the one-position shift between a token and the position that predicts it.

### From theory to code

Implement `response_mask` and `sft_loss`.

### Constraints

- A batch has `B` sequences padded to length `T`. Sequence `b` has `prompt_lens[b]` prompt tokens followed by response tokens up to `seq_lens[b]`, then padding.
- `response_mask(prompt_lens, seq_lens, T)` returns a `(B, T)` boolean array that is `True` exactly at token positions `t` with `prompt_lens[b] <= t < seq_lens[b]`.
- `logits` has shape `(B, T, V)`: `logits[b, t]` predicts token `t + 1`. `sft_loss(logits, token_ids, prompt_lens, seq_lens)` therefore compares `logits[:, :-1]` with `token_ids[:, 1:]` and the mask `mask[:, 1:]`.
- Return the mean negative log-likelihood over the masked target tokens, using a numerically stable log-softmax.
- Every sequence has at least one response token.

### Hints

<details>
<summary>Hint 1</summary>

`np.arange(T)[None, :]` compared with `prompt_lens[:, None]` and `seq_lens[:, None]` builds the mask with broadcasting.

</details>

<details>
<summary>Hint 2</summary>

Shift first, then mask: target token `t + 1` is scored by the logits at position `t`, and it is the mask of token `t + 1` that decides whether it counts.

</details>

<details>
<summary>Hint 3</summary>

Divide by the number of masked tokens, not by `B * (T - 1)`.

</details>

## Theory

### The simple version

Treat the training text as a script with stage directions. The model should learn the lines it is meant to say and not the cue cards it is shown. The mask is a highlighter: only the highlighted response tokens contribute to the score.

### The formula

With $m_t \in \{0, 1\}$ marking response tokens and $x_t$ the token at position $t$,

$$
\mathcal{L} = -\frac{\sum_{t \ge 1} m_t \,\ln p_\theta(x_t \mid x_{<t})}{\sum_{t \ge 1} m_t}
$$

Because the logits at position $t - 1$ produce the distribution over $x_t$, the mask applies to the shifted target, not to the input position.

### How this is done in practice

Hugging Face collators set prompt labels to `-100`, the value that `torch.nn.functional.cross_entropy(ignore_index=-100)` skips, which is the same idea implemented through labels instead of a separate mask. Frameworks such as TRL expose it as "completion only" loss. Whether to normalise per sequence or per token is a real design choice that changes how long responses are weighted.

## Explanation

The mask is built by comparing each position with the two boundaries. The loss shifts logits and targets by one position, computes a log-softmax with the usual maximum subtraction, picks the log-probability of each true next token and averages only where the shifted mask is true. Prompt tokens and padding therefore never contribute and never receive gradient.
