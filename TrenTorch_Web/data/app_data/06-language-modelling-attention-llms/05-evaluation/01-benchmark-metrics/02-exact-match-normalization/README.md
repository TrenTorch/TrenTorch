---
name: lm-exact-match-normalization
title: Exact Match & Token F1
tags: [evaluation, question-answering, text-metrics]
difficulty: Beginner
---

## Statement

### The problem, from first principles

For short-answer tasks the simplest metric is whether the model's answer equals the reference. Taken literally it is brutal: "The Eiffel Tower." and "eiffel tower" are the same answer to a human and different strings to a computer. Benchmarks therefore normalize both sides first (lowercase, strip punctuation and articles, collapse whitespace) and then compare. Exact match is all-or-nothing, so a partially correct answer scores zero. **Token F1** gives partial credit by measuring the overlap of words between prediction and reference, which is why question-answering leaderboards usually report both.

### From theory to code

Implement `normalize_answer`, `exact_match` and `token_f1`.

### Constraints

- `normalize_answer(s)`: lowercase, delete every character in `string.punctuation`, remove the standalone words `a`, `an` and `the`, then collapse runs of whitespace to single spaces and strip.
- `exact_match(prediction, golds)` is `1.0` if the normalized prediction equals the normalized form of **any** reference in `golds`, else `0.0`.
- `token_f1(prediction, gold)` splits both normalized strings on whitespace and counts overlapping tokens as a multiset intersection. If either side is empty the score is `1.0` when both are empty and `0.0` otherwise. Otherwise precision is `overlap / len(pred tokens)`, recall is `overlap / len(gold tokens)` and F1 is their harmonic mean, or `0.0` if the overlap is `0`.
- Use only the standard library plus NumPy.

### Hints

<details>
<summary>Hint 1</summary>

Remove punctuation before removing articles, so "the," does not survive as a token.

</details>

<details>
<summary>Hint 2</summary>

`collections.Counter(a) & Counter(b)` is the multiset intersection and `sum(c.values())` its size.

</details>

## Theory

### The simple version

Grading short answers by hand you would not mark "The Moon" wrong for the capital letter. Exact match is the strict teacher, F1 the generous one who gives half marks for "the big red apple" when the reference is "red apple".

### The formula

$$
P = \frac{|\text{pred} \cap \text{gold}|}{|\text{pred}|}, \quad
R = \frac{|\text{pred} \cap \text{gold}|}{|\text{gold}|}, \quad
F_1 = \frac{2PR}{P + R}
$$

Overlap counts repeated tokens as many times as the smaller of the two counts, so repeating a correct word does not raise the score.

### How this is done in practice

This is the SQuAD evaluation script, reused by many open-domain QA benchmarks. For open-ended generation, string overlap breaks down and evaluation moves to model-based graders, which the later questions in this section cover.

## Explanation

Normalization is a pipeline of small, order-sensitive steps. Exact match compares against every reference, and F1 uses a multiset intersection to count shared tokens fairly. The empty-answer rule matters in practice: models sometimes output nothing and datasets sometimes have empty gold answers for unanswerable questions.
