---
name: classification-distribution-shift-detection
title: 'Production Engineering: detecting train/serve distribution shift'
tags: [classical-ml, classification, evaluation]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`Generalization: train/val split and the generalization gap` measured whether a model generalizes from training data to a held-out set drawn from the SAME underlying distribution. A deployed model faces a harder, ongoing version of this problem: the real world doesn't hold still. User behavior shifts, a product changes, a new customer segment appears, and the LIVE data flowing into a deployed model can quietly drift away from the distribution it was trained on, degrading performance in a way that never shows up in any offline validation metric, because validation was computed before the drift ever happened.

The Population Stability Index (PSI) is the standard production-ML tool for catching this: a single number, computed continuously on live traffic, that flags when a feature's distribution has drifted meaningfully from what the model was trained to expect, before that drift necessarily shows up as a visible drop in business metrics.

### From theory to code

Theory bins both the training distribution and the live distribution using bin edges chosen from the TRAINING data's own quantiles (so training data is roughly evenly spread across bins by construction), then measures how differently the live data falls across those same bins, in a KL-divergence-like formula.

Implement `bin_proportions(values, bin_edges)` first, then `population_stability_index(train_values, live_values, num_bins=10)`, then `detect_distribution_shift(train_values, live_values, num_bins=10, threshold=0.2)`.

### Constraints

- Bin edges are derived from `train_values`' quantiles, with the outermost edges widened to `-inf`/`+inf`.
- Clip proportions away from exactly `0` before taking a log (the same reason `01-entropy`, Math & Statistics, clips).
- `detect_distribution_shift` uses the conventional threshold, `PSI > 0.2` signals a significant shift.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.quantile(train_values, np.linspace(0, 1, num_bins + 1))` gives bin edges that split the TRAINING data into roughly equal-sized buckets.

</details>

<details>
<summary>Hint 2</summary>

`np.histogram(values, bins=bin_edges)` counts how many values fall in each bin; divide by `len(values)` to get proportions.

</details>

## Theory

### The simple version

A restaurant designs its menu and staffing around its typical Tuesday-lunch crowd: mostly office workers, moderate spice preference, quick orders. Six months later, a nearby office closes and a new residential complex opens up, the crowd composition has quietly shifted, families, slower orders, different tastes, without anyone at the restaurant explicitly deciding anything changed. If nobody's tracking the CROWD COMPOSITION itself, only sales totals, the shift can go unnoticed for a long time even as it steadily degrades how well the old staffing plan actually serves the new crowd. PSI is exactly a tool for tracking "has the crowd composition itself changed," applied to a model's input features instead of restaurant customers.

### The formula

```text
bin_proportions(values, bin_edges) = fraction of values in each bin

bin_edges: chosen from TRAINING data's quantiles (num_bins equal-sized
           buckets by construction), outermost edges widened to +-inf

PSI = sum_bins( (live_pct - train_pct) * log(live_pct / train_pct) )
```

PSI has the same mathematical shape as KL divergence (`03-kl-divergence`, Math & Statistics): both measure how much one distribution diverges from another using a sum of `(difference) * log(ratio)` terms. PSI is specifically symmetrized in a way that makes it a genuinely popular, standard industry metric: values near `0` mean the distributions match closely, and the conventional interpretation bands are `PSI < 0.1` (no significant shift), `0.1 <= PSI < 0.2` (moderate shift, worth monitoring), `PSI >= 0.2` (significant shift, action likely needed).

The key practical insight PSI formalizes: model performance can degrade in production for reasons that have NOTHING to do with the model itself being wrong, the WORLD changed, and the model, trained on an earlier snapshot of that world, is now answering a slightly different question than the one it was trained for. Detecting this early, via monitoring PSI on key input features continuously, is often the difference between catching a production problem in hours versus discovering it weeks later through a slow, hard-to-diagnose decline in business metrics.

### How PyTorch actually implements this

There is no PyTorch API for this, distribution-shift monitoring is an MLOps/production-monitoring concern (`evidently`, `whylogs`, and similar open-source libraries implement PSI and related drift metrics directly, wrapped around models regardless of framework), sitting entirely downstream of training and inference. This is exactly why the question is titled "Production Engineering": the skill it builds isn't a model-architecture choice, it's operational discipline, continuously comparing live traffic against the training snapshot a model was built from, so a genuinely important class of real-world failure (the world moved, the model didn't) gets caught by a dashboard rather than by a customer complaint.

## Explanation

`bin_proportions` calls `np.histogram(values, bins=bin_edges)` and divides the resulting counts by `len(values)`.

`population_stability_index` derives bin edges from `train_values`' quantiles (widening the outer edges to `-inf`/`+inf` so no value falls outside every bin), computes both distributions' bin proportions (clipped away from `0`), and sums `(live_pct - train_pct) * log(live_pct / train_pct)` across bins.

`detect_distribution_shift` computes the PSI and compares it against `threshold`, returning `True` for a significant shift.
