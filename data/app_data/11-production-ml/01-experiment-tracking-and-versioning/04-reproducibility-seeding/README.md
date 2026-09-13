---
name: production-ml-reproducibility-seeding
title: 'Reproducibility: Pinning Every Source of Randomness in a Training Run'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-experiment-tracking` records a run's hyperparameters faithfully — but hyperparameters alone don't fully determine a training run's outcome: weight initialization, data shuffling, and dropout all involve randomness, and a training run is only truly REPRODUCIBLE if every one of those independent random sources is pinned to a known seed. Missing even one — a genuinely common mistake, since a language's built-in RNG and NumPy's RNG are completely separate systems — silently breaks reproducibility.

### From theory to code

Implement `seeded_numpy_sequence` and `seeded_python_random_sequence` (two GENUINELY SEPARATE random number sources, each independently seedable), `capture_reproducibility_config` (bundling both seeds for logging), and `verify_reproducible` (the actual practical test of whether reproducibility holds).

### Constraints

- `seeded_numpy_sequence(seed, n)` uses `np.random.default_rng(seed)`; the same seed must always produce the same sequence.
- `seeded_python_random_sequence(seed, n)` uses Python's own `random.Random(seed)` — a genuinely independent generator from NumPy's.
- Seeding one of the two sources must have NO effect on the other's output.
- `verify_reproducible(fn, seed, num_trials)` calls `fn(seed)` `num_trials` times and returns `True` only if every call produces an identical result.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`random.Random(seed)` creates a fresh, independent generator instance (as opposed to `random.seed(seed)`, which mutates Python's single GLOBAL generator) — using an instance keeps this exercise's functions free of hidden global state, exactly the kind of hidden state that makes real reproducibility bugs hard to track down.

</details>

<details>
<summary>Hint 2</summary>

`verify_reproducible` doesn't need to know anything about WHAT `fn` does internally — it just calls it several times with the same seed and checks all the results match, using `np.array_equal` so it works whether `fn` returns a NumPy array or a plain Python list.

</details>

## Theory

### The simple version

Imagine trying to reproduce a specific chemistry experiment's result, but the experiment involves THREE separate pieces of equipment, each with its own independent random dial (a die-roller, a coin-flipper, and a card-shuffler) — writing down only the die-roller's setting and assuming "the experiment is reproducible now" would be a mistake, because the coin-flipper and card-shuffler are still producing fresh randomness every time. A real training run has exactly this structure: NumPy's RNG, Python's built-in RNG, and (in a real deep learning framework) the framework's own RNG are all independent "dials" that each need their own seed recorded.

### The formula

```text
seeded_numpy_sequence(seed, n)        = np.random.default_rng(seed).random(n)
seeded_python_random_sequence(seed, n) = [random.Random(seed).random() for _ in range(n)]

-- these two are COMPLETELY INDEPENDENT: seeding one has zero effect on the other

capture_reproducibility_config(numpy_seed, python_seed) = {numpy_seed, python_random_seed}

verify_reproducible(fn, seed, num_trials):
    results = [fn(seed) for _ in range(num_trials)]
    return all results are equal to results[0]
```

`verify_reproducible` is deliberately the actual, operational definition of reproducibility used in this exercise: not "did I remember to call a seed function somewhere," but "does calling the SAME code with the SAME seed genuinely produce the SAME output, every single time, verified empirically."

### How PyTorch actually implements this

Context only, untested by your submission: real deep learning frameworks (PyTorch's `torch.manual_seed`, plus separately `torch.cuda.manual_seed_all` for GPU operations, on top of Python's `random.seed` and NumPy's `np.random.seed`) require pinning MULTIPLE independent RNG sources at once for full reproducibility — and PyTorch's own documentation explicitly warns that even with every seed pinned, some GPU operations remain non-deterministic unless additional (performance-costly) determinism flags are also set, a real, well-known limit on how far seeding alone can go.

## Explanation

`seeded_numpy_sequence` and `seeded_python_random_sequence` each create a fresh, seed-scoped generator instance rather than mutating any shared global state — `tests.py` confirms both are independently reproducible under a fixed seed, and — via its dedicated cross-source test — confirms that generating a NumPy sequence with an unrelated seed in between two Python-random calls has zero effect on the Python sequence, directly demonstrating the two sources' genuine independence.

`capture_reproducibility_config` is a simple bundling function, included specifically to connect back to `01-experiment-tracking`: a real reproducibility-conscious run would log exactly this kind of config as part of its tracked metadata.

`verify_reproducible` is the exercise's actual payoff: a general-purpose reproducibility checker that works on ANY seed-taking function — `tests.py` confirms it correctly returns `True` for a genuinely-seeded function and, via a deliberately unseeded counter-example, correctly returns `False` for a function that ignores its seed entirely, and its final oracle test confirms the function is actually invoked the requested number of times (via a call-counting closure), ruling out a mutant that fakes reproducibility without ever really calling `fn` more than once.
