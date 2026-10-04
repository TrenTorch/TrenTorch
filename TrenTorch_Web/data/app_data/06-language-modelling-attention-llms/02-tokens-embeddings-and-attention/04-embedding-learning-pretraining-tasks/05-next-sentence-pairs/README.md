---
name: lm-next-sentence-pairs
title: Next-Sentence Pair Construction
tags: [pretraining, bert, data-construction]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Besides filling blanks, BERT's original pretraining included a second task: given two segments, decide whether the second **actually follows** the first in the text or was drawn from somewhere else. Building the training set is a data-engineering exercise. For each pair of consecutive sentences in a document, flip a fair coin. On heads keep the true pair and label it `1`. On tails replace the second sentence with a random sentence from a **different** document and label it `0`, since a random sentence from the same document might be a legitimate continuation and would poison the label. Later work found this task adds little, but the pattern of constructing positive and negative pairs appears everywhere in contrastive training.

### From theory to code

Implement `make_pairs`.

### Constraints

- `docs` is a list of documents, each a list of sentence strings. `rng` is a `np.random.RandomState`. Iterate documents in order and, inside each, consecutive sentence pairs `(docs[i][k], docs[i][k + 1])` in order.
- For each pair draw `u = rng.random_sample()`. If `u < 0.5` emit `(a, b, 1)`. Otherwise build the list `others` of all sentences from documents other than `i` (in document order, then sentence order), draw `idx = rng.randint(len(others))` and emit `(a, others[idx], 0)`.
- Return the list of triples. If there is only one document, every negative has no candidate: raise `ValueError` in that case before generating anything.

### Hints

<details>
<summary>Hint 1</summary>

Draw `u` first for every pair, then the index only when needed, so the stream is predictable.

</details>

<details>
<summary>Hint 2</summary>

Building `others` per document, not per pair, is fine.

</details>

## Theory

### The simple version

Making true/false cards for a reading quiz: half the cards pair a sentence with the one that really follows, the other half pair it with a sentence borrowed from an unrelated book.

### The formula

$$
(a_k, b, y) = \begin{cases}(s_k, s_{k+1}, 1) & u < \tfrac12\\ (s_k, \tilde s, 0),\ \tilde s \sim \text{Uniform}(\text{sentences of other docs}) & \text{otherwise}\end{cases}
$$

### How this is done in practice

The original BERT used NSP with 50/50 sampling. Successors such as ALBERT replaced it with sentence-order prediction (two consecutive segments in the right or swapped order), a harder task that does not leak topic information.

## Explanation

The only subtleties are the stated draw order and the source of the negatives. The tests replay the random stream to check both.
