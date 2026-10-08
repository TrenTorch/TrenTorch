---
name: problem-108-isolation-path-length
title: 'Isolation Path Length'
tags: [problemset, unsupervised-ml, anomaly-detection]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'anomaly detection'
hint: 'loop: split = rng.uniform(lo, hi); depth += 1; keep the side containing x'
tools: [NumPy]
---

## Statement

Compute the path length of a point in one random isolation 'tree' (as used by Isolation Forest). Start with the interval `[lo, hi]`; repeatedly draw a random split uniformly inside it with `rng.uniform(lo, hi)`, count one level, and keep the side containing `x` (`x <= split` keeps the left side). Stop when the interval is empty (`lo >= hi`) or after `max_depth` splits.

Implement `solve(x, lo, hi, max_depth, rng)`.

**Returns.** Return the number of splits performed as an `int`. `rng` is a `numpy.random.Generator`.

### Examples

**Example 1**

Input:

```python
solve(3.0, 0.0, 10.0, 5, np.random.default_rng(0))
```

Output:

```text
5
```

**Example 2**

Input:

```python
solve(0.0, 5.0, 5.0, 10, np.random.default_rng(1))
```

Output:

```text
0
```

## Theory

### The simple version

Anomalies are easy to isolate: a point far from the others gets separated from them by only a few random cuts, while a point inside a dense group needs many. Isolation Forest scores points by how short their average path to isolation is.

### The process

Repeat: pick a random cut inside the current range, keep the side containing the point, and count one step. The step count is the path length; averaging it over many random trees gives the anomaly score.

### Why it matters

- Isolation Forest finds anomalies as points that random splits separate quickly.
- A short path means "easy to isolate", so a likely anomaly.

### How it works

1. Pick a random split inside the current interval.
2. Keep the side containing the point and count one step.
3. Stop when the interval is empty or the depth cap is reached.

### Worked example

Starting from $[0,10]$ with $x=3$ and a seeded generator, the loop splits $5$ times (the depth cap) without the interval collapsing, so the path length is 5. A point far from the others would typically be isolated in fewer steps.

## Explanation

Because the splits are random, the result is a random variable; only with a seeded generator is it reproducible. The loop ends early if the interval collapses (the second example starts with `lo == hi`, so the path length is $0$). The depth cap bounds the work for points that are hard to isolate.
