---
name: instance-based-probabilistic-bayes-minimum-risk-decision
title: Bayes decision rule with misclassification costs
tags: [classical-ml, bayesian-decision-theory, cost-sensitive]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Choosing the most probable class is only optimal when every mistake costs the same. If wrongly clearing a fraudulent payment is far worse than wrongly flagging a good one, the best decision is the one with the smallest _expected cost_, which can differ from the most probable class.

### From theory to code

Implement `minimum_risk_class(posteriors, cost_matrix)`. For each possible prediction, compute its expected cost under the posterior, and return the prediction with the lowest cost.

### Constraints

- `posteriors` is a one-dimensional array of class probabilities summing to 1.
- `cost_matrix[i][j]` is the cost of predicting class `j` when the true class is `i`; it is square.
- Return a Python `int`. On ties, return the smallest class index.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The expected cost of predicting `j` is `sum_i posteriors[i] * cost_matrix[i][j]`.

</details>

<details><summary>Hint 2</summary>

That is a vector-matrix product: `posteriors @ cost_matrix` gives every prediction's risk at once.

</details>

## Theory

### The simple version

Weigh each possible mistake by how likely it is and how much it hurts, then pick the choice that hurts least on average. With equal costs for every mistake this reduces to 'pick the most probable class'.

### The formula

$$R(c_j \mid x) = \sum_{i} P(c_i \mid x)\, \lambda_{ij}, \qquad h^{*}(x) = \arg\min_{j} R(c_j \mid x)$$

where $\lambda_{ij}$ is the cost of predicting $c_j$ when the truth is $c_i$.

### How libraries implement this

scikit-learn classifiers have no cost-matrix argument at prediction time; this rule is typically applied on top of `predict_proba` output.

## Explanation

A single matrix product turns the posterior into per-prediction risks, and `argmin` picks the cheapest, breaking ties toward the smallest index.
