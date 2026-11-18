---
name: research-seq2seq-reverse-source
title: 'Seq2seq: Reversing the Source Sentence'
tags: [research-papers, transformers, llm, seq2seq]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Sutskever et al. (2014) found that reversing the source sentence makes learning easier, because the first words of the input end up close to the first words of the output. Only the input is reversed; the target is left alone.

### From theory to code

Implement `reverse_source(tokens)`, which returns the tokens in reverse order as a new list.

### Constraints

- The input may be a list or a tuple.

### Hints

<details>
<summary>Hint 1</summary>

Slice with a step of `-1`, after converting to a list.

</details>

## Theory

### The simple version

Reversal changes no information, but it shortens the distance between corresponding source and target words, which gives gradients an easier path during training.

### The formula

$$\text{src} = (w_1, \ldots, w_T) \;\longrightarrow\; (w_T, \ldots, w_1)$$

### How NumPy/PyTorch actually implements this

Preprocessing in translation pipelines performs exactly this step on the source side before batching.

## Explanation

The reversed source is fed to the encoder as ordinary input; the decoder and target are unchanged.
