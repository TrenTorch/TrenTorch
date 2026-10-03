---
name: lm-activation-patching
title: Activation Patching
tags: [interpretability, causal-intervention, circuits]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A probe shows that information is _present_; it does not show the model _uses_ it. To test causal importance we intervene. Run the model on a clean prompt where it answers correctly and on a corrupted prompt where it answers wrongly. Then rerun the corrupted prompt but **patch in** one activation copied from the clean run. If that single patch restores the correct behavior, the activation carries information the answer depends on. Scanning every position or component gives a map of where the computation happens. Results are reported as a **recovery fraction**: 0 means the patch changed nothing and 1 means it fully restored the clean behavior.

### From theory to code

Implement `patch_rows`, `recovery` and `patching_scan`.

### Constraints

- `patch_rows(clean, corrupt, rows)` returns a copy of the corrupted activations `corrupt` (shape `(T, d)`) with the listed rows replaced by the same rows of `clean`.
- `recovery(clean_metric, corrupt_metric, patched_metric)` is `(patched - corrupt) / (clean - corrupt)`.
- `patching_scan(model, clean, corrupt)` calls `model(acts)` (a function from a `(T, d)` array to a scalar metric such as a logit difference) once on the clean activations and once on the corrupted ones, then once per position `t` with only row `t` patched. It returns the array of recovery fractions, one per position.
- Do not modify `clean` or `corrupt`.

### Hints

<details>
<summary>Hint 1</summary>

The scan is a loop over positions that reuses `patch_rows` and `recovery`.

</details>

<details>
<summary>Hint 2</summary>

Compute the clean and corrupted metrics once, outside the loop.

</details>

## Theory

### The simple version

It is like swapping a single part between a working engine and a broken one. If the engine starts after one swap, that part was the fault. Swapping every part one at a time maps out which ones matter.

### The formula

$$
\text{recovery}(t) = \frac{m(\text{corrupt with row } t \leftarrow \text{clean}) - m(\text{corrupt})}{m(\text{clean}) - m(\text{corrupt})}
$$

For a metric that is linear in the activations, the recovery of patching row $t$ equals that row's share of the total clean-minus-corrupt difference, so the recoveries over all positions sum to $1$.

### How this is done in practice

TransformerLens and nnsight provide hooks that implement patching at any layer, head or position, and path patching extends it to edges between components. The metric is usually the logit difference between the correct and the incorrect answer token, which is the quantity the next question decomposes.

## Explanation

The scan is a causal experiment run in a loop. The recovery normalization makes scans comparable across prompts, and the linearity property in the tests gives a clean mathematical check on the implementation.
