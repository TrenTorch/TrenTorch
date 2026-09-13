---
name: rl-alignment-alignment-tax
title: 'Note: Alignment Tax, the Capability Cost of Aligning a Model'
tags: [reinforcement-learning, nlp, metrics-and-evaluation]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`12-reward-hacking-goodharts-law` showed that optimizing a proxy reward too hard can actively hurt what you truly care about. There's a related, equally real cost worth measuring directly: even a WELL-aligned model (genuinely more helpful, honest, and harmless) can lose some raw capability on standard benchmarks compared to its un-aligned base model — a real, quantifiable tradeoff the original InstructGPT paper explicitly measured and reported, rather than a purely hypothetical worry.

### From theory to code

Implement `alignment_tax` (the average capability regression across a suite of benchmarks), `per_benchmark_regression` (the same comparison, unaveraged), and `has_net_alignment_tax`.

### Constraints

- `alignment_tax(base_model_scores, aligned_model_scores)` returns `mean(base_model_scores - aligned_model_scores)`.
- `per_benchmark_regression(base_model_scores, aligned_model_scores)` returns the elementwise difference, one entry per benchmark.
- `has_net_alignment_tax(...)` returns `True` exactly when `alignment_tax(...) > 0`.
- A positive `alignment_tax` means the aligned model is, ON AVERAGE, less capable than the base model it came from; it's possible for `per_benchmark_regression` to show BOTH gains and losses across different benchmarks even when the net tax is exactly zero.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`alignment_tax` is nothing more than `per_benchmark_regression(...).mean()` — the whole exercise is really about getting the SIGN of the subtraction right (base minus aligned, so a positive number means capability was LOST).

</details>

<details>
<summary>Hint 2</summary>

A model can genuinely improve on some benchmarks (alignment sometimes helps instruction-following-style tasks) while regressing on others (raw completion-style tasks) — `per_benchmark_regression` is what lets you see that full, mixed picture, rather than a single averaged number hiding it.

</details>

## Theory

### The simple version

Imagine a talented generalist employee who goes through specialized customer-service training: afterward, they're noticeably better at handling customer complaints politely and helpfully, but they might have gotten slightly rustier at some of the more technical, unrelated tasks they used to do routinely, simply because their practice time got reallocated. The "alignment tax" measures exactly this kind of tradeoff for a language model: how much general capability (on standard, alignment-unrelated benchmarks) got traded away in exchange for better alignment behavior.

### The formula

```text
per_benchmark_regression(base_scores, aligned_scores) = base_scores - aligned_scores    -- per benchmark

alignment_tax(base_scores, aligned_scores) = mean(per_benchmark_regression(base_scores, aligned_scores))

has_net_alignment_tax(...) = alignment_tax(...) > 0
```

A tax of exactly `0` doesn't necessarily mean NOTHING changed — it can mean gains on some benchmarks exactly offset losses on others, which is why `per_benchmark_regression`'s full, unaveraged view matters alongside the single summary number.

### How PyTorch actually implements this

Context only, untested by your submission: the InstructGPT paper (Ouyang et al., 2022) explicitly measured and reported exactly this — evaluating their RLHF-aligned model against the base pretrained model on a suite of public NLP benchmarks, finding a small but real capability regression on some of them (which they called the "alignment tax"), and treating minimizing that tax (e.g. by mixing pretraining data back into the RLHF fine-tuning phase) as an explicit design goal.

## Explanation

`per_benchmark_regression` computes the direct, base-minus-aligned difference for every benchmark, preserving the full picture of which benchmarks improved and which regressed.

`alignment_tax` averages that difference into one summary number — `tests.py` confirms it's mathematically just `per_benchmark_regression(...).mean()`, that it's exactly zero when the two models score identically, negative when the aligned model is uniformly BETTER, and — crucially — that a mix of gains and losses can still net to exactly zero, demonstrating the average alone doesn't tell the whole story.

`has_net_alignment_tax` is a simple boolean framing of the same number, and `tests.py` verifies the subtraction direction is genuinely `base - aligned` (not reversed) by checking that a model with UNIFORMLY worse aligned-model scores reports a real, unambiguous positive regression rather than accidentally reporting a capability GAIN — directly ruling out a mutant that swaps the subtraction order, which would silently invert the entire metric's meaning.
