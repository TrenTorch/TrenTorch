---
name: agentic-diverse-retrieval-mmr
title: Maximal Marginal Relevance
tags: [agentic-systems, retrieval, rag, diversity]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Retrieving the top-`k` documents by similarity has a failure mode: if the best five passages are near-duplicates (the same fact on five web pages), they waste the context window and crowd out other useful information. **Maximal marginal relevance** (MMR) selects documents one at a time, scoring each candidate by how relevant it is to the query _minus_ how similar it is to what has already been chosen. A parameter `lam` between 0 and 1 controls the balance: `lam = 1` is plain top-`k` relevance, `lam = 0` is pure diversity.

### From theory to code

Implement `mmr_select`.

### Constraints

- `query` is a vector and `docs` is a list of vectors (plain Python lists). Similarity is cosine similarity (`0.0` for zero vectors).
- Select `k` documents greedily. At each step choose the unselected document maximizing `lam * sim(query, d) - (1 - lam) * max(sim(d, s) for s in selected)`, where the max over an empty selection is `0`. Ties go to the lower index.
- Return the selected indices in selection order. If `k` exceeds the number of documents, return all of them.

### Hints

<details>
<summary>Hint 1</summary>

The first pick is always the most relevant document, since nothing has been selected yet.

</details>

<details>
<summary>Hint 2</summary>

Compute the cosine similarities as you go, or precompute the pairwise matrix once.

</details>

## Theory

### The simple version

Assembling a reading list: the first book is the best on the topic, but the second should add something new rather than say the same thing.

### The formula

$$
d^\ast = \arg\max_{d \notin S}\Big[\lambda\,\text{sim}(q, d) - (1 - \lambda)\max_{s \in S}\text{sim}(d, s)\Big]
$$

### How this is done in practice

MMR is a built-in search type in LangChain and most vector stores. Alternatives include maximum-diversity sampling and determinantal point processes, and re-rankers can replace the heuristic with a learned score.

## Explanation

A greedy loop with a running selection. The key behaviour, preferring a slightly less relevant but different document over a duplicate, is verified in the tests.
