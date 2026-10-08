---
name: research-bert-input-embedding
title: 'BERT: Summing Token, Segment and Position Embeddings'
tags: [research-papers, transformers, llm, pretraining, bert]
difficulty: Beginner
---

## Statement

### The problem, from first principles

BERT's input must tell the model three things at once: which word it is, which sentence segment it belongs to, and where it sits in the sequence. The paper gives each its own learned table, and the three vectors are added together.

### From theory to code

Implement `bert_input_embedding`, which looks up token, segment and position vectors and returns their element-wise sum for each position.

### Constraints

- Use the first `T` rows of the position table.

### Hints

<details>
<summary>Hint 1</summary>

Index each table with the matching ids, slice the position table to length `T`, and add the three arrays.

</details>

## Theory

### The simple version

Adding instead of concatenating keeps the model width fixed, and the network learns to separate the three signals inside the same vector.

### The formula

$$e_t = E_{\text{tok}}[x_t] + E_{\text{seg}}[s_t] + E_{\text{pos}}[t]$$

### How NumPy/PyTorch actually implements this

`torch.nn.Embedding` tables used three times and added, the standard BERT-style input block.

## Explanation

This is a sum of three lookups: a single matrix row per token, segment and position, then broadcast over the sequence.
