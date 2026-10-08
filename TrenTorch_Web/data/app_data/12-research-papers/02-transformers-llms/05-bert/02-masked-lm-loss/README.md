---
name: research-bert-masked-lm-loss
title: 'BERT: The Masked Language Model Loss'
tags: [research-papers, transformers, llm, pretraining, bert]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

BERT's training loss is only computed on the masked positions. Unmasked tokens contribute nothing, so the model learns to recover the hidden words from their context on both sides.

### From theory to code

Implement `masked_lm_loss(log_probs, targets, mask)`, which averages the negative log-probability of the correct token over masked positions.

### Constraints

- Return `0.0` when no position is masked.

### Hints

<details>
<summary>Hint 1</summary>

Index the correct log-probability at each position, negate, then average over the masked entries only.

</details>

## Theory

### The simple version

Averaging over masked positions keeps the loss on a comparable scale regardless of how many tokens were selected in a batch.

### The formula

$$\mathcal{L}_{\text{MLM}} = -\frac{1}{|M|}\sum_{t \in M}\log p(x_t \mid \tilde x)$$

### How NumPy/PyTorch actually implements this

`torch.nn.functional.cross_entropy(..., ignore_index=-100)` implements the same restriction by ignoring unmasked labels.

## Explanation

The mask selects the positions in `M`; the loss is the cross-entropy restricted to those positions.
