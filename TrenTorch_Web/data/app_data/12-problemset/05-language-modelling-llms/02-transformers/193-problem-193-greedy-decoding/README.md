---
name: problem-193-greedy-decoding
title: 'Greedy Decoding'
tags: [problemset, transformer-llm, generation]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'generation'
hint: 'int(np.argmax(logits))'
tools: [NumPy]
---

## Statement

Choose the next token greedily: the index of the largest logit (probability). On a tie, the smallest index wins.

Implement `solve(logits)`.

**Returns.** Return the index as a Python `int`.

### Examples

**Example 1**

Input:

```python
solve([0.1, 0.7, 0.2])
```

Output:

```text
1
```

**Example 2**

Input:

```python
solve([1.0, 3.0, 3.0])
```

Output:

```text
1
```

## Theory

### The simple version

Greedy decoding writes text by always taking the single most likely next token. It is deterministic and fast, but it can get stuck in repetitive loops and misses sequences that begin with a slightly less likely word but end better.

### The rule

$$\hat y_t=\arg\max_v\;p(v\mid y_{<t})$$

### Why it matters

- Greedy decoding is deterministic and fast, and is the baseline other decoding methods are compared with.
- Softmax is monotonic, so the largest logit is also the most probable token.

### How it works

1. Take the index of the maximum value (the first one on ties).

### Worked example

The largest of $(0.1,0.7,0.2)$ is $0.7$, at index 1.

## Explanation

Because softmax is monotonic, the argmax of the logits equals the argmax of the probabilities, so no softmax is needed. `np.argmax` returns the first maximum, so ties go to the lowest index (second example returns 1).
