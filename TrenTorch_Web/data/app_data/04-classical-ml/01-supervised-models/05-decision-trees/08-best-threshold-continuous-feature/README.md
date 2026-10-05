---
name: decision-trees-best-threshold-continuous-feature
title: Best split threshold for a continuous feature
tags: [classical-ml, decision-trees, splitting-criteria]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A categorical feature splits a node by value; a continuous one has infinitely many possible cut points. Fortunately only cut points _between_ observed values can change which samples go left, so a finite set of candidates is enough.

### From theory to code

Implement `best_threshold(x, y)`. Sort the distinct values of `x`, take the midpoint of every pair of consecutive values as a candidate threshold, send samples with `x <= t` left and the rest right, and return the candidate with the highest information gain (base-2 entropy) together with that gain.

### Constraints

- `x` is a one-dimensional float array and `y` an integer label array of the same length; neither is guaranteed sorted.
- Return a tuple `(threshold, gain)` of two Python floats.
- On ties, return the smallest threshold.
- If `x` has fewer than two distinct values there is nothing to split: return `(None, 0.0)`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Candidates come from `np.unique(x)`, which already sorts and de-duplicates.

</details>

<details><summary>Hint 2</summary>

For each candidate, gain is the parent entropy minus the size-weighted entropy of the left and right groups. Keep a candidate only if its gain beats the best so far by more than a tiny tolerance, so earlier (smaller) thresholds win ties.

</details>

## Theory

### The simple version

To split on a number, ask 'is x at most t?'. Try every sensible `t`, score each by how much purer the two sides become, and keep the best. Midpoints are the sensible values: any threshold between the same two neighbouring data points sends exactly the same samples left.

### The formula

For a candidate threshold $t$, with $D^- = \{x \le t\}$ and $D^+ = \{x > t\}$:

$$\operatorname{Gain}(D, t) = H(D) - \frac{|D^-|}{|D|} H(D^-) - \frac{|D^+|}{|D|} H(D^+)$$

Candidates are $t = (a_i + a_{i+1}) / 2$ for consecutive distinct sorted values $a_i$.

### How libraries implement this

C4.5 and CART both evaluate midpoints (or the sorted values themselves) of continuous features. scikit-learn sorts each feature once per node and sweeps a running class-count so every candidate is scored in one pass; the loop here is the clearer, slower equivalent.

## Explanation

Using the midpoint keeps the threshold strictly between two observed values, so it never coincides with a sample. The `1e-12` tolerance makes ties resolve to the first (smallest) candidate instead of whichever floating-point rounding favours.
