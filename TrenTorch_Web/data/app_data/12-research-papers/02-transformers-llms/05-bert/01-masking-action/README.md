---
name: research-bert-masking-action
title: 'BERT: The 80/10/10 Masking Rule'
tags: [research-papers, transformers, llm, pretraining, bert]
difficulty: Beginner
---

## Statement

### The problem, from first principles

BERT (Devlin et al., 2018) pretrains by hiding some input tokens and predicting them. If it always showed a [MASK] token, the model would never see real text at fine-tuning time. So among the selected tokens, most become [MASK], some become random words, and some stay unchanged.

### From theory to code

Implement `masking_action(u)`, which maps a uniform draw to `"mask"`, `"random"` or `"keep"` with probabilities 0.8, 0.1 and 0.1.

### Constraints

- Thresholds: `u < 0.8` is mask, `u < 0.9` is random, otherwise keep.

### Hints

<details>
<summary>Hint 1</summary>

Compare `u` against the two thresholds in order.

</details>

## Theory

### The simple version

The model cannot tell which selected tokens were left alone, so it must keep a good representation of every token. That is why the random and unchanged cases are needed.

### The formula

$$P(\text{mask}) = 0.8,\qquad P(\text{random}) = 0.1,\qquad P(\text{keep}) = 0.1$$

### How NumPy/PyTorch actually implements this

Masked-language-model collators in Hugging Face's libraries implement this 80/10/10 split.

## Explanation

The function is a three-way threshold on a uniform draw. Callers use `np.random.uniform` for `u`, one per selected token.
