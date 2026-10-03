---
name: agentic-reciprocal-rank-fusion
title: Reciprocal Rank Fusion
tags: [agentic-systems, retrieval, rag, hybrid-search]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Different retrievers are good at different things. Keyword search (BM25) finds exact terms and rare identifiers, vector search finds paraphrases. **Hybrid search** runs both and merges the lists, but their scores live on incompatible scales (BM25 scores are unbounded, cosine similarities are in `[-1, 1]`), so adding raw scores is meaningless. **Reciprocal rank fusion** (RRF) ignores scores and uses only ranks: a document earns `1 / (k + rank)` from each list it appears in, and documents are sorted by their total. A document ranked well by several retrievers rises to the top, and the constant `k` (typically 60) softens the advantage of rank 1.

### From theory to code

Implement `reciprocal_rank_fusion`.

### Constraints

- `rankings` is a list of ranked lists of document ids, best first. Ranks start at 1.
- The score of a document is the sum over the lists in which it appears of `1 / (k + rank)`. Documents missing from a list get nothing from it.
- Return the list of all document ids sorted by score descending, ties broken by id ascending (ids are sortable).

### Hints

<details>
<summary>Hint 1</summary>

Accumulate scores in a dictionary while enumerating each list with `start=1`.

</details>

<details>
<summary>Hint 2</summary>

Documents appearing in several lists naturally accumulate more.

</details>

## Theory

### The simple version

Two judges each rank the contestants without sharing score sheets. A contestant both judges like gets pushed to the top, and a single enthusiastic judge cannot dominate.

### The formula

$$
\text{RRF}(d) = \sum_{r \in R} \frac{1}{k + \text{rank}_r(d)}
$$

### How this is done in practice

RRF is the default fusion in Elasticsearch, OpenSearch, Weaviate and Azure AI Search hybrid queries. Its robustness comes from not needing score calibration, at the cost of ignoring how large the gaps between scores are.

## Explanation

A dictionary and a sort. The tests show the characteristic behaviours: agreement beats single-list dominance and absent documents are simply not rewarded.
