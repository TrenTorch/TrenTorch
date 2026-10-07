---
name: stable-softmax-logits-company-201
title: 'stable-softmax-logits — Netflix case'
tags: [problemset, maths-stats-for-ml, probability-foundations, netflix]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Netflix'
hint: 'subtract the max logit before exponentiating'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Netflix** ranking and experimentation team might handle; it is not a real interview question or a claim that Netflix uses this exact task. The team needs a reliable implementation for score-to-probability conversion in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Given a vector of model logits, convert them into probabilities without overflowing when logits are large.

Use the maximum-subtraction form of softmax so that logits in the thousands do not overflow.

Implement `solve(logits)`.

**Returns.** Return a NumPy vector of probabilities with the same length as `logits`; the entries are positive and sum to 1.

### Examples

**Example 1**

Input:

```python
solve([1000.0, 1001.0])
```

Output:

```text
[0.268941, 0.731059]
```

**Example 2**

Input:

```python
solve([0.0, 0.0, 0.0])
```

Output:

```text
[0.333333, 0.333333, 0.333333]
```

**Example 3**

Input:

```python
solve([-1000.0, 0.0])
```

Output:

```text
[0.0, 1.0]
```

## Theory

### The simple version

Softmax turns scores into probabilities, but $e^{1000}$ is too large for a floating-point number and becomes infinity, which gives `nan`. The fix relies on a harmless identity: subtracting the same number from every logit leaves the result unchanged.

### The formula

$$p_i=\frac{e^{z_i-m}}{\sum_je^{z_j-m}},\qquad m=\max_jz_j$$

## Explanation

After the shift the largest exponent is $0$, so every term lies in $(0,1]$ and the denominator is at least $1$. Very negative logits underflow harmlessly to $0$ (third example). Equal logits give a uniform distribution (second example).
