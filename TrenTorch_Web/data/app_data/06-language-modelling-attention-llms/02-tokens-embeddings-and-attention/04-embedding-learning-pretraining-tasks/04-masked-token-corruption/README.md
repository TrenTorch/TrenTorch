---
name: lm-masked-token-corruption
title: Masked-Token Corruption
tags: [pretraining, bert, masked-lm]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

BERT learns language by a fill-in-the-blank game. Some tokens are hidden and the model must recover them using context from _both_ sides. The corruption recipe has a subtle design. About 15% of the (non-special) tokens are chosen as targets. A chosen token is replaced by the `[MASK]` token only **80%** of the time, by a **random** token 10% of the time and left **unchanged** 10% of the time. Why not always mask? Because `[MASK]` never appears in real text at fine-tuning time. Sometimes seeing a random or unchanged token forces the model to keep a good representation of _every_ token, since any token might be a target. The labels are the original ids at chosen positions and an ignore value everywhere else.

### From theory to code

Implement `mask_tokens`.

### Constraints

- `ids` is a 1-D integer array. `special_ids` is a set of ids that may never be chosen. `rng` is a `np.random.RandomState`. Draw random numbers in exactly this order: (1) `u = rng.random_sample(len(ids))`; a position is **chosen** iff `u < mask_prob` and its id is not special. (2) `r = rng.random_sample(num_chosen)` for the chosen positions in increasing order. (3) `rand_tokens = rng.randint(0, vocab_size, size=num_chosen)`.
- For chosen position number `m`: if `r[m] < 0.8` the input becomes `mask_id`; elif `r[m] < 0.9` it becomes `rand_tokens[m]`; else it is unchanged.
- Return `(inputs, labels)`: `inputs` is a corrupted copy of `ids`, and `labels` equals the original id at chosen positions and `-100` elsewhere.

### Hints

<details>
<summary>Hint 1</summary>

Compute all three random draws even when no position is chosen, in the stated order, so streams stay aligned.

</details>

<details>
<summary>Hint 2</summary>

Boolean indexing with the chosen mask gives the chosen positions in increasing order.

</details>

## Theory

### The simple version

A teacher blanks out words on a worksheet. Occasionally they swap a word for a wrong one without telling you, or leave a word that is graded anyway, so you cannot simply skip the words that look normal.

### The formula

$$
x'_t = \begin{cases} [\text{MASK}] & t \in T,\; r_t < 0.8\\ \text{random token} & t \in T,\; 0.8 \le r_t < 0.9 \\ x_t & \text{otherwise}\end{cases}
$$

Only positions in $T$ contribute to the loss: $\mathcal{L} = -\sum_{t\in T}\ln p(x_t \mid x')$.

### How this is done in practice

Hugging Face's `DataCollatorForLanguageModeling` implements this, with `-100` as the label that `cross_entropy` ignores. Later work (RoBERTa) re-samples the mask every epoch (dynamic masking), and some models mask whole words or spans.

## Explanation

The statistical behaviour (about 15% chosen, about 80/10/10 of those) is tested with a large sample, and the exact corruption is tested by replaying the stated random-number order.
