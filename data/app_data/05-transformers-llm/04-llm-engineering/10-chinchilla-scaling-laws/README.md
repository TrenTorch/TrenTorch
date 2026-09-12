---
name: txf-llmeng-chinchilla-scaling-laws
title: 'Compute-optimal training: Chinchilla-style scaling laws'
tags: [transformers, nlp]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Training a large language model costs a roughly fixed, known amount of COMPUTE (measured in total floating-point operations, FLOPs), and that budget has to be SPLIT between two competing uses: making the model itself BIGGER (`N`, the parameter count) or training it on MORE data (`D`, the number of tokens seen). Kaplan et al. (2020, OpenAI's original scaling laws paper) initially suggested favoring bigger models; Hoffmann et al. (2022, DeepMind, "Chinchilla") revisited this far more carefully and found the earlier guidance had been systematically under-training models relative to their size. Chinchilla's headline finding: for a FIXED compute budget, loss is minimized when model size and training data are scaled roughly EQUALLY, both proportional to the SQUARE ROOT of the compute budget, not favoring one over the other. This directly motivated a real, visible shift in how the field trains models: Chinchilla itself, at `70B` parameters trained on `1.4T` tokens, OUTPERFORMED the much larger `280B`-parameter Gopher, trained on far fewer tokens for the SAME compute budget, purely by reallocating that same budget toward more data instead of more parameters.

### From theory to code

Implement `flops_for_training(num_params, num_tokens)`, the standard `6*N*D` compute approximation, and `chinchilla_optimal_allocation(compute_budget_flops)`, returning the compute-optimal `(N, D)` split for a given budget: both proportional to `sqrt(compute_budget_flops / 6)`.

### Constraints

- `flops_for_training(N, D) = 6 * N * D`: this is a widely-used APPROXIMATION (one forward pass costs roughly `2N` FLOPs per token, and a full forward-plus-backward pass costs roughly `3x` that, `2N + 4N = 6N`), not an exact count.
- `chinchilla_optimal_allocation` returns EQUAL values for `N` and `D` (Chinchilla's simplified headline finding: roughly `N ≈ D` at the optimum, in appropriately-scaled units), specifically `sqrt(compute_budget_flops / 6)` for both.
- The chosen `(N, D)` must satisfy `flops_for_training(N, D) == compute_budget_flops` EXACTLY (the whole budget gets allocated, none wasted, none exceeded).
- Doubling the compute budget scales BOTH `N` and `D` by `sqrt(2)` (not by `2`, and not by different amounts for each).

### Hints

<details>
<summary>Hint 1: The compute formula</summary>

`return 6.0 * num_params * num_tokens`. A direct, standard approximation, not an approximation this question needs to derive from scratch.

</details>

<details>
<summary>Hint 2: Solving for the optimal split</summary>

Given `C = 6*N*D` and the constraint `N == D` (Chinchilla's simplified equal-scaling finding), substitute: `C = 6*N*N = 6*N^2`, so `N = sqrt(C / 6)`. `D` is the same value, by the `N == D` constraint.

</details>

## Theory

### The simple version

A fixed budget for building and stocking a library: spend it entirely on more SHELVES (bigger model, `N`), entirely on more BOOKS (more data, `D`), or split between both. Kaplan et al.'s early advice was closer to "mostly build more shelves." Chinchilla's finding, after more careful experimentation, was that the earlier advice had been under-buying books relative to shelves: for the SAME total budget, a library with FEWER shelves but proportionally MORE books on each of them serves readers better than one with many mostly-empty shelves, and the mathematically optimal split turns out to grow BOTH shelves and books at the same rate as the overall budget grows, never favoring one indefinitely over the other.

### The formula

```
C = 6 * N * D                      # total training compute (FLOPs)

Chinchilla-optimal split (simplified, N ≈ D at the optimum):
N_opt = D_opt = sqrt(C / 6)
```

Doubling `C` scales both `N_opt` and `D_opt` by `sqrt(2) ≈ 1.41`, not by `2`, a direct consequence of the square-root relationship.

### How PyTorch actually implements this

There is no `torch.nn` scaling-law utility (this is a PLANNING calculation, done BEFORE training starts, to decide what size model to train on how much data, not a runtime model component). Real large-scale training projects (LLaMA's technical report explicitly cites Chinchilla-style reasoning in justifying its own architecture and data-scale choices) use exactly this kind of compute-optimal allocation calculation to decide, GIVEN a fixed hardware/compute budget, what model size and dataset size to target BEFORE committing weeks of GPU time to an actual training run, since getting this allocation wrong (training a model too large for the data it'll see, or too small to make good use of the data available) wastes a real, substantial fraction of an expensive training budget.

## Explanation

`flops_for_training` implements the standard `6*N*D` approximation directly. `chinchilla_optimal_allocation` solves for the compute-optimal split under Chinchilla's simplified `N ≈ D` finding: substituting `N = D` into `C = 6*N*D` gives `C = 6*N^2`, so `N = sqrt(C / 6)`, and `D` takes that identical value. Because both `N_opt` and `D_opt` are proportional to `sqrt(C)`, doubling the compute budget scales BOTH by `sqrt(2)`, never favoring model size over data (or vice versa) as the budget grows, the precise mathematical content behind Chinchilla's real-world impact: reallocating a fixed compute budget toward more DATA (relative to what earlier scaling-law guidance suggested) produced Chinchilla's `70B`-parameter model outperforming Gopher's `280B` parameters trained on proportionally less data, for the same total training compute.
