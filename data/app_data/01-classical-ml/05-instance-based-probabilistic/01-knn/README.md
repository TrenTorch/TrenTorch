---
name: instance-based-probabilistic-knn
title: 'KNN: distance and neighbor lookup'
tags: [classical-ml, instance-based, knn]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every model earlier in this curriculum learns a fixed set of parameters once — `weight`/`bias` for linear/logistic regression, a tree's splits for `03-decision-trees` — and then discards the training data, using only those learned parameters to predict. There's a completely different strategy: don't learn anything at training time, just remember every training example, and at prediction time ask "which training examples does this new point actually resemble?" That's the whole idea behind K-Nearest Neighbors, and it starts from a very ordinary intuition: points that sit near each other in feature space tend to share a label, so to guess a new point's label, look at what its closest neighbors are labeled.

### From theory to code

Theory below breaks this into two pieces: measuring how far a query point is from every training point, and turning a handful of nearest labels into one prediction. `pairwise_distances` computes the first (every query-to-sample Euclidean distance, all at once); `knn_predict` uses it to find each query's `k` nearest training points and takes a majority vote among their labels.

### Constraints

- `pairwise_distances(input, queries)`: `input` has shape `(n_samples, n_features)`, `queries` has shape `(n_queries, n_features)`, output has shape `(n_queries, n_samples)` — Euclidean distance from every query to every training point.
- One vectorized expression for `pairwise_distances`, no loop over samples or queries.
- `knn_predict(input, labels, queries, k)` returns shape `(n_queries,)`: the majority class among each query's `k` nearest neighbors.
- Ties in the vote are broken by the lower class label, same convention `01-random-forest-majority-vote` uses.
- `k` nearest means by distance rank, not by any fixed radius — always exactly `k` neighbors per query, regardless of how close or far they are.
- No training-time computation at all: `input`/`labels` are used directly at prediction time, nothing is fit or cached beyond what's passed in.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

To get every query-to-sample distance without a loop, you need a `(n_queries, n_samples, n_features)` intermediate array — one difference vector per query-sample pair. `queries[:, np.newaxis, :]` and `input[np.newaxis, :, :]` broadcast against each other into exactly that shape.

</details>

<details>
<summary>Hint 2</summary>

Once you have distances, `np.argsort` on each query's row of distances gives you neighbor indices ordered nearest-to-farthest — the first `k` columns of that are your `k` nearest neighbors' indices for every query at once.

</details>

<details>
<summary>Hint 3</summary>

For the vote itself, `np.unique(neighbor_labels, return_counts=True)` returns labels in sorted order alongside their counts. `np.argmax` on the counts returns the _first_ index achieving the maximum — since labels are already sorted ascending, a tie in counts resolves to the lower label automatically, no extra tie-breaking logic needed.

</details>

## Theory

### The simple version

Imagine trying to guess a stranger's favorite cuisine by looking at the five people standing physically closest to them at a party — not their family, not the whole room, just whoever happens to be nearby right now. If most of those five people love the same cuisine, that's your guess. There's no rule you've learned in advance about what kind of person likes what — you're just trusting that people who ended up near each other tend to share things in common, and checking that on the spot, every single time you need a guess.

### The formula

For query point `q` and training points `x_1, ..., x_n`, the Euclidean distance to each is:

```text
distance(q, x_i) = sqrt( sum_j (q_j - x_i_j)^2 )
```

computed for every query against every training point at once, producing a `(n_queries, n_samples)` distance matrix. For each query row, take the `k` smallest distances, look up those `k` training points' labels, and predict:

```text
prediction = the label value that appears most often among those k labels
```

with ties broken toward the lower label value.

```text
query point
   ↓ measure distance to every training point
k closest training points
   ↓ majority vote among their labels
prediction
```

This makes KNN "instance-based" (or "lazy"): there's no model to fit, no loss to minimize, no gradient to compute — the entire "model" is the training data itself plus this rule for using it at prediction time. The tradeoff is prediction cost: every single query has to compare itself against every training point, which doesn't scale the way a fitted `weight`/`bias` pair or even a tree does.

### How PyTorch actually implements this

`torch.cdist(queries, input)` computes exactly this pairwise Euclidean distance matrix (Euclidean is `cdist`'s default `p=2`), and `torch.topk(distances, k, largest=False)` gives the `k` nearest indices per row — the two building blocks this exercise implements by hand with `np.newaxis` broadcasting and `np.argsort`. PyTorch has no built-in "KNN classifier" module, since the majority-vote step isn't a tensor op; libraries like `scikit-learn`'s `KNeighborsClassifier` or `faiss` (for large-scale nearest-neighbor search) sit on top of this same distance-then-vote structure.

## Explanation

`pairwise_distances` computes every query-to-sample distance in one vectorized shot: `queries[:, np.newaxis, :]` has shape `(n_queries, 1, n_features)`, `input[np.newaxis, :, :]` has shape `(1, n_samples, n_features)`, and subtracting them (`diff`) broadcasts to `(n_queries, n_samples, n_features)` — one difference vector for every query-sample pair. `np.sqrt(np.sum(diff**2, axis=-1))` squares, sums over the last axis, and takes the square root, collapsing that down to `(n_queries, n_samples)`, exactly the standard Euclidean distance formula computed for every pair simultaneously (`test_pairwise_distances_matches_hand_computation`'s 3-4-5 triangle checks this directly).

`knn_predict` calls `distances = pairwise_distances(input, queries)`, then `nearest_indices = np.argsort(distances, axis=1)[:, :k]`, sorting each query's row of distances and keeping the first `k` column indices — the `k` nearest training points for that query. The `for i in range(queries.shape[0])` loop is over queries, not over samples, so it doesn't violate the "vectorize `pairwise_distances`" constraint; inside it, `labels[nearest_indices[i]]` looks up those neighbors' labels, and `values, counts = np.unique(neighbor_labels, return_counts=True)` followed by `values[np.argmax(counts)]` is the exact same majority-vote pattern `01-random-forest-majority-vote` uses — a vote among a handful of nearby labels instead of a vote among several trees' predictions, the same underlying mechanism either way. Because `np.unique` returns `values` sorted ascending, `np.argmax` picking the first count-maximizing index is what makes `test_knn_predict_ties_break_to_lower_class_label` pass without any explicit tie-breaking code.
