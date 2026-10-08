---
name: problem-19-bayes-posterior
title: 'Bayes Posterior'
tags: [problemset, maths-stats-for-ml, bayesian-inference]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'Bayesian inference'
hint: 'numerator is prior times likelihood, denominator adds the alternative'
tools: [NumPy]
---

## Statement

Compute the posterior probability of hypothesis $H_1$ from its prior probability and the likelihood of the observed evidence under $H_1$ and under $H_0$.

Implement `solve(prior, likelihood_h1, likelihood_h0)`.

**Returns.** Return a float in $[0, 1]$. The prior of $H_0$ is $1-\text{prior}$. The prior and both likelihoods must lie in $[0, 1]$, and if the total evidence $P(e)$ is zero the posterior does not exist; both cases raise `ValueError`.

### Examples

**Example 1**

Input:

```python
solve(0.5, 0.8, 0.2)
```

Output:

```text
0.8
```

**Example 2**

Input:

```python
solve(0.01, 0.9, 0.05)
```

Output:

```text
0.153846
```

## Theory

### The simple version

Bayes' rule updates a belief after seeing evidence. A rare hypothesis stays fairly unlikely even after fairly strong evidence, because most of the evidence still comes from the common alternative.

### The formula

$$P(H_1\mid e)=\frac{P(H_1)\,P(e\mid H_1)}{P(H_1)\,P(e\mid H_1)+P(H_0)\,P(e\mid H_0)}$$

### Why it matters

- Bayes' rule is how a prior belief is updated by evidence, and it explains why rare events stay unlikely even after a positive test.
- It is the foundation of Bayesian classifiers and of probabilistic reasoning in general.

### How it works

1. Multiply the prior by the likelihood under $H_1$.
2. Multiply the complementary prior by the likelihood under $H_0$.
3. Divide the first product by the sum of both.

### Worked example

With prior $0.5$ and likelihoods $0.8$ and $0.2$: the numerator is $0.5\cdot0.8=0.4$, the other term is $0.5\cdot0.2=0.1$, so the posterior is $0.4/(0.4+0.1)=0.8$.

## Explanation

The second example shows the base-rate effect: a test that is $90\%$ sensitive with a $5\%$ false-positive rate gives only about a $15\%$ posterior when the prior is $1\%$.
