---
name: txf-llmeng-deduplication
title: 'Deduplication: removing near-identical documents before training'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Real training corpora, scraped from the web or assembled from many sources, contain a LOT of near-duplicate content: the same article mirrored on several sites, boilerplate legal text repeated across thousands of documents, near-identical product descriptions. Training on heavily duplicated data wastes compute (the model sees essentially the same information many times over, without learning anything new from the repetition) and, more seriously, can cause the model to MEMORIZE that duplicated content disproportionately (Lee et al. 2021 showed measurably higher memorization and verbatim regurgitation of content that appears many times in training data), a real quality and privacy concern for production LLMs. Deduplication removes documents that are EXACT or NEAR duplicates of something already kept, before training ever sees them.

### From theory to code

Implement `jaccard_similarity(tokens_a, tokens_b)`, a standard set-overlap similarity measure, and `deduplicate_documents(documents, threshold)`, greedily keeping a document only if it isn't a near-duplicate (similarity `>= threshold`) of anything ALREADY kept.

### Constraints

- Jaccard similarity operates on token SETS, not lists: `|intersection| / |union|`, so repeated tokens within one document don't inflate similarity.
- `deduplicate_documents` processes documents IN ORDER, comparing each one against EVERY already-kept document (not just the immediately preceding one), keeping it only if it fails to match (at or above `threshold`) all of them.
- Returns the INDICES of kept documents (into the original list), preserving their original relative order.

### Hints

<details>
<summary>Hint 1: Jaccard similarity</summary>

```python
set_a, set_b = set(tokens_a), set(tokens_b)
return len(set_a & set_b) / len(set_a | set_b)
```

</details>

<details>
<summary>Hint 2: Greedy deduplication</summary>

```python
kept_indices = []
for i, doc in enumerate(documents):
    if not any(jaccard_similarity(doc, documents[j]) >= threshold for j in kept_indices):
        kept_indices.append(i)
return kept_indices
```

</details>

## Theory

### The simple version

A librarian cataloging new book donations one at a time: before shelving a new book, they check it against EVERY book already on the shelf (not just the most recently shelved one) for substantial overlap, and only shelve it if it's genuinely different enough from everything already there. A book that's a word-for-word reprint of one already shelved gets set aside; a book that merely shares a FEW words or themes with an existing one stays.

### The formula

```
jaccard(A, B) = |A ∩ B| / |A ∪ B|

kept = []
for doc in documents (in order):
    if max(jaccard(doc, k) for k in kept) < threshold:
        kept.append(doc)
```

### How PyTorch actually implements this

There is no `torch.nn` deduplication utility (this is a DATA preprocessing step, run once before training even starts, not a model component); real large-scale deduplication pipelines (used to build corpora for GPT, LLaMA, and similar models) use MinHash or SimHash (locality-sensitive hashing schemes that approximate Jaccard similarity far more cheaply than this question's exact `O(n^2)` all-pairs comparison, since real corpora have far too many documents to compare every pair directly). This question's exact, brute-force version is the right SCALE to understand the underlying idea; production systems trade some accuracy for the ability to run on billions of documents.

## Explanation

`jaccard_similarity` converts both token lists to SETS (collapsing any repeated tokens within a document, since only DISTINCT content matters for measuring overlap) and computes `|intersection| / |union|`, `1.0` for identical sets, `0.0` for entirely disjoint ones. `deduplicate_documents` walks through `documents` in order, and for each one, checks its similarity against EVERY document already accepted into `kept_indices` (not merely the previous document, since a near-duplicate could appear anywhere earlier in the corpus, not just immediately before it); if none of those comparisons reach `threshold`, the document is genuinely new content and gets kept, otherwise it's dropped as a near-duplicate of something the training corpus already contains.
