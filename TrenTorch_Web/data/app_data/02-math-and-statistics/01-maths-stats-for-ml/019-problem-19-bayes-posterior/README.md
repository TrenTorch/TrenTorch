---
name: problem-19-bayes-posterior
title: "Bayes Posterior"
tags: [problemset, maths-stats-for-ml, bayesian-inference]
difficulty: Intermediate
kind: problemset
relatedModule: "part-math|Probability"
topic: "Bayesian inference"
hint: "apply Bayes' numerator and normalize both hypotheses"
tools: [NumPy]
---

# Bayes Posterior

## Statement

Implement `solve(prior, likelihood_h1, likelihood_h0)`. Compute the posterior probability of hypothesis H1 from its prior probability and the likelihoods under H1 and H0.

## Theory

Bayes’ rule normalizes prior-weighted likelihoods: P(H1|E)=P(E|H1)P(H1)/P(E).

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve(0.2, 0.8, 0.1)
```

Output:
```text
0.6666666666666666
```

**Example 2**

Input:
```python
solve(0.5, 0.2, 0.2)
```

Output:
```text
0.5
```
