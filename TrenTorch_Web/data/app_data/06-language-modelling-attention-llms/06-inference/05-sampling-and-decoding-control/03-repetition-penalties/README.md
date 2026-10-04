---
name: lm-repetition-penalties
title: Repetition, Frequency & Presence Penalties
tags: [decoding, sampling, penalties]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Language models love to loop: once a phrase appears, its tokens become more likely to appear again, and greedy or low-temperature decoding can repeat the same sentence forever. Decoding libraries fight this by editing the logits of tokens that have already been generated. Three common rules exist. The **repetition penalty** (from the CTRL paper) divides the logit of a seen token by a factor when it is positive and multiplies it when it is negative, so the token always becomes less likely. The **frequency penalty** subtracts an amount proportional to how many times the token has appeared, and the **presence penalty** subtracts a flat amount once if it has appeared at all.

### From theory to code

Implement `apply_penalties`.

### Constraints

- `logits` is a 1-D float array over the vocabulary and `generated_ids` is a list of the token ids produced so far.
- First apply the repetition penalty `rep > 0` to every distinct generated token: a positive logit becomes `logit / rep`, a negative logit becomes `logit * rep` (`rep = 1.0` changes nothing).
- Then, for every token with count `c > 0`, subtract `freq * c + pres`.
- Tokens never generated are untouched. Return a new array and do not modify `logits`.

### Hints

<details>
<summary>Hint 1</summary>

`np.bincount(generated_ids, minlength=len(logits))` gives all counts at once.

</details>

<details>
<summary>Hint 2</summary>

Apply the repetition rule before the subtractive penalties, and only where the count is positive.

</details>

## Theory

### The simple version

A conversation partner who keeps repeating a favourite word gets a gentle nudge each time they use it: a flat nudge for ever having used it (presence), a growing nudge for each repeat (frequency) and a rule that makes the word less attractive however you score it (repetition).

### The formula

$$
z_i' = \begin{cases}
z_i / \theta & z_i > 0,\; c_i > 0\\
z_i \cdot \theta & z_i \le 0,\; c_i > 0\\
z_i & c_i = 0
\end{cases}
\qquad z_i'' = z_i' - \alpha_f\,c_i - \alpha_p\,\mathbf{1}[c_i > 0]
$$

### How this is done in practice

Hugging Face's `RepetitionPenaltyLogitsProcessor` implements the first rule and OpenAI-style APIs expose the other two as `frequency_penalty` and `presence_penalty`. Penalizing too strongly damages legitimate repetition such as names, code and numbers, so values are kept small.

## Explanation

The repetition rule treats the sign carefully so that a penalty always reduces probability. The count array turns the per-token frequency logic into a vectorized subtraction.
