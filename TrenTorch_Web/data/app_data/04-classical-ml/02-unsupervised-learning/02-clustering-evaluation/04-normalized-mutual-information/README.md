---
name: unsupervised-clustering-normalized-mutual-information
title: 'Normalized mutual information'
tags: [classical-ml, unsupervised, clustering, evaluation, information-theory]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Another way to compare a clustering with ground truth is to ask how much knowing one labeling tells you about the other. Mutual information measures that shared information in nats. It is hard to read on its own, because its scale depends on the entropy of each labeling, so normalized mutual information (NMI) divides it by the average of the two entropies. The result lies in [0, 1].

Implement `normalized_mutual_information(labels_true, labels_pred)` with arithmetic-mean normalization.

- Contingency counts n_ij over the two labelings, with p_ij = n_ij / N, and marginals p_i and p_j.
- MI = Σ p_ij · log(p_ij / (p_i · p_j)), summed over cells with p_ij > 0.
- H(U) = −Σ p_i log p_i, and H(V) likewise.
- NMI = MI / ((H(U) + H(V)) / 2).
- If both entropies are zero (each labeling has a single cluster), return `1.0`.

### Constraints

- Inputs must have the same length, otherwise raise `ValueError`.
- Use the natural logarithm.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Reuse the contingency table idea: `np.unique(..., return_inverse=True)` plus `np.add.at`.

</details>

<details>
<summary>Hint 2</summary>

Only sum over nonzero cells. Filter with `p_ij > 0` before taking logs.

</details>

## Theory

### The simple version

If knowing one clustering tells you the other exactly, the shared information equals each entropy and NMI is 1. If the two are unrelated, the shared information is zero and NMI is 0.

### The formula

$$
\text{NMI} = \frac{\text{MI}(U, V)}{\tfrac12\left(H(U) + H(V)\right)}
$$

## Explanation

`normalized_mutual_information` turns both labelings into a joint probability table, computes the mutual information over nonzero cells, and divides by the mean of the two entropies. Dropping zero cells before the log avoids `log(0)` without changing the sum.
