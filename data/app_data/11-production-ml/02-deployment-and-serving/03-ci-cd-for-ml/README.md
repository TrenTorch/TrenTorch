---
name: production-ml-ci-cd-for-ml
title: 'Note: CI/CD for ML, Testing a Model Like You Would Test Code Before It Ships'
tags: [mlops]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`02-training-pipelines-dag` made training itself reproducible and automatable — but a pipeline that runs reliably can still produce a genuinely BAD model. Ordinary software CI blocks a deploy when tests fail; ML needs the same discipline, adapted to one real complication: a model's output can shift slightly between valid retrains (different random seed, slightly different data), so gating on "100% of tests pass" is often too strict to be useful in practice.

### From theory to code

Implement `run_model_tests` (a real test-suite runner for a model), `pass_rate`, and `gate_deployment`, which decides whether a model is allowed to ship based on a PASS-RATE threshold rather than requiring every single test to succeed.

### Constraints

- `run_model_tests(model_fn, test_cases)`: each test case is `(test_name, input_value, check_fn)`; a test that raises an exception counts as FAILED, never crashes the whole suite.
- `pass_rate(results)` returns the fraction of passing tests; an empty suite is vacuously `1.0`.
- `gate_deployment(results, min_pass_rate)` returns `True` exactly when `pass_rate(results) >= min_pass_rate`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Wrap each test's execution in a `try`/`except` — a model that crashes on one particular input is a real, valid test FAILURE, not a reason to abort checking the rest of the suite.

</details>

<details>
<summary>Hint 2</summary>

`gate_deployment` doesn't need to know anything about the individual test cases — it's a one-line comparison built entirely on top of `pass_rate`'s already-computed number.

</details>

## Theory

### The simple version

Imagine a factory quality-control process for a product whose exact measurements are allowed to vary slightly batch to batch (a cookie's weight, say) — requiring EVERY single cookie to weigh EXACTLY 50.000 grams would reject perfectly good batches over meaningless noise, so real quality control instead asks "are at least 95% of cookies within an acceptable range?" ML model testing works the same way: exact-match assertions on a model's raw output are usually too brittle, so CI/CD for ML gates on a PASS-RATE threshold across a suite of behavioral checks instead.

### The formula

```text
run_model_tests(model_fn, test_cases):
    for (name, input, check_fn) in test_cases:
        try: passed = check_fn(model_fn(input))
        except: passed = False
        results.append({name, passed})

pass_rate(results) = (count of passed) / len(results), or 1.0 if empty

gate_deployment(results, min_pass_rate) = pass_rate(results) >= min_pass_rate
```

The exception-safety in `run_model_tests` matters for a genuinely different reason than in ordinary code testing: a model artifact that literally crashes on some valid-looking input is exactly the kind of regression a real deployment gate exists to catch, and letting one crashing test case take down the entire test RUN (instead of just that one test) would hide every other test's result behind it.

### How PyTorch actually implements this

Context only, untested by your submission: this reflects the real practice behind ML-specific CI/CD tooling (behavioral test suites like CheckList for NLP models, or simple custom pytest-based model test suites run in a GitHub Actions pipeline) — testing invariants (a sentiment classifier shouldn't flip its prediction when a name is swapped), known edge cases, and minimum-performance thresholds on a held-out set, gated by a tolerance for the natural variability real trained models exhibit.

## Explanation

`run_model_tests` runs every test case defensively, converting any exception into a straightforward failure rather than an uncaught crash — `tests.py` confirms a genuinely broken model call is correctly reported as a failed test, not a test-suite-ending error.

`pass_rate` computes the straightforward fraction, treating an empty suite as vacuously passing (there's nothing to have failed) — a real, if easily overlooked, edge case.

`gate_deployment` is the actual go/no-go decision — `tests.py`'s final oracle test confirms it genuinely derives its answer from `pass_rate` (varying the threshold around a fixed 30%-passing test suite and confirming the gate flips exactly where expected), directly ruling out a mutant that hardcodes a fixed pass/fail answer independent of the actual test results.
