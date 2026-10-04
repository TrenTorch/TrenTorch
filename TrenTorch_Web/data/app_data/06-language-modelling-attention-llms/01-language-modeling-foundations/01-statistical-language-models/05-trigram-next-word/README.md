---
name: lm-trigram-next-word
title: Trigram Models & Longer Context
tags: [language-modeling, n-gram]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Looking back one symbol is too short. After "the cat" the next word is very different from after "the dog", yet a bigram model sees only "the" or "cat" alone. Conditioning on the previous **two** tokens gives a trigram model, and the trade-off appears at once: longer context makes predictions sharper, but the number of possible contexts grows with the square of the vocabulary, so most contexts are seen rarely or never. This is the data-sparsity problem that smoothing softens and that neural models later solve by sharing statistical strength between similar contexts. At the word level we also need sentence boundaries, so each sentence is padded with two start markers and one end marker.

### From theory to code

Implement `trigram_next_distribution(sentences, w1, w2, alpha)`. It returns the vocabulary and the smoothed probability of each token following the context `(w1, w2)`.

### Constraints

- `sentences` is a list of token lists. Pad each as `['<s>', '<s>'] + tokens + ['</s>']`.
- The vocabulary `vocab` is the sorted list of distinct tokens appearing in the sentences plus `'</s>'`. The marker `'<s>'` is never predicted, so it is not in `vocab`.
- Count every triple `(a, b, c)` of consecutive padded tokens. For the context `(w1, w2)` return `(count(w1, w2, c) + alpha) / (total for this context + alpha * len(vocab))` for each `c` in `vocab`.
- `alpha > 0`. A context never seen gives the uniform distribution.
- Return `(vocab, probs)` with `probs` a NumPy array aligned with `vocab`.

### Hints

<details>
<summary>Hint 1</summary>

A dictionary keyed by the pair `(a, b)` whose value is a `Counter` of next tokens keeps the lookup cheap.

</details>

<details>
<summary>Hint 2</summary>

Only the tokens after the chosen context matter, so you can stop counting everything else.

</details>

## Theory

### The simple version

Predicting the next word after "I would like a cup of" is easy because "cup of" strongly suggests "tea" or "coffee". The model that only sees "of" has to guess from everything that ever followed "of". Two words of context narrow it dramatically, at the price of needing many more examples.

### The formula

$$
P(c \mid a, b) = \frac{N_{abc} + \alpha}{N_{ab\cdot} + \alpha V}
$$

The number of possible contexts is $V^2$, so a corpus must be far larger than $V^2$ for most of them to be observed. A generic order-$n$ model has $V^{n-1}$ contexts, which is why classical n-gram models rarely go beyond 5-grams.

### How this is done in practice

Production n-gram systems (KenLM, SRILM) store counts in tries and use Kneser-Ney smoothing with back-off to shorter contexts instead of one constant `alpha`. Today the same prediction problem is solved by a transformer, whose context window plays the role of `n` but whose parameters are shared across contexts instead of stored per context.

## Explanation

The solution pads and counts the triples, then reads the row for the requested context and applies the same add-`alpha` formula as the bigram case but with the context total in the denominator. A context that never occurred has total zero and every count zero, so every probability becomes `alpha / (alpha * V) = 1 / V`, the uniform distribution, with no special-casing.
