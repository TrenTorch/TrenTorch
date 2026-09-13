---
name: systems-perf-fp16-bf16-representable-range
title: FP16/BF16 Representable Range vs FP32, Why Naive FP16 Training Underflows
tags: [mlops, neural-networks, mixed-precision]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`03-memory-footprint-estimation` and `01-quantize-float32-to-int8` both treated reduced precision as purely a storage question. Training in reduced precision is a different, sharper problem: gradients during real training routinely take on very small values (a well-trained network's gradients often shrink to `1e-6` or smaller as the loss flattens out) — and unlike `int8`'s wide, evenly-spaced quantization range, `float16` has a _hard floor_ below which numbers don't round imprecisely, they vanish to exactly zero.

### From theory to code

Implement `cast_to_dtype(x, dtype)`, a real (not simulated) cast using NumPy's own dtype system, `detect_underflow(original, casted)`, which flags every value that vanished entirely, and `detect_overflow(casted)`, which flags every value that blew past the narrower dtype's representable maximum.

### Constraints

- `cast_to_dtype(x, dtype)`: `dtype` is `"float16"` or `"float32"`.
- `detect_underflow(original, casted)`: `True` only where `original` was genuinely nonzero AND `casted` rounded all the way to exactly `0.0` — a value that was already `0.0` doesn't count as "lost."
- `detect_overflow(casted)`: `True` wherever a value is `+inf` or `-inf` (only possible after casting _down_ to a narrower dtype).
- Both mask functions return boolean arrays matching their input's shape.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`x.astype(dtype)` is NumPy's real cast — no need to reimplement IEEE-754 rounding by hand, NumPy's `float16` already is genuine 16-bit half precision.

</details>

<details>
<summary>Hint 2</summary>

"Lost to underflow" needs both halves of the condition: the original value must have been nonzero (otherwise casting `0.0` to `0.0` would incorrectly count as a loss), and the casted value must be exactly `0.0`.

</details>

## Theory

### The simple version

`float32` and `float16` don't just differ in "how many decimal digits" they can represent — they differ in how far their exponent can stretch. `float16`'s exponent runs out of room around `6e-5` (its smallest _normal_ number) and `6e-8` (its smallest representable number at all, in the "subnormal" range) — anything smaller than that isn't rounded imprecisely, it's rounded straight down to exactly `0.0`, an actual, silent loss of a real value, not just reduced precision. On the other end, `float16` overflows to `+inf`/`-inf` past about `65504` — a value `float32` would represent completely comfortably.

### The formula

```text
cast_to_dtype(x, dtype)        = x.astype(dtype)
detect_underflow(orig, casted) = (orig != 0) & (casted == 0)
detect_overflow(casted)        = isinf(casted)
```

`bfloat16` (Google's "brain float," widely used for training) takes the opposite tradeoff from `float16`: it keeps `float32`'s full exponent range (so it never underflows or overflows anywhere `float32` wouldn't), at the cost of far fewer precision bits than `float16` — a genuinely different design point for the same 16-bit budget. This exercise sticks to `float16`/`float32` since NumPy has no native `bfloat16` dtype to cast to directly.

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch's `torch.float16` is bit-for-bit the same IEEE-754 binary16 format NumPy's `float16` already implements — verified directly in this exercise's own `tests.py`, whose oracle test checks NumPy's `float16` boundary values (`tiny`, `smallest_subnormal`, `max`) against the identical numbers `torch.finfo(torch.float16)` reports. This is exactly why naive `float16` training can silently fail partway through: a small-but-real gradient underflowing to `0.0` means that parameter simply stops updating, with no error or warning — the entire motivation for `02-loss-scaling`'s fix.

## Explanation

`cast_to_dtype` is `x.astype(dtype)` directly — NumPy's own cast already implements real IEEE-754 rounding-to-nearest behavior for every value, including the underflow-to-zero and overflow-to-infinity edge cases this exercise studies.

`detect_underflow` combines two elementwise conditions with `&`: `original != 0` (this value genuinely carried real information) and `casted == 0` (that information is now completely gone) — a value that was already exactly `0.0` before casting is correctly excluded, since nothing was lost there.

`detect_overflow` is `np.isinf(casted)` directly — NumPy represents an out-of-range cast as `inf`/`-inf` rather than raising an error, so checking for infinity is exactly checking "did this value overflow the target dtype's range."
