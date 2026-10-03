---
name: lm-embedding-analogies
title: Embedding Analogies
tags: [embeddings, analogy, nearest-neighbor]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A famous property of word embeddings is that relationships between words become **directions** in the space: the vector from "man" to "woman" is roughly the vector from "king" to "queen". That makes analogy questions "a is to b as c is to ?" solvable by arithmetic. Compute the target `e_b - e_a + e_c` and return the word whose vector is **most similar by cosine** to it. One rule is essential: the three question words must be excluded from the answer, otherwise the nearest word to the target is usually one of the inputs (typically `c`).

### From theory to code

Implement `solve_analogy`.

### Constraints

- `E` has shape `(V, d)` and `vocab` is a list of `V` words. `solve_analogy(E, vocab, a, b, c)` takes three words from `vocab`.
- Compute `target = E[b] - E[a] + E[c]`. Score every word by cosine similarity with `target` (treat a zero-norm vector as similarity `0`).
- Exclude `a`, `b` and `c` from the candidates and return the word with the highest similarity (lowest index on ties).

### Hints

<details>
<summary>Hint 1</summary>

Normalize the rows of `E` once, normalize the target, then one matrix-vector product gives all cosines.

</details>

<details>
<summary>Hint 2</summary>

Set the excluded rows to `-inf` before `argmax`.

</details>

## Theory

### The simple version

If the step from "France" to "Paris" is "go to the capital", then taking the same step from "Japan" should land near "Tokyo". Subtracting and adding vectors performs the step.

### The formula

$$
\hat d = \arg\max_{w \notin \{a, b, c\}} \cos\big(e_w,\; e_b - e_a + e_c\big)
$$

### How this is done in practice

The analogy benchmark from the word2vec paper (Mikolov et al.) uses 19,544 such questions, including semantic (capital cities) and syntactic (verb tenses) relations. Gensim exposes `most_similar(positive=[b, c], negative=[a])`, the same computation.

## Explanation

A cosine nearest-neighbour search with an exclusion set. The tests use a hand-built embedding where the analogy holds exactly, and one showing why excluding the inputs is necessary.
