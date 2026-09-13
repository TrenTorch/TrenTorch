---
name: dl-core-tensor-creation-dtype
title: Tensor creation / dtype
tags: [deep-learning, tensors, dtype]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every question from here on builds tensors, autograd, and neural networks on top of NumPy, mirroring real PyTorch's own API surface (`torch` itself is never imported, the same fidelity discipline `01-classical-ml`'s `linear` held to when it mirrored `torch.nn.functional.linear` exactly). Before any of that can work, the most basic operation of all, "make an array," has to actually produce the same numbers a real PyTorch program would.

That sounds trivial until you notice NumPy and PyTorch quietly disagree about it. Ask NumPy for an array of floats and it hands you `float64`. Ask PyTorch the same thing and you get `float32`. If tensor-creation helpers here silently kept NumPy's own default, every later question's numbers would be technically different from what real PyTorch produces, small precision differences that compound across a training loop. Getting this one gotcha right up front is what lets everything built afterward be trusted.

### From theory to code

Implement four creation helpers, `make_tensor`, `zeros`, `ones`, `arange`, each mirroring its `torch.*` namesake. The core idea from Theory, PyTorch overrides floating-point defaults to `float32` but leaves integer/boolean inference alone, applies identically in all four; `make_tensor` and `arange` need to inspect an inferred dtype to decide whether to override it, `zeros`/`ones` don't need any inference at all since their own `dtype` parameter already defaults to the right value.

### Constraints

- `make_tensor(data, dtype=None)`: infer from `data` like `np.array` would, unless `dtype` is given explicitly.
- If no `dtype` is given and the inferred dtype is floating-point, use `float32`, never NumPy's own `float64` default.
- If no `dtype` is given and the inferred dtype is integer or boolean, keep NumPy's own inference unchanged.
- `zeros(shape, dtype=np.float32)` / `ones(shape, dtype=np.float32)`: default dtype is `float32`, matching `torch.zeros`/`torch.ones`, not NumPy's own `np.zeros`/`np.ones` defaults.
- `arange(start, stop, step=1, dtype=None)`: same float32-override rule as `make_tensor`, applied to `np.arange`'s own inferred dtype.
- An explicit `dtype` argument always wins over any inference, in all four functions.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.issubdtype(array.dtype, np.floating)` answers "did NumPy infer a floating type," regardless of whether that's `float32`, `float64`, or something else. That's the check you need before deciding whether to override.

</details>

<details>
<summary>Hint 2</summary>

Both `make_tensor` and `arange` follow the exact same shape: compute the array first with NumPy's own rules (`np.array(data)` or `np.arange(start, stop, step)`), then apply one shared decision — explicit dtype wins, otherwise override only if floating, otherwise leave untouched.

</details>

## Theory

### The simple version

Think of dtype inference as two different librarians filing the same book. NumPy's librarian defaults to the most precise shelf available for a decimal number, `float64`. PyTorch's librarian knows most deep learning work doesn't need that much precision, and that the smaller shelf, `float32`, is faster and uses half the memory, especially on a GPU, so it files decimals there by default instead. Both librarians agree on where whole numbers and true/false values go, that part was never in dispute.

### The formula

```text
make_tensor(data, dtype=None):
    array = np.array(data)
    if dtype given:       return array.astype(dtype)
    if array is floating: return array.astype(float32)
    else:                 return array   # int/bool unchanged

zeros(shape, dtype=float32):  np.zeros(shape, dtype=dtype)
ones(shape, dtype=float32):   np.ones(shape, dtype=dtype)

arange(start, stop, step=1, dtype=None):
    result = np.arange(start, stop, step)
    if dtype given:         return result.astype(dtype)
    if result is floating:  return result.astype(float32)
    else:                   return result
```

### How PyTorch actually implements this

`torch.tensor(data)` and `torch.arange(start, stop)` both use `torch.get_default_dtype()` (`float32` unless changed globally) whenever no explicit `dtype` is passed and the inferred data is floating-point; integer and boolean inputs infer `int64`/`bool` the same way NumPy does. This is context only, no PyTorch code runs anywhere in this repo, `tests.py` doesn't bake in any PyTorch-generated reference numbers for this question, so nothing here is a numeric claim about real PyTorch beyond this general dtype rule.

## Explanation

`make_tensor` calls `np.array(data)` first to let NumPy do its normal type inference, then applies PyTorch's actual rule on top: if an explicit `dtype` was given, cast to it directly (`array.astype(dtype)`), no further inference needed. Otherwise it checks `np.issubdtype(array.dtype, np.floating)`; if NumPy inferred a floating type, it overrides to `float32` specifically, not just "whatever NumPy picked." Integer or boolean data passes through with NumPy's own inferred dtype unchanged, since that already matches PyTorch's behavior — this is exactly what `test_make_tensor_int_data_keeps_numpy_inferred_dtype` checks.

`zeros`/`ones` default their own `dtype` parameter to `np.float32` directly, a one-line call to `np.zeros`/`np.ones` with that default already produces the right behavior, there's no ambiguous input dtype to infer from when only a shape is given.

`arange` calls `np.arange(start, stop, step)` first, then applies the exact same float32-override rule `make_tensor` uses: `arange(0, 5)` (integer bounds) keeps NumPy's integer inference, but `arange(0.0, 5.0)` (float bounds) overrides to `float32`, not NumPy's default `float64` — the distinction `test_arange_with_float_bounds_defaults_to_float32` and `test_arange_with_int_bounds_keeps_integer_dtype` both verify.
