---
name: problem-200-benchmark-accuracy
title: 'Benchmark Accuracy'
tags: [problemset, transformer-llm, llm-evaluation]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'LLM evaluation'
hint: 'mean of (pred.strip() == target.strip())'
tools: [NumPy]
---

## Statement

Compute exact-match accuracy of model outputs: the fraction of positions where the predicted string equals the expected string after removing leading and trailing whitespace. Pairs are formed with `zip`, so extra items in the longer list are ignored.

Implement `solve(predictions,targets)`.

**Returns.** Return a float in $[0,1]$.

### Examples

**Example 1**

Input:

```python
solve(['cat', 'dog', 'yes'], ['cat', 'cat', 'yes'])
```

Output:

```text
0.666667
```

**Example 2**

Input:

```python
solve([' cat ', 'Dog'], ['cat', 'dog'])
```

Output:

```text
0.5
```

## Theory

### The simple version

For tasks with a single correct answer (a label, a number, a short phrase), the simplest benchmark metric is the share of answers that match the reference exactly. It is strict: "Cat" and "cat" are different, but harmless padding whitespace should not count as a mistake.

### The formula

$$\text{acc}=\frac1N\sum_i\mathbb 1\big[\operatorname{strip}(\hat a_i)=\operatorname{strip}(a_i)\big]$$

### Why it matters

- Exact match is the strictest metric for tasks with a single correct answer.
- Stripping whitespace avoids counting harmless padding as a mistake.

### How it works

1. Strip each prediction and each target.
2. Compare them for equality.
3. Average the matches.

### Worked example

Of the three pairs only `dog` against `cat` differs, so $2/3=0.666667$.

## Explanation

In the second example the padded `' cat '` matches `'cat'` once stripped, but `'Dog'` does not match `'dog'` because the comparison is case-sensitive, so the accuracy is $0.5$. Many benchmarks additionally normalise case and punctuation before comparing.
