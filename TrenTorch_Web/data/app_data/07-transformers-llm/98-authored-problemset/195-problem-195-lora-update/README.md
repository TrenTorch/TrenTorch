---
name: problem-195-lora-update
title: "LoRA Update"
tags: [problemset, transformer-llm, fine-tuning-and-peft]
difficulty: Beginner
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "fine tuning and PEFT"
hint: "apply A to x then B to the result"
tools: [NumPy]
---

## Statement

Compute low-rank update B @ (A @ x); return the update only.

Signature: `def solve(x, A, B)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve(np.array([1.0, 2.0]), np.array([[1.0, 0.0], [0.0, 1.0]]), np.array([[2.0, 1.0], [0.0, 3.0]]))
```

Returns:

```python
[4.0, 6.0]
```

### Example 2

```python
solve(np.array([0.0, 0.0]), np.array([[1.0, 1.0]]), np.array([[2.0], [3.0]]))
```

Returns:

```python
[0.0, 0.0]
```

## Theory

A projects x into rank space and B maps it into output space; no residual or scaling is added.

## Explanation

Compute low-rank update B @ (A @ x); return the update only. The examples show concrete inputs and expected returned values.
