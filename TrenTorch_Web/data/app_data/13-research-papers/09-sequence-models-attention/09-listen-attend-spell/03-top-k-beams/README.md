---
name: research-las-top-k-beams
title: 'Listen, Attend and Spell: Beam Search Pruning'
tags: [research-papers, sequence-models, speech, attention]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

LAS decodes with beam search, keeping the best few partial transcripts at each step rather than the single best greedy choice. Pruning to the top scores is the step that keeps the search tractable.

### From theory to code

Implement `top_k_beams(scores, k)`, the indices of the k best hypotheses.

### Constraints

- Ties keep the earlier index.

### Hints

<details>
<summary>Hint 1</summary>

Sort the indices by descending score with a stable sort, then keep the first k.

</details>

## Theory

### The simple version

Beam search trades a little compute for better transcripts, since the greedy path can be locally best but globally poor.

### The formula

$$\mathcal{B}_{s+1} = \operatorname{top}_k\{\,h \oplus c : h \in \mathcal{B}_s,\; c \in V\,\}$$

### How NumPy/PyTorch actually implements this

Speech decoders call a top-k selection over expanded hypotheses at every output step.

## Explanation

Stable sorting makes the pruning deterministic when scores tie.
