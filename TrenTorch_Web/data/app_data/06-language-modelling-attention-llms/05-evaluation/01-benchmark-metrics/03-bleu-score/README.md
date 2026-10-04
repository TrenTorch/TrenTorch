---
name: lm-bleu-score
title: BLEU
tags: [evaluation, translation, text-metrics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

When the answer is a whole sentence rather than a short span, string equality is hopeless and we measure overlap instead. **BLEU** asks how many of the n-grams (runs of `n` consecutive words) in the candidate also appear in the reference. Counting matches naively is exploitable: a candidate that repeats "the the the the" matches the word "the" every time. So each candidate n-gram is credited at most as often as it appears in the reference (**clipping**). Precision alone also rewards very short outputs, so a **brevity penalty** reduces the score of candidates shorter than the reference. The final score is the geometric mean of the precisions for n = 1 to 4 times that penalty.

### From theory to code

Implement `modified_precision` and `bleu`.

### Constraints

- Candidates and references are lists of tokens. `references` is a list of reference token lists.
- `modified_precision(candidate, references, n)` is the number of candidate n-grams after clipping divided by the number of candidate n-grams. Clipping credits each n-gram at most `max over references of its count in that reference` times. Return `0.0` if the candidate has no n-grams of that order.
- `bleu(candidate, references, max_n=4)` is `BP * exp(mean(log p_n))` for `n = 1..max_n`, and `0.0` if any `p_n` is zero (no smoothing). `BP = 1` if `c > r` else `exp(1 - r / c)` where `c` is the candidate length and `r` is the length of the reference closest in length to `c` (the shorter one on ties).
- Return Python floats.

### Hints

<details>
<summary>Hint 1</summary>

`Counter` of n-gram tuples makes clipping a one-liner: `min(count, max_ref_count)` per n-gram.

</details>

<details>
<summary>Hint 2</summary>

Pick `r` with `min(lengths, key=lambda l: (abs(l - c), l))`.

</details>

## Theory

### The simple version

A translator is rewarded for using the same phrases an expert would, but cannot cheat by repeating a safe phrase endlessly (clipping) and cannot cheat by saying only two safe words (brevity penalty).

### The formula

$$
\text{BLEU} = \text{BP}\cdot\exp\!\Big(\tfrac{1}{N}\sum_{n=1}^{N}\ln p_n\Big), \qquad
\text{BP} = \begin{cases}1 & c > r\\ e^{\,1 - r/c} & c \le r\end{cases}
$$

where $p_n$ is the clipped n-gram precision. The geometric mean makes a zero at any order zero overall, which is why short sentences are usually scored with smoothing.

### How this is done in practice

`sacrebleu` is the standard implementation because BLEU is very sensitive to tokenization and smoothing details. BLEU correlates with human judgement reasonably for translation and poorly for open-ended generation, so modern evaluations pair it with learned or model-based metrics.

## Explanation

The solution counts n-grams per order, clips against the best reference count, and combines the precisions in log space. The tests contain the classic degenerate candidate (the same word repeated) to show clipping working, and a short candidate to show the brevity penalty working.
