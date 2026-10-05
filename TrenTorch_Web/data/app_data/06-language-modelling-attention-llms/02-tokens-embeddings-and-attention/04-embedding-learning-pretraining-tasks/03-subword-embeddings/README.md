---
name: lm-subword-embeddings
title: Subword Embeddings
tags: [embeddings, fasttext, subwords]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Word2vec gives every word its own vector, so a word never seen in training, a typo or an inflected form like "unhappiness" has no embedding at all. **fastText** fixes this by representing a word as the sum of the vectors of its **character n-grams**. The word is wrapped in boundary markers (`<` and `>`), so "where" becomes `<where>` and its 3-grams are `<wh`, `whe`, `her`, `ere`, `re>`. Because words that share morphemes share n-grams, "unhappy" and "unhappiness" automatically get related vectors, and an unseen word still receives a vector built from whatever of its n-grams were learned.

### From theory to code

Implement `char_ngrams` and `subword_embedding`.

### Constraints

- `char_ngrams(word, n_min, n_max)` wraps the word as `'<' + word + '>'` and returns the list of all character n-grams for `n` from `n_min` to `n_max` inclusive, ordered by `n` then by start position, followed by the whole wrapped word `'<word>'` itself (always appended last, even if its length falls inside the range, but not duplicated if it already appeared as an n-gram).
- `subword_embedding(word, table, n_min, n_max, dim)` averages the vectors `table[g]` over the n-grams (from `char_ngrams`) that are keys of `table` (a dict from string to length-`dim` arrays). If none are present return a zero vector of length `dim`.

### Hints

<details>
<summary>Hint 1</summary>

The wrapped word of length `L` has `L - n + 1` n-grams of size `n` when `n <= L`.

</details>

<details>
<summary>Hint 2</summary>

Keep the whole word as the last entry so the output does not depend on whether the word is in the n-gram range.

</details>

## Theory

### The simple version

Reading an unfamiliar long word, you recognise the pieces ("un-", "happi", "-ness") and guess the meaning from them. The vector is the average of what the pieces mean.

### The formula

$$
v_w = \frac{1}{|G_w \cap \mathcal{K}|}\sum_{g \in G_w \cap \mathcal{K}} z_g
$$

where $G_w$ is the set of the word's n-grams (plus the word itself) and $\mathcal{K}$ the n-grams with learned vectors. fastText hashes n-grams into a fixed number of buckets instead of keeping them all.

### How this is done in practice

fastText's published models use n-grams of length 3 to 6. Subword units are also what BPE and WordPiece tokenizers use, which is why modern LLMs have no true out-of-vocabulary words.

## Explanation

N-gram extraction is a double loop, and the embedding is a masked mean. The tests show the property that matters: two morphologically related words share n-grams and therefore have positive cosine similarity even if one was never seen.
