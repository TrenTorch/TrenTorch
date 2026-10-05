---
name: lm-rouge-scores
title: ROUGE
tags: [evaluation, summarization, text-metrics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Where BLEU asks "how much of what you wrote is in the reference" (precision), summarization cares more about the reverse: "how much of the reference did you cover" (recall). **ROUGE** is the family built around that. ROUGE-N counts overlapping n-grams. ROUGE-L uses the **longest common subsequence**, words that appear in the same order in both texts but not necessarily next to each other, so it rewards getting the structure right without demanding exact phrasing. Both are reported as precision, recall and F1.

### From theory to code

Implement `rouge_n` and `rouge_l`.

### Constraints

- Inputs are token lists. Both functions return a tuple `(precision, recall, f1)` of floats.
- `rouge_n(candidate, reference, n)`: overlap is the multiset intersection of the n-gram counts. Precision is `overlap / candidate n-grams`, recall is `overlap / reference n-grams`. A side with no n-grams makes its ratio `0.0`.
- `rouge_l(candidate, reference)`: let `L` be the length of the longest common subsequence. Precision is `L / len(candidate)` and recall is `L / len(reference)`, with `0.0` for an empty side.
- F1 is `2PR / (P + R)`, or `0.0` when `P + R == 0`.

### Hints

<details>
<summary>Hint 1</summary>

The longest common subsequence is a small dynamic program: `dp[i][j]` is the LCS length of the first `i` candidate tokens and the first `j` reference tokens.

</details>

<details>
<summary>Hint 2</summary>

Reuse one helper for the F1 computation.

</details>

## Theory

### The simple version

To check a book report you can count how many key phrases from the original appear in it (ROUGE-N), or you can check whether it tells the main events in the right order even if it phrases them differently (ROUGE-L).

### The formula

$$
\text{ROUGE-N}_{\text{recall}} = \frac{\sum_{g\in \text{ref}} \min(\text{count}_{\text{cand}}(g),\, \text{count}_{\text{ref}}(g))}{\sum_{g\in\text{ref}}\text{count}_{\text{ref}}(g)}
$$

and $\text{LCS}(i, j) = \text{LCS}(i-1, j-1) + 1$ if the tokens match, else $\max(\text{LCS}(i-1, j), \text{LCS}(i, j-1))$.

### How this is done in practice

The `rouge-score` package is the common implementation, with stemming and sentence-level ROUGE-Lsum on top. ROUGE correlates with human judgement for extractive summaries but is easily gamed by copying the source, which is why abstractive and long-form evaluations add faithfulness checks.

## Explanation

The n-gram variant reuses the counting idea from BLEU but reports recall as the headline. The LCS variant is a classic dynamic program that costs `O(len(candidate) * len(reference))`, trivial for sentences and the reason sentence-level rather than document-level ROUGE-L is typical.
