---
name: math-set-and-function-notation
title: 'Set and Function Notation Used in ML Papers'
tags: [notation, foundations]
difficulty: Beginner
---

## Statement

### The problem, from first principles

ML papers write things like `f: ℝⁿ → ℝᵐ`, `x ∈ ℝⁿ`, `A ⊆ B`, and `argmax_i f(i)` constantly, without ever pausing to define them — they're assumed background, the same way `for` and `if` are assumed background in code. This question makes the two most operationally useful pieces concrete: **`⊆`** (subset), which shows up in "is this a valid choice from the allowed set," and **`argmax`**, which shows up everywhere a model has to pick the single best option out of many (classification's predicted class, a search algorithm's best move, a language model's next token under greedy decoding).

### From theory to code

Implement `is_subset(a, b)`, checking whether every element of set `a` is also in set `b`, then `argmax(values)`, returning the **index** of the largest value. The signatures and docstrings are already in the editor.

### Constraints

- `a` and `b` are Python `set` objects for `is_subset`.
- `values` is a non-empty list or tuple of numbers for `argmax`.
- If more than one value is tied for the maximum, return the **first** such index (matching NumPy's `np.argmax` convention).

### Hints

<details>
<summary>Hint 1</summary>

`is_subset(a, b)` is one line using Python's own set operations — no explicit loop needed, though writing the loop version once is worth doing mentally to see what the operator is actually checking.

</details>

<details>
<summary>Hint 2</summary>

For `argmax`, track both the best value seen so far and its index as you scan once through `values`; only update when you find something **strictly** greater, which is exactly what keeps the first tied index instead of the last.

</details>

## Theory

### The simple version

`x ∈ ℝⁿ` reads "`x` is a member of `ℝⁿ`" — `x` is a vector of `n` real numbers. `A ⊆ B` reads "`A` is a subset of `B`" — every element of `A` is also in `B` (note `A` itself can equal `B`; **strict** subset, "`A` is a subset of `B` but not equal to it," is written `A ⊂ B`). `f: ℝⁿ → ℝᵐ` reads "`f` maps an `n`-dimensional real vector to an `m`-dimensional real vector" — the same idea as a Python type hint (`def f(x: np.ndarray) -> np.ndarray`), just written in math notation instead of code. `argmax_i f(i)` reads "the value of `i` that makes `f(i)` largest" — not the maximum value itself (that would be written `max_i f(i)`), but **which index achieves it**.

### The formula

$$
\text{argmax}_i \; f(i) = i^* \quad \text{such that} \quad f(i^*) \geq f(i) \; \text{ for all } i
$$

- `argmax` — "the argument that maximizes," returning the input (here, the index `i`) that produces the largest output, not the output itself.
- `s.t.` — shorthand for "such that," introducing a condition the preceding statement must satisfy.
- `∀` — "for all" (as used above, spelled out); appears constantly in formal definitions to say a condition holds across an entire set rather than for one specific element.

### Where this shows up

- **Classification**: a model outputs a probability for every class; the predicted label is `argmax_c p(c | x)` — "whichever class the model assigns the highest probability to."
- **Greedy decoding**: a language model outputs a probability for every possible next token; greedy decoding picks `argmax_t p(t | \text{context})` at each step.
- **Constrained optimization** (`05-numerical-computation`'s Lagrange multipliers question): problems are written `maximize f(x) \; \text{s.t.} \; g(x) = 0` — "find the input maximizing `f`, subject to the constraint that `g(x)` equals zero."

### How code actually implements this

`np.argmax(arr)` and `torch.argmax(tensor)` both implement exactly this operation, and both follow the same first-tie-wins convention this question's `argmax` does. Reading a paper's `argmax_i f(i)` and immediately recognizing it as "there's an `np.argmax` call hiding in this formula" is the entire point of this question.

## Explanation

`is_subset(a, b)` returns `a.issubset(b)` (equivalently `a <= b`), directly using Python's own set semantics to answer exactly the question `⊆` asks: is every element of `a` also present in `b`. `argmax` tracks `best_index` and `best_value` while scanning `values` once, updating both only when a **strictly** larger value is found — using `>` rather than `>=` for the comparison is precisely what keeps the first occurrence of a tied maximum instead of the last, matching `np.argmax`'s documented tie-breaking behavior.
