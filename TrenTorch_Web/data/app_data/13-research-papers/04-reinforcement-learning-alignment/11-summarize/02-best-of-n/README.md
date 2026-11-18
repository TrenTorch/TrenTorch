---
name: research-summarize-best-of-n
title: 'Learning to Summarize: Best-of-N Selection'
tags: [research-papers, reinforcement-learning, alignment, rlhf, summarization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Best-of-N sampling draws several candidate summaries from the model, scores them with the reward model, and returns the best. It is a simple way to use a reward model at inference time and a baseline that the paper compares against.

### From theory to code

Implement `best_of_n_index(scores)`, returning the index of the candidate with the highest reward.

### Constraints

- Return a Python `int`.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.argmax` on the scores.

</details>

## Theory

### The simple version

Selecting the best of N trades extra sampling cost for quality, and the reward model decides what counts as best.

### The formula

$$\hat y = \arg\max_{i \in \{1,\ldots,N\}} r_\phi(x, y_i)$$

### How NumPy/PyTorch actually implements this

Sampling-and-reranking pipelines call `argmax` over reward scores in exactly this way.

## Explanation

The argmax is the same operation as greedy decoding, applied to whole candidates instead of tokens.
