---
name: dl-core-elementwise-ops
title: Elementwise ops
tags: [deep-learning, tensors]
difficulty: Beginner
---

## Statement

Implement:

```python
def add(a, b) -> np.ndarray: ...
def sub(a, b) -> np.ndarray: ...
def mul(a, b) -> np.ndarray: ...
def div(a, b) -> np.ndarray: ...
def power(a, b) -> np.ndarray: ...
```

- `div` performs TRUE division always, even between two integer arrays, never integer (floor) division.

## Theory

`torch.add`/`sub`/`mul`/`div`/`pow` (and the operators `+`/`-`/`*`/`/`/`**` that call them) apply an operation to every pair of corresponding elements, this is what "elementwise" means, as opposed to `01-hypothesis-function`'s matrix multiplication, which combines many elements together into each output value.

The one genuine gotcha here is `div`: `torch.div(a, b)` between two _integer_ tensors still returns a floating-point result, `torch.div(torch.tensor(7), torch.tensor(2))` is `3.5`, not `3`. This differs from Python's own `//` (floor division) and matters because a careless implementation using integer-only division would silently truncate results whenever both inputs happen to be integer tensors, a real, distinct class of bug from a shape mismatch or a wrong formula.

## Explanation

`add`/`sub`/`mul`/`power` are direct one-line calls to the corresponding NumPy operator, NumPy's own broadcasting and dtype-promotion rules already match what `torch`'s equivalents do for these operations.

`div` calls `np.true_divide(a, b)` explicitly rather than a bare `a / b`, guaranteeing floating-point division regardless of whether `a`/`b` are integer or float arrays, `np.true_divide` is the exact function NumPy's own `/` operator calls internally, naming it explicitly here is about being unambiguous that this is a deliberate choice, not an accident of which operator happened to be used.
