---
name: math-stratified-sampling
title: Stratified sampling for an imbalanced dataset
tags: [data-processing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A fraud-detection dataset with 95% legitimate transactions and 5% fraudulent ones has a real trap waiting inside it: draw a plain random sample of 20 rows, and there's a meaningful chance you get ZERO fraud examples at all, purely by bad luck, even though fraud makes up a real, nontrivial fifth of every 100 rows. A model, or an evaluation set, built from that unlucky sample would be blind to the exact class it's supposed to detect.

Stratified sampling fixes this directly: instead of sampling from the whole dataset at once, sample from EACH class separately, in proportion to that class's true share of the data. The result is a smaller sample that still faithfully reflects the original class balance, no matter how rare the minority class is or how unlucky a plain random draw might have been.

### From theory to code

Theory computes each class's true proportion of the full dataset first, then draws from each class separately, sized to match that same proportion, so the resulting sample's class balance mirrors the original.

Implement `class_proportions(labels)` first, then `stratified_sample_indices(labels, sample_size, seed=None)` on top of it.

### Constraints

- `class_proportions` returns a dict, `{label: fraction}`, fractions summing to `1.0`.
- `stratified_sample_indices` samples WITHOUT replacement within each class.
- The returned array holds INDICES into `labels`, not the label values themselves.
- Same `seed` must produce the same sample (reproducibility, `01-sampling-estimating-distribution`'s own convention).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.unique(labels, return_counts=True)` gives you both the distinct labels and how many of each there are, in one call.

</details>

<details>
<summary>Hint 2</summary>

For each class, `round(proportion * sample_size)` gives roughly how many samples to draw from that class specifically, then `rng.choice(class_indices, size=that_count, replace=False)`.

</details>

## Theory

### The simple version

Imagine a bag with 95 white marbles and 5 red ones, thoroughly mixed. Grab a random handful of 20, and it's entirely possible you get zero red marbles, purely by chance, even though red marbles are a real, meaningful fraction of the bag. Stratified sampling instead treats the two colors as separate pools: grab roughly `20 * 0.95 = 19` white marbles from the white pool, and `20 * 0.05 = 1` red marble from the red pool. The resulting handful, by construction, reflects the bag's true color balance, no luck required.

### The formula

```text
class_proportions(labels)[c] = count(labels == c) / len(labels)

for each class c:
    n_from_class = round(class_proportions(labels)[c] * sample_size)
    sample n_from_class indices from that class, without replacement

stratified_sample = concatenation of all per-class samples
```

The key guarantee: the SAMPLE's class balance matches the FULL DATASET's class balance, by construction, not by chance. This matters most exactly when it would otherwise fail most badly, a severely imbalanced dataset, where a plain random sample has a real, nontrivial chance of badly under-representing (or entirely missing) the minority class.

This connects directly to `07-evaluation/13-model-selection-class-imbalance` (Classical ML), whose `stratified_k_fold_split` applies exactly this same idea to cross-validation folds: every fold needs to preserve the true class balance, or a model evaluated on an accidentally class-skewed fold gets a systematically misleading performance estimate.

### How PyTorch actually implements this

`sklearn.model_selection.train_test_split(..., stratify=labels)` and `StratifiedKFold` both implement exactly this algorithm as a reusable, well-tested utility, used constantly whenever a dataset has any meaningful class imbalance (which is most real classification datasets, fraud detection, rare disease diagnosis, defect detection, all skew heavily toward the "nothing interesting happened" class). `torch.utils.data.WeightedRandomSampler` addresses a RELATED but distinct problem at training time (not evaluation-set construction): rather than stratifying a fixed sample once, it reweights how often each example is drawn DURING training, so a model sees minority-class examples more often than their raw frequency would otherwise produce, directly combating a model's natural tendency to mostly ignore a rare class it barely ever encounters.

## Explanation

`class_proportions` calls `np.unique(labels, return_counts=True)` to get every distinct label and its count in one pass, then divides each count by `len(labels)`, returning a `{label: fraction}` dict.

`stratified_sample_indices` computes those proportions, then for each class, finds that class's indices (`np.where(labels == label)`), computes how many to draw (`round(proportion * sample_size)`, capped at the class's own size), and draws that many via `rng.choice(..., replace=False)`, concatenating every class's chosen indices into the final result.
