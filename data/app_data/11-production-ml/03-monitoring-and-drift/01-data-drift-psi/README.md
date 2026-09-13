---
name: production-ml-data-drift-psi
title: 'Data Drift: The Input Distribution Shifting After Deployment'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`06-ab-testing-rollback` compares two MODELS against a fixed traffic source. But the world a deployed model sees keeps changing on its own, independent of any model change at all: customer demographics shift, a new product launch changes typical purchase amounts, a sensor gets recalibrated. Data drift is exactly this — the INPUT distribution a model sees in production drifting away from the distribution it was trained on — and it needs its own real, quantifiable detection metric, separate from anything about model accuracy.

### From theory to code

Implement `bin_distribution` (turning raw samples into a normalized histogram) and `population_stability_index` (PSI), the standard industry metric for quantifying distribution shift, plus `detect_data_drift`.

### Constraints

- `bin_distribution(samples, bin_edges)` returns a normalized histogram summing to `1.0`, with any empty bin's zero count replaced by a tiny floor value (`1e-6`) before normalizing.
- `population_stability_index(expected, actual)` returns `sum((actual - expected) * ln(actual / expected))` over two ALREADY-NORMALIZED distributions.
- `detect_data_drift(psi_value, threshold=0.2)` is a plain threshold comparison.
- PSI must be near `0` for two samples drawn from the SAME true distribution, regardless of sample size, and large for a genuinely shifted distribution.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

PSI's formula has the exact same SHAPE as a KL-divergence-style comparison (`math-kl-divergence`) — a weighted sum of log-ratios between two distributions — but PSI specifically uses `(actual - expected)` as the weight instead of just `actual` or `expected` alone, which is what makes it symmetric in a way plain KL divergence isn't.

</details>

<details>
<summary>Hint 2</summary>

The floor value in `bin_distribution` matters more than it looks: without it, any bin that happens to get zero samples in EITHER distribution makes `ln(actual/expected)` blow up to `+/-infinity`, silently corrupting the whole PSI computation.

</details>

## Theory

### The simple version

Imagine a store owner who carefully recorded exactly how many customers arrived in every hour-long slot last month (the "expected" distribution), then compares that against today's hourly arrival counts (the "actual" distribution) — if today looks basically like a typical day, the two hourly patterns line up closely; if a nearby event just let out and suddenly everyone arrives between 5-6pm instead of being spread out, the two patterns diverge sharply. PSI is exactly this kind of bucket-by-bucket comparison, turned into one number: the bigger the number, the more the "shape" of the input distribution has changed.

### The formula

```text
bin_distribution(samples, edges):
    counts = histogram(samples, edges)
    counts[counts == 0] = 1e-6      -- avoid log(0)
    return counts / counts.sum()

population_stability_index(expected, actual) = sum( (actual_i - expected_i) * ln(actual_i / expected_i) )

detect_data_drift(psi, threshold=0.2) = psi > threshold
```

PSI's real, industry-standard interpretation scale: below ~0.1 means no meaningful shift, 0.1-0.25 a moderate shift worth watching, above ~0.25 a significant shift worth investigating — this exercise's `detect_data_drift` exposes a single configurable threshold rather than the full three-tier scale, but the underlying PSI computation is the exact, real formula used in practice.

### How PyTorch actually implements this

Context only, untested by your submission: PSI is a long-standing, widely-used metric in credit scoring and production ML monitoring specifically because it's simple, interpretable, and doesn't require any assumption about the underlying distribution's shape — real ML monitoring platforms (Evidently AI, WhyLabs, Arize) compute exactly this metric (alongside others like the Kolmogorov-Smirnov statistic) as a standard, automated data-drift check on every feature a deployed model consumes.

## Explanation

`bin_distribution` converts raw samples into a proper probability distribution over fixed bins, with the small floor value specifically preventing a genuinely empty bin from corrupting the later log computation — `tests.py` confirms the result always sums to `1.0` and contains only finite values, even for a heavily-concentrated sample set that leaves most bins empty.

`population_stability_index` implements the real formula directly — `tests.py` confirms it's near-zero for two samples drawn from the identical true distribution (regardless of how different their SAMPLE SIZES are, a direct check that the metric depends on distribution SHAPE, not raw counts), grows with the magnitude of an actual shift, and correctly reduces to exactly `0` for two literally identical (already-normalized) input arrays.

`detect_data_drift` is the final, practical threshold decision — `tests.py` confirms the boundary behaves as documented (exclusive, `>` not `>=`), tying the whole exercise to a concrete, actionable yes/no monitoring alert.
