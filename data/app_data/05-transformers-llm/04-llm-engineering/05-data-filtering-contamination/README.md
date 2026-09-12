---
name: txf-llmeng-data-filtering-contamination
title: 'Data filtering and contamination: keeping eval data out of the training set'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A model's evaluation score is only meaningful if the evaluation questions were GENUINELY unseen during training; if a benchmark's text (or something close enough to it) leaked into the training corpus, the model can "solve" it by partial memorization rather than by the actual capability the benchmark claims to measure, inflating reported scores in a way that doesn't reflect real ability. "Contamination" checking is exactly `[04-deduplication]`'s near-duplicate detection idea, applied ACROSS two different sets (training data vs. evaluation data) instead of WITHIN one set: the goal isn't merely "is this document unique," it's specifically "does this training document overlap with anything from the evaluation set that must stay unseen."

### From theory to code

Implement `get_ngrams(tokens, n)` (every contiguous `n`-token window, as a set), `has_contamination(train_doc_tokens, eval_ngrams, n)` (does a training document share any `n`-gram with a precomputed evaluation-set n-gram pool), and `filter_contaminated_documents(train_documents, eval_documents, n)`, removing every contaminated training document.

### Constraints

- `n`-grams are built from CONTIGUOUS windows of exactly `n` tokens; a document shorter than `n` tokens produces an EMPTY n-gram set.
- The evaluation-set n-gram pool is built from EVERY evaluation document combined (a training document contaminating ANY one of them counts as contamination), not just the first.
- A single shared `n`-gram is sufficient to flag contamination (`len(train_ngrams & eval_ngrams) > 0`), no minimum overlap COUNT required.
- Larger `n` is a STRICTER, more specific contamination signal (fewer false positives from ordinary common phrasing); smaller `n` is looser and catches more, at the cost of more coincidental matches.

### Hints

<details>
<summary>Hint 1: n-grams</summary>

`{tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)}`. Tuples (not lists) so they're hashable and can live inside a `set`.

</details>

<details>
<summary>Hint 2: Building the eval pool, then filtering</summary>

```python
eval_ngrams = set()
for doc in eval_documents:
    eval_ngrams |= get_ngrams(doc, n)
return [i for i, doc in enumerate(train_documents) if not has_contamination(doc, eval_ngrams, n)]
```

</details>

## Theory

### The simple version

A teacher building a final exam who wants to make absolutely sure no exam question (or anything close to one) accidentally ended up in the practice materials students studied from. Before finalizing the practice set, every practice passage gets checked against every phrase that appears in the actual exam; anything that shares even a modestly long, specific phrase with the real exam gets pulled from the practice materials, so a student's practice-test performance genuinely reflects understanding, not memorization of the exam's own wording.

### The formula

```
eval_ngrams = union of get_ngrams(doc, n) for doc in eval_documents
contaminated(train_doc) = get_ngrams(train_doc, n) ∩ eval_ngrams ≠ ∅
kept = [doc for doc in train_documents if not contaminated(doc)]
```

### How PyTorch actually implements this

There is no `torch.nn` contamination-detection utility (a data-pipeline concern, run once before training, not a model component); real large-scale contamination checks (documented in GPT-3, PaLM, and LLaMA's own technical reports) typically use exactly this kind of n-gram overlap approach, often at `n=13` or similar (long enough to be a specific, unlikely-to-be-coincidental match, short enough to still be computationally practical), sometimes combined with MinHash-style approximate matching (mentioned in `[04-deduplication]`) to scale to billions of documents. Contamination checking and `[04-deduplication]` are conceptually the SAME core operation (n-gram or set overlap detection) applied to two different comparisons: within one corpus (deduplication) versus across a train/eval boundary that must never be crossed (contamination).

## Explanation

`get_ngrams` slides a window of exactly `n` tokens across a document, collecting every contiguous span as a tuple into a set (a document shorter than `n` tokens produces `range(len(tokens) - n + 1)` with a non-positive stop, correctly yielding an empty set). `has_contamination` checks whether a training document's own n-gram set intersects at all with a precomputed `eval_ngrams` pool. `filter_contaminated_documents` first builds that pool by unioning together the n-grams from EVERY evaluation document (so contamination against ANY eval document counts), then keeps only the training documents whose n-gram sets share nothing at all with that combined pool, exactly mirroring `[04-deduplication]`'s "keep only if it doesn't match anything it shouldn't" pattern, applied here across the crucial train/eval boundary rather than within one corpus.
