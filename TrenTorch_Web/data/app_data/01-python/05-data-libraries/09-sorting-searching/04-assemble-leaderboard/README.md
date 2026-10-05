---
name: numpy-assemble-leaderboard
title: 'Assemble: Leaderboard Queries'
tags: [numpy-core]
difficulty: Intermediate
---

## Statement

A game keeps one score per player in an array. Implement the four queries a leaderboard needs, using sorting and partial sorting rather than Python loops. `top_k` returns the indices of the `k` highest scores (highest first, ties by lower index), `competition_ranks` gives every player a 1-based rank where equal scores share the best rank ("1, 2, 2, 4"), `kth_largest` returns the `k`-th largest value without sorting the whole array, and `percentile_rank` reports what fraction of the scores each player strictly beats.

## Theory

### Four questions, one toolbox

| Question                              | Tool                                                          |
| ------------------------------------- | ------------------------------------------------------------- |
| who are the top $k$?                  | stable order, largest first (`argsort` of the negated scores) |
| what is each player's place?          | order, then rank with ties sharing the best place             |
| what is the $k$-th largest value?     | **partial** sort: `np.partition`                              |
| what share of players does each beat? | sorted values and `searchsorted`                              |

### Competition ranking

With scores `[90, 80, 80, 70]` the places are `1, 2, 2, 4`: equal scores share the best place and the next place is skipped. In terms of the descending-sorted scores `s`, a score $x$ has rank

$$
\text{rank}(x) = 1 + \#\{\,y : y > x\,\}
$$

and `1 + (number of strictly greater scores)` is exactly `n - searchsorted(ascending, x, side="right") + 1`.

### Partial sorting

You do not need the whole order to find the $k$-th largest. `np.partition(a, kth)` rearranges the array so that the element at position `kth` is the one a full sort would put there, with smaller elements before it and larger after, in $O(n)$ average time instead of $O(n \log n)$. The $k$-th largest is the element at position `n - k` of the partitioned array.

### Percentile rank

The fraction of scores a value strictly beats is

$$
\text{pr}(x) = \frac{\#\{\,y : y < x\,\}}{n} = \frac{\text{searchsorted}(\text{ascending}, x, \text{left})}{n}
$$

### Ties and determinism

Rankings must be reproducible, so every ordering here uses a stable sort: equal scores are ordered by their original index.

### How NumPy implements this

`partition` uses introselect (quickselect with a fallback), so it finds one order statistic without sorting the rest. `searchsorted` over a sorted copy answers all the percentile questions in $O(m \log n)$ for $m$ queries.

## Explanation

`top_k` takes the first `k` entries of the stable order from the negated scores. `competition_ranks` sorts the scores ascending once, and each player's rank is `n` minus the right insertion point of their score, plus one, which is one more than the number of strictly higher scores. `kth_largest` partitions at position `n - k` and reads that element. `percentile_rank` is the left insertion point of each score in the sorted scores divided by `n`, the number of strictly smaller scores as a fraction.
