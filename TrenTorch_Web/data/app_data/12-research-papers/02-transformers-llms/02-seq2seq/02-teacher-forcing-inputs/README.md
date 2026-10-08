---
name: research-seq2seq-teacher-forcing
title: 'Seq2seq: Teacher-Forced Decoder Inputs'
tags: [research-papers, transformers, llm, seq2seq]
difficulty: Beginner
---

## Statement

### The problem, from first principles

During training the decoder is fed the correct previous word, not its own guess. This is teacher forcing. The inputs are the targets shifted right by one position, with a begin-of-sentence token at the front.

### From theory to code

Implement `decoder_inputs(targets, bos)`, which returns `[bos] + targets[:-1]`.

### Constraints

- The last target token is never an input.

### Hints

<details>
<summary>Hint 1</summary>

Concatenate the start token with all targets except the final one.

</details>

## Theory

### The simple version

At each step the decoder predicts the next target from all previous ones. Shifting the targets gives it exactly the context it would have at inference, minus the errors it would have made.

### The formula

$$\text{input}_t = \begin{cases} \text{bos} & t = 1 \\ y_{t-1} & t > 1 \end{cases}$$

### How NumPy/PyTorch actually implements this

Machine translation code builds the decoder input with `torch.cat([bos, targets[:, :-1]], dim=1)`.

## Explanation

The shift lets one forward pass compute every next-token prediction in parallel during training.
