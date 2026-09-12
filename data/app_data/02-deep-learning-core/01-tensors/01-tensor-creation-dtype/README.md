---
name: dl-core-tensor-creation-dtype
title: Tensor creation / dtype
tags: [deep-learning, tensors, dtype]
difficulty: Beginner
---

## Statement

Implement:

```python
def make_tensor(data, dtype=None) -> np.ndarray: ...
def zeros(shape, dtype=np.float32) -> np.ndarray: ...
def ones(shape, dtype=np.float32) -> np.ndarray: ...
def arange(start, stop, step=1, dtype=None) -> np.ndarray: ...
```

- Mirror `torch.tensor`/`torch.zeros`/`torch.ones`/`torch.arange`'s actual dtype behavior, not NumPy's own defaults, they genuinely differ.

## Theory

This is the start of a new section: everything from here on builds toward tensors, autograd, and neural networks, mirroring real PyTorch's own API surface (still implemented in NumPy, `torch` itself is never imported), the same fidelity discipline the classical ML section held to (`01-classical-ml`'s `linear` mirroring `torch.nn.functional.linear` exactly).

The very first gotcha: **NumPy and PyTorch pick different default float dtypes.** `np.array([1.0, 2.0]).dtype` is `float64` (NumPy's default), but `torch.tensor([1.0, 2.0]).dtype` is `float32` (PyTorch's default, chosen because most deep learning doesn't need double precision, and float32 uses half the memory and is faster on GPU). Building tensor-creation helpers that silently keep NumPy's `float64` default would make every later question's numbers technically different from what real PyTorch would produce, small differences in floating-point precision that compound across a real training loop.

Integers and booleans aren't affected by this rule, `torch.tensor([1, 2, 3]).dtype` is `int64`, matching NumPy's own default int inference, PyTorch's float-only override exists specifically because float32-vs-float64 is the practically significant case.

## Explanation

`make_tensor` calls `np.array(data)` first to let NumPy do its normal type inference, then applies PyTorch's actual rule on top: if an explicit `dtype` was given, cast to it directly, no further inference needed. Otherwise, check `np.issubdtype(array.dtype, np.floating)`, if NumPy inferred a floating type, override it to `float32` specifically (not just "whatever NumPy picked"). Integer or boolean data passes through with NumPy's own inferred dtype unchanged, since that already matches PyTorch's behavior.

`zeros`/`ones` default their own `dtype` parameter to `np.float32` directly (PyTorch's real default), a one-line call to `np.zeros`/`np.ones` with that default already produces the right behavior without needing `make_tensor`'s inference logic, there's no ambiguous input dtype to infer from when the shape alone is given.

`arange` calls `np.arange(start, stop, step)` first, then applies the exact same float32-override rule `make_tensor` uses, `torch.arange(0, 5)` (integer bounds) gives `int64`, but `torch.arange(0.0, 5.0)` (float bounds) gives `float32`, not NumPy's default `float64`.
