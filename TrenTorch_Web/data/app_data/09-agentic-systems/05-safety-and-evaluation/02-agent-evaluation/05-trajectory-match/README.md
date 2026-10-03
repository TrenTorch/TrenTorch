---
name: agentic-trajectory-match
title: Trajectory Matching
tags: [agentic-systems, evaluation, trajectories, lcs]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Sometimes the _path_ matters, not just the final answer: in a support workflow the agent must look up the account **before** issuing a refund, and verify identity **before** either. Comparing the sequence of tool names the agent used with a reference sequence checks this. Exact equality is too strict, since extra harmless calls are fine, and a set comparison ignores order. The **longest common subsequence** (LCS) is the natural middle ground: the longest sequence of steps appearing in both lists in the same relative order, with other steps allowed in between. Normalizing by the lengths gives an order-aware precision and recall.

### From theory to code

Implement `lcs_length` and `trajectory_match`.

### Constraints

- `lcs_length(a, b)` is the length of the longest common subsequence of two lists, computed by dynamic programming.
- `trajectory_match(actual, reference)` returns `(precision, recall, in_order)`: `precision = lcs / len(actual)` and `recall = lcs / len(reference)` (`0.0` for an empty denominator), and `in_order` is `True` iff `lcs == len(reference)`, meaning every reference step appears in order inside the actual trajectory.

### Hints

<details>
<summary>Hint 1</summary>

The table `dp[i][j]` holds the LCS of the first `i` elements of `a` and the first `j` of `b`.

</details>

<details>
<summary>Hint 2</summary>

Extra steps lower precision but do not break `in_order`.

</details>

## Theory

### The simple version

A recipe check: did the cook add the ingredients in the right order? Extra stirring in between is fine, but putting the eggs in after baking is not.

### The formula

$$
\text{LCS}(i, j) = \begin{cases} \text{LCS}(i-1, j-1) + 1 & a_i = b_j \\ \max(\text{LCS}(i-1, j), \text{LCS}(i, j-1)) & \text{otherwise}\end{cases}
$$

### How this is done in practice

Trajectory evaluation in agent frameworks (LangSmith, AgentEvals) offers strict, subset and unordered matches, and LCS-style scoring is a standard fourth option. Order constraints are often safety-critical, which is why they are checked separately from the outcome.

## Explanation

The dynamic program is the same one used for ROUGE-L in the Language Models track, applied to action names instead of words.
