---
name: problem-120-xavier-initialization
title: Xavier Initialization
tags: [dl-core, case-study, hard, weight-initialization., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(fan_in, fan_out, seed=0)`. Generate weights using Xavier uniform initialization. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Cloudflare is scenario context only; this is not an official Cloudflare interview question or endorsement.

### Example 1

**Input**

```python
solve(2, 3, 4)
```

**Output**

```text
[[0.9706872930495041, 0.024817424791027998, 1.0433976819438455], [-0.9183422600237403, 0.23520484345365023, -0.2706043355643152]]
```

**Explanation.** Generate weights using Xavier uniform initialization.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[0.9706872930495041, 0.024817424791027998, 1.0433976819438455], [-0.9183422600237403, 0.23520484345365023, -0.2706043355643152]]
```

### Hint

bound=sqrt(6/(fan_in+fan_out))

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Xavier Initialization?

Generate weights using Xavier uniform initialization. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Xavier Initialization supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **bound=sqrt(6/(fan_in+fan_out))**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `rng.uniform(-a, a, (fan_in, fan_out))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(2,3,4)` returns `[[0.9706872930495041, 0.024817424791027998, 1.0433976819438455], [-0.9183422600237403, 0.23520484345365023, -0.2706043355643152]]`. Reversing its observation rows returns `[[0.9706872930495041, 0.024817424791027998, 1.0433976819438455], [-0.9183422600237403, 0.23520484345365023, -0.2706043355643152]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.random.default_rng`, `np.sqrt`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `rng.uniform(-a, a, (fan_in, fan_out))` after preparing the intermediates for Xavier Initialization. `np.random.default_rng`, `np.sqrt` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
