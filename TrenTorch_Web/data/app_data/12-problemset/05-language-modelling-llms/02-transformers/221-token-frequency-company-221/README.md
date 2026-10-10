---
name: token-frequency-company-221
title: 'token-frequency — LinkedIn case'
tags: [problemset, transformer-llm, tokenization-for-llms, linkedin]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'LinkedIn'
hint: 'dict(Counter(tokens))'
---

## Statement

LinkedIn-inspired text analytics service is building a lightweight vocabulary report from a batch of documents. You need to count token occurrences consistently so the team can identify the most frequent terms for the next modeling stage.

Count how many times each token occurs and return the counts as a dict. Keys appear in order of first occurrence.

Implement `solve(tokens)`.

**Returns.** Return a dict `{token: count}`; an empty list gives an empty dict.

Count how many times each token occurs and return the counts as a dict. Keys appear in order of first occurrence.

Implement `solve(tokens)`.

**Returns.** Return a dict `{token: count}`; an empty list gives an empty dict.

### Examples

**Example 1**

Input:

```python
solve([2, 1, 2, 3, 2, 1])
```

Output:

```text
{2: 3, 1: 2, 3: 1}
```

**Example 2**

Input:

```python
solve(['a', 'b', 'a'])
```

Output:

```text
{'a': 2, 'b': 1}
```

## Theory

### The simple version

The first step of building a vocabulary report is counting. Frequent tokens deserve their own entries; rare ones may be merged into an _unknown_ bucket or split into smaller pieces. Token frequencies in natural text follow a long-tailed (Zipf) distribution.

### The definition

$$\text{count}(t)=\#\{i:\;\text{tokens}_i=t\}$$

### Why it matters

- Token frequencies are the first step of building a vocabulary and show the long-tailed (Zipf) shape of text.
- Counting once, in a single pass, keeps the cost proportional to the data size.

### How it works

1. Walk through the tokens once.
2. Increase the count of each token in a dictionary.
3. Return the dictionary (keys in order of first appearance).

### Worked example

In $(2,1,2,3,2,1)$ the token $2$ appears three times, $1$ twice and $3$ once, so the counts are {2: 3, 1: 2, 3: 1}.

## Explanation

`collections.Counter` does a single pass in time proportional to the number of tokens. Any hashable token works: integers (first example) or strings (second).
