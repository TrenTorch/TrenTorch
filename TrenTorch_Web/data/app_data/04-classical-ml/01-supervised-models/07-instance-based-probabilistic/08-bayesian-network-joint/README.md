---
name: bayes-network-joint-probability
title: 'Joint probability in a discrete Bayesian network'
tags: [classical-ml, bayesian-networks, conditional-probability, factorization]
difficulty: Intermediate
---

## Statement

### Multiply the local tables to get one joint probability

A discrete Bayesian network factorizes the joint distribution into one conditional table per node: `P(x) = product_i P(x_i | parents of x_i)`. This question computes the probability of one full assignment.

Implement `joint_probability(x, parents, cpts)`.

- `x` is a sequence with one integer value per node.
- `parents[i]` is a tuple of node indices that are the parents of node `i`. It is empty for a root.
- `cpts[i]` is a NumPy array with one axis per parent (in the order given by `parents[i]`) followed by a last axis for node `i`. Each row along the last axis sums to 1.
- Return the product of `cpts[i][parent values..., x_i]` over all nodes, as a float.

### Constraints

- `len(x)`, `len(parents)` and `len(cpts)` must match. Otherwise raise `ValueError`.
- A table whose number of axes is not `len(parents[i]) + 1` raises `ValueError`.
- A table whose last-axis rows do not sum to 1 raises `ValueError`.
- A value outside its axis range raises `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Build the index for node `i` as a tuple: the parent values followed by `x[i]`. Then index the table with that tuple.

</details>

## Theory

The factorization follows from the chain rule plus the conditional independence assumptions in the graph. Each node only needs its own table, so the number of parameters falls from exponential in the number of variables to roughly the sum of the table sizes over the parent sets. Once the tables are known, any joint, marginal or conditional probability is a sum or ratio of products of entries from these tables.

### Where this shows up in production

Discrete Bayesian networks run inside medical decision support, where a diagnosis node depends on symptom and test nodes, and inside alerting systems that score a combination of discrete events. Industrial reliability models use them to combine component failure states. In each case the network is written by domain experts or learned from data, then used to score rare combinations.

### Using it to make decisions

Use a network when you need to answer a question about a combination of variables that rarely appears in the data, because the factorization shares statistical strength across cells. Check the table sizes before you commit: a node with many parents needs an exponentially large table, so you may need a noisy-OR or another compact form. Validate the structure against held-out events, since a wrong edge produces confident and wrong probabilities.

### Pros and cons

**Pros:** the model is interpretable, the parameters are local and easy to audit, it handles missing inputs by summing them out, and it encodes causal assumptions that domain experts can review.

**Cons:** tables grow quickly with the number of parents, so dense networks need many parameters. Structure learning is hard and the result can be unstable. Probabilities are only as good as the independence assumptions, and a single wrong edge can make the model confidently wrong.

## Explanation

The solution loops over the nodes, builds each node's index from its parent values and its own value, and multiplies the table entries. The validation checks run before the product, so a malformed table fails loudly rather than returning a silent number.
