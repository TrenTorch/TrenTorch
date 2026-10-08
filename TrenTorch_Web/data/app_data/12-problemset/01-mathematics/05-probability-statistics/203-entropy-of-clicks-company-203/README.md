---
name: entropy-of-clicks-company-203
title: 'entropy-of-clicks — Google case'
tags: [problemset, maths-stats-for-ml, information-theory, google]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Google'
hint: 'drop zeros, then minus the sum of p*log2(p)'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Google** ranking and experimentation team might handle; it is not a real interview question or a claim that Google uses this exact task. The team needs a reliable implementation for traffic-distribution monitoring in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Compute Shannon entropy for a probability vector representing user-click outcomes.

Use base-2 logarithms so the answer is in bits. The input must be a non-empty 1-D vector of non-negative values that sums to 1, otherwise `ValueError` is raised; zero probabilities contribute nothing.

Implement `solve(p)`.

**Returns.** Return the entropy as a non-negative Python float.

Use base-2 logarithms so the answer is in bits. The input must be a non-empty 1-D vector of non-negative values that sums to 1, otherwise `ValueError` is raised; zero probabilities contribute nothing.

Implement `solve(p)`.

**Returns.** Return the entropy as a non-negative Python float.

### Examples

**Example 1**

Input:

```python
solve([0.5, 0.5])
```

Output:

```text
1.0
```

**Example 2**

Input:

```python
solve([0.9, 0.1])
```

Output:

```text
0.468996
```

**Example 3**

Input:

```python
solve([1.0, 0.0])
```

Output:

```text
0.0
```

**Example 4**

Input:

```python
solve([0.5, 0.6])
```

Output: Raises `ValueError`.

## Theory

### The simple version

Entropy measures how unpredictable an outcome is. If every click goes to one item it is perfectly predictable (0 bits); if clicks are spread evenly across many items it is as unpredictable as possible. Monitoring it over time reveals sudden concentration or drift in traffic.

### The formula

$$H(p)=-\sum_ip_i\log_2p_i,\qquad 0\log_20:=0$$

### Why it matters

- The entropy of a click distribution shows how concentrated traffic is: a sudden drop means a few items now take most clicks.
- Working in bits makes the numbers easy to read.

### How it works

1. Check the input is a non-empty probability vector summing to $1$.
2. Drop zero entries.
3. Compute $-\sum p\log_2p$.

### Worked example

For $(0.5,0.5)$ each term is $0.5\cdot\log_20.5=-0.5$, the sum is $-1$, and negating gives 1.0 bit. A distribution like $(0.9,0.1)$ would give about $0.47$ bits.

## Explanation

A fair split between two items is exactly one bit. A skewed split (second example) carries less uncertainty. Zero entries are dropped before the logarithm because $\log0$ is undefined and $p\log p\to0$.
