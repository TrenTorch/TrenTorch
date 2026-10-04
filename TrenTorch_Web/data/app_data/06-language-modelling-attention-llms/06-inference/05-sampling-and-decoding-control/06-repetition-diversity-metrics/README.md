---
name: lm-repetition-diversity-metrics
title: Repetition & Diversity Metrics
tags: [decoding, evaluation, diversity]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Tuning decoding settings needs numbers, not impressions. Two simple metrics describe a generated text. **Distinct-n** is the fraction of its n-grams that are unique: a text that repeats itself has a low value, and a text with no repeated n-gram has distinct-n equal to 1. The **repetition rate** is the fraction of n-gram positions that repeat an earlier one, which is simply `1 - distinct-n` for one text. For a _set_ of samples from the same prompt, distinct-n computed over all samples pooled together measures **diversity across samples**: low values mean the model keeps writing the same thing every time.

### From theory to code

Implement `distinct_n` and `corpus_distinct_n`.

### Constraints

- `tokens` is a list of tokens. `distinct_n(tokens, n)` is `unique n-grams / total n-grams`, or `0.0` if there are no n-grams.
- `corpus_distinct_n(samples, n)` pools the n-grams of every sample (n-grams never span two samples) and returns `unique pooled n-grams / total pooled n-grams`, or `0.0` if there are none.
- Return Python floats.

### Hints

<details>
<summary>Hint 1</summary>

Build n-grams as tuples with `zip(*[tokens[i:] for i in range(n)])` or a slice comprehension.

</details>

<details>
<summary>Hint 2</summary>

Sets of tuples count the uniques.

</details>

## Theory

### The simple version

A writer whose paragraphs reuse the same phrases scores low, and a team of five writers who all produce the same story scores low as a group even if each individual story reads fine.

### The formula

$$
\text{distinct-}n = \frac{|\{\text{n-grams}\}|}{\#\text{n-grams}}, \qquad \text{repetition rate} = 1 - \text{distinct-}n
$$

### How this is done in practice

Distinct-n and self-BLEU are the standard quick diversity checks for dialogue and story generation, and they expose the usual trade-off: lowering the temperature improves coherence and lowers diversity. They ignore meaning, so two different phrasings of one idea count as distinct.

## Explanation

Counting unique tuples is the entire algorithm. The pooled version shows why the same function applied to a collection of samples measures something different from the per-sample average.
