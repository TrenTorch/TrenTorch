---
name: rl-alignment-capstone-report
title: 'Final Capstone: Submission/Report'
tags: [mlops, metrics-and-evaluation]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`02-apply-optimization-measure-improvement` produced raw benchmark numbers for ONE optimization attempt. A real capstone submission needs to turn that into an honest, structured verdict — and, crucially, needs a rule for what actually counts as a PASSING submission when comparing several candidate optimizations: a big speedup on broken code, or a correct-but-slower result, must never be treated as a win.

### From theory to code

Implement `build_capstone_report` (turning one optimization's raw stats into a structured pass/fail verdict) and `compare_capstone_reports` (picking the best PASSING submission out of several).

### Constraints

- `build_capstone_report(project_name, baseline_stats, optimized_stats, correctness_verified)` computes `speedup_factor = baseline_stats["median"] / optimized_stats["median"]`, and `passed = correctness_verified and speedup_factor > 1.0`.
- Returns a dict with `"project_name"`, `"speedup_factor"`, `"correctness_verified"`, `"passed"`, and a one-line `"summary"` string mentioning the project name.
- `compare_capstone_reports(reports)` returns the highest-`speedup_factor` report AMONG ONLY the ones with `passed=True`; if none pass, returns `{"best_project": None, "best_speedup_factor": None, "num_passing": 0}`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`passed` requires BOTH conditions at once (`correctness_verified AND speedup_factor > 1.0`) — a correct-but-not-actually-faster submission fails just as much as an incorrect-but-fast one does.

</details>

<details>
<summary>Hint 2</summary>

`compare_capstone_reports` should FILTER to `passed=True` reports first, THEN find the max by `speedup_factor` among only those survivors — never compare a failing report's speedup against a passing one's.

</details>

## Theory

### The simple version

Imagine judging a science fair where one project claims a dramatic result but the judges can't reproduce it, another project shows a real, verified, but fairly modest improvement, and a third project shows no real improvement at all — a fair judging rule has to disqualify the unreproducible dramatic claim FIRST, before even comparing magnitudes, otherwise the flashiest (but fake) result would always "win" on paper. This exercise builds exactly that judging rule: correctness is a gate you must pass through before speed is even allowed to matter.

### The formula

```text
build_capstone_report(name, baseline, optimized, correct):
    speedup = baseline.median / optimized.median
    passed  = correct AND speedup > 1.0
    return {project_name: name, speedup_factor: speedup, correctness_verified: correct,
            passed: passed, summary: "<name>: <speedup>x speedup (...)"}

compare_capstone_reports(reports):
    passing = [r for r in reports if r.passed]
    if passing is empty: return {best_project: None, best_speedup_factor: None, num_passing: 0}
    best = passing report with the highest speedup_factor
    return {best_project: best.project_name, best_speedup_factor: best.speedup_factor, num_passing: len(passing)}
```

This is the same "correctness gates speed" theme that's run throughout this curriculum's optimization-focused questions (`02-apply-optimization-measure-improvement`'s `verify_optimization_correctness`, the Systems Performance section's quantization/pruning tradeoffs) — a fast wrong answer is never actually an improvement, no matter how impressive the raw number looks in isolation.

### How PyTorch actually implements this

Context only, untested by your submission: this mirrors how real ML systems benchmarking suites and CI pipelines are structured in practice — a performance regression test typically has to pass a correctness check FIRST, and only compares timing numbers among implementations that already produced the right answer, exactly to avoid the failure mode of accidentally celebrating a "fast" but silently broken change.

## Explanation

`build_capstone_report` computes the raw speedup ratio directly from the two stats dicts' `"median"` entries, and applies the two-part pass condition — `tests.py` confirms a submission fails when correctness isn't verified (even if the speedup number alone would look great), fails when the "optimized" version is actually SLOWER than baseline (even if correctness holds), and only passes when both hold at once.

`compare_capstone_reports` filters to passing submissions before ever comparing speedup factors — `tests.py`'s dedicated test constructs a deliberately impressive-looking but `correctness_verified=False` submission alongside a modest, genuinely correct one, and confirms the correct-but-modest submission wins every time, and its final oracle test confirms the winner is chosen by genuinely comparing `speedup_factor` values (not by submission order), directly ruling out a mutant that just returns the first or last passing report without actually comparing them.
