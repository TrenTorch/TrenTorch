---
name: evaluation-bayesian-optimization
title: 'Note: Bayesian optimization for hyperparameter search'
tags: [classical-ml, evaluation, hyperparameter-tuning, gaussian-processes]
difficulty: Intermediate
---

## Statement

Implement:

```python
def expected_improvement(mean, std, best_so_far, xi=0.01) -> np.ndarray: ...
def propose_next_point(input_train, targets_train, candidates, length_scale, variance, noise, xi=0.01) -> int: ...
```

- Reuse `05-gaussian-processes`'s `gp_predict`.

## Theory

`04-grid-search` and `05-random-search` both pick their next hyperparameter configuration blindly, a fixed grid or a random draw, with no memory of how earlier configurations actually scored. Bayesian optimization does the opposite: fit a probabilistic model (a Gaussian Process, `05-gaussian-processes`, treating "hyperparameters in, validation score out" as the unknown function being learned) to every configuration tried so far, and use that model's _uncertainty_, not just its predictions, to decide where to look next.

The key tool is an **acquisition function**, a score computed at every untried candidate that balances two competing goals:

- **exploitation**: try points near where the GP's mean prediction is already good
- **exploration**: try points where the GP is still very uncertain (`std` is high), since a genuinely great configuration could be hiding there

**Expected Improvement (EI)** is the standard acquisition function that formalizes this tradeoff into one number:

```text
z  = (mean(x) - best_so_far - xi) / std(x)
EI(x) = (mean(x) - best_so_far - xi) * Phi(z) + std(x) * phi(z)
```

`Phi`/`phi` are the standard normal CDF/PDF. Intuitively: `EI` is large when `mean(x)` is well above the best value seen so far (a candidate the model is confident would improve on the current best) _or_ when `std(x)` is large (a candidate the model genuinely doesn't know about yet, worth trying just to learn more), and `EI` is exactly `0` wherever `std(x) = 0`, a point the model is completely certain about has no room to improve, revisiting it teaches nothing. `xi` is a small margin that keeps the search from stalling out on tiny, insignificant improvements.

```text
initialize with a few random configurations
repeat:
    fit a GP to (configurations tried, scores observed)
    propose_next_point: whichever untried candidate maximizes EI
    actually evaluate it, add it to the observed data
```

Compared to grid or random search, Bayesian optimization typically needs far fewer total evaluations to find a good configuration, at the cost of needing to fit a model (the GP) between every evaluation, worthwhile when each evaluation (training a real model) is expensive, less so when evaluations are cheap and grid/random search's simplicity wins instead.

## Explanation

`expected_improvement` computes `z = improvement / std` (guarded against `std == 0`, which would divide by zero), then `normal_pdf(z)` directly from the Gaussian density formula, and `normal_cdf(z)` via `math.erf` (`Phi(z) = 0.5*(1+erf(z/sqrt(2)))`, the standard closed-form relationship between the normal CDF and the error function), `np.vectorize`d to apply elementwise across the whole array of candidates. The final `np.where(std > 0, ei, 0.0)` enforces the "zero uncertainty means zero improvement value" rule directly, rather than relying on the formula to naturally produce `0` there.

`propose_next_point` calls `gp_predict(input_train, targets_train, candidates, ...)` to get the GP's posterior `mean`/`variance` at every candidate (`std = sqrt(variance)`), scores every candidate with `expected_improvement` against `targets_train.max()` (the best value observed among the points actually evaluated so far), and returns `np.argmax(ei)`, the single candidate the acquisition function says is most worth trying next.
