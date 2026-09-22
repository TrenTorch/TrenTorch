---
name: potd-top-hashtags
title: 'TOP HASHTAGS'
tags: [nlp]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** NLP

---

### Story

TikTok's hashtag-suggestion model needs a vocabulary built from raw captions before it can suggest
anything: take the `k` most frequent hashtags, everything else becomes `<unk>`.

---

### The Problem

Count hashtag frequency across all captions; return the top `k` by count, ties broken by earliest
first appearance in the input.

### Input Format

```
k
n
caption_1
...
caption_n
```

Hashtags are whitespace-separated tokens starting with `#`; non-hashtag words are ignored.

### Output Format

`k` lines (fewer if fewer than `k` distinct hashtags exist): `hashtag count`.

### Constraints

- `1 <= k <= 1000`, `1 <= n <= 10^4`
- Time limit: 1.0 second.

---

### Example

**Input**

```
2
1
#fyp #dance #fyp #comedy #fyp #dance #viral
```

**Output**

```
#fyp 3
#dance 2
```

## Theory

### The simple version

This is a straightforward popularity contest: count how often each hashtag shows up across every caption, then report the ones that showed up the most.

### "Most frequent" under-specifies the answer at a tie

Sorting by count alone leaves a tie at the `k`-th cutoff ambiguous: several hashtags can share the
same count right at the boundary. The tie-break rule here is **earliest first appearance across the
whole input**, not alphabetical. This must be stated and tested explicitly, since a solution that
breaks ties alphabetically will pass every test without a tie and fail silently the moment one
appears.

### Fewer than `k` distinct hashtags

If fewer than `k` distinct hashtags exist across all captions, the output simply has fewer than `k`
lines. There is no padding with placeholder entries.

### Case sensitivity, again

`#FYP` and `#fyp` are distinct hashtags, matching the case-sensitive convention used elsewhere in
this set (the amenity and one-hot encoder questions), not merged by lowercasing.

## Explanation

`top_k_hashtags` scans every caption's whitespace-split tokens in order, and for each token starting
with `#`, increments its count and records the token's index of first appearance the first time it
is seen (never overwritten after that). It then sorts the distinct hashtags by `(-count,
first_appearance_index)`: descending count first, and among equal counts, ascending first-appearance
index, which is exactly "earliest first appearance wins the tie." The first `k` entries of that
sorted list are the answer, and if fewer than `k` distinct hashtags exist, the list is simply
shorter than `k`.
