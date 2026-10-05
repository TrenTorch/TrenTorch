---
name: problem-120-xavier-initialization
title: 'Xavier Initialization'
tags: [problemset, dl-core, weight-initialization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'weight initialization'
hint: 'bound=sqrt(6/(fan_in+fan_out))'
tools: [NumPy]
---

## Statement

120 Xavier Initialization. Generate a (fan_in, fan_out) array using Xavier/Glorot uniform initialization and a NumPy default_rng seeded by seed. Sample uniformly from [−a,a], where a=sqrt(6/(fan_in+fan_out)).

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
[[0.2740704356, 0.8702518358, 0.6039970853], [-0.6020408827, -0.437813734, 0.8184145939]]
```

**Example 2**

**Input**

```python
solve(fan_in=1, fan_out=1, seed=0)
```

**Output**

```python
[[0.4744492023]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Xavier uniform initialization sets a scale based on both incoming and outgoing fan counts to help preserve activation variance across layers.

## Explanation

Compute the symmetric bound, instantiate a seeded NumPy generator, and draw the requested matrix uniformly within that bound.
