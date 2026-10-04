---
name: problem-121-he-initialization
title: "He Initialization"
tags: [problemset, dl-core, weight-initialization]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "weight initialization"
hint: "std=sqrt(2/fan_in)"
tools: [NumPy]
---

## Statement

121 He Initialization. Generate a (fan_in, fan_out) array using He normal initialization and a NumPy default_rng seeded by seed. Sample from a normal distribution with mean 0 and standard deviation sqrt(2/fan_in).

### Function signature

```python
solve(fan_in, fan_out, seed=0)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(fan_in=2, fan_out=3, seed=7)
```

**Output**

```python
[[0.0012301534, 0.2987455375, -0.2741378554], [-0.8905918388, -0.4546707852, -0.991646555]]
```

**Example 2**

**Input**

```python
solve(fan_in=1, fan_out=2, seed=0)
```

**Output**

```python
[[0.1778093839, -0.1868244893]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

He initialization scales variance by the number of input connections and is suited to layers using ReLU-like activations.

## Explanation

Use a seeded generator for reproducibility and draw the requested shape with standard deviation sqrt(2/fan_in).
