---
name: research-gpt3-continuation-logprob
title: 'GPT-3: Scoring a Continuation'
tags: [research-papers, transformers, llm, llm, prompting]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

GPT-3 ranks candidate answers by how likely the model finds each one as a continuation of the prompt. The score is the sum of the log-probabilities of the continuation tokens, given everything before them.

### From theory to code

Implement `continuation_logprob(log_probs, tokens, start)`, which sums the log-probability of each token from `start` onward.

### Constraints

- Only continuation tokens are scored; the prompt contributes nothing.

### Hints

<details>
<summary>Hint 1</summary>

Loop from `start` to the end, pick each token's log-probability from its row, and sum.

</details>

## Theory

### The simple version

Summing log-probabilities multiplies the probabilities of the tokens, so this is the log of the probability the model gives the whole continuation.

### The formula

$$\log p(y \mid x) = \sum_{t=\text{start}}^{T-1} \log p(\text{tok}_t \mid \text{tok}_{<t})$$

### How NumPy/PyTorch actually implements this

Evaluation harnesses compute this with a single forward pass and a gather over the continuation positions.

## Explanation

Prompt tokens are conditioning only, so their probabilities are excluded from the sum.
