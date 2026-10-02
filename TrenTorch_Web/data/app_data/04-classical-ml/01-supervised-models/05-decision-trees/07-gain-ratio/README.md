---
name: decision-trees-gain-ratio
title: Gain ratio for a categorical feature
tags: [classical-ml, decision-trees, splitting-criteria]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Information gain has a flaw: a feature with many distinct values (an ID column, say) splits the data into tiny, perfectly pure groups and looks wonderful, while telling you nothing about unseen samples. Gain ratio divides the gain by how finely the feature splits the data, so many-valued features are penalised.

### From theory to code

Implement `gain_ratio(feature, labels)`. Split `labels` into one group per distinct value of `feature`, compute the information gain of that split, then divide by the split's intrinsic value. Use base-2 logarithms throughout.

### Constraints

- `feature` and `labels` are one-dimensional arrays of equal length; either can hold arbitrary integers.
- Return a Python `float`.
- Return `0.0` for empty input, and `0.0` when the feature has a single distinct value (its intrinsic value is zero).
- Use base-2 logs, so entropy is measured in bits.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Entropy is `-sum(p * log2(p))` over class proportions. Information gain is the parent entropy minus the size-weighted entropy of the child groups.

</details>

<details><summary>Hint 2</summary>

The intrinsic value is the entropy of the _group sizes_ themselves: `-sum(w * log2(w))`, where `w` is each group's share of the samples.

</details>

## Theory

### The simple version

Information gain rewards any split that makes groups purer, even a split into one-sample groups. Gain ratio asks a second question: how many ways did you have to slice the data to get that gain? A feature that slices into many small groups pays a large penalty.

### The formula

$$\operatorname{Gain}(D, a) = H(D) - \sum_{v} \frac{|D_v|}{|D|} H(D_v)$$

$$\operatorname{IV}(a) = -\sum_{v} \frac{|D_v|}{|D|} \log_2 \frac{|D_v|}{|D|}$$

$$\operatorname{GainRatio}(D, a) = \frac{\operatorname{Gain}(D, a)}{\operatorname{IV}(a)}$$

where $D_v$ is the set of samples whose feature `a` equals $v$.

### How libraries implement this

C4.5 uses gain ratio instead of plain information gain. scikit-learn's trees offer `gini`, `entropy` and `log_loss` criteria but not gain ratio, so this is usually written by hand.

## Explanation

`np.unique(feature, return_counts=True)` gives both the distinct values and the group sizes in one call. The size shares are reused twice: once to weight the child entropies for the gain, and once as the distribution whose entropy is the intrinsic value. The early return on a zero intrinsic value avoids dividing by zero for a constant feature.
