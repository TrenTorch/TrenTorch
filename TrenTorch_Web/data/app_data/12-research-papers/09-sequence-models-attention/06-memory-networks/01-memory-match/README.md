---
name: research-memnet-match
title: 'Memory Networks: Matching the Question to Memory'
tags: [research-papers, sequence-models, memory, question-answering]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Memory Networks (Weston et al., 2014) store sentences as memory embeddings. To answer a question, the model scores every memory against the question embedding, then reads the memories that match.

### From theory to code

Implement `memory_match(u, M)`, the dot product of the question with each memory row.

### Constraints

- One score per memory row.

### Hints

<details>
<summary>Hint 1</summary>

Multiply the memory matrix by the question vector.

</details>

## Theory

### The simple version

The match scores decide which stored facts matter for the question. The softmax over these scores is the attention used in the next question.

### The formula

$$p_i = \operatorname{softmax}_i\big(u^\top m_i\big)$$

### How NumPy/PyTorch actually implements this

Memory-network variants compute this matching with one matrix product per hop.

## Explanation

The dot product uses the same embedding space for questions and memories, which the paper trains jointly.
