---
name: production-ml-concept-drift-sliding-window
title: 'Concept Drift: The Relationship Between Inputs and the Target Shifting'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-data-drift-psi` catches a shift in WHAT inputs look like. But a model can keep seeing perfectly familiar-looking inputs while the actual RELATIONSHIP between those inputs and the correct answer changes underneath it — a spam filter's inputs might look statistically identical over time, but spammers constantly adapt their tactics, so what USED TO be a reliable spam signal stops being one. This is concept drift, and PSI can't catch it at all, since it never looks at labels or predictions — only actual PERFORMANCE monitoring can.

### From theory to code

Implement `sliding_window_accuracy` (breaking a long prediction stream into windows to make a performance shift visible over time), `detect_concept_drift`, and `first_drift_window`.

### Constraints

- `sliding_window_accuracy(predictions, labels, window_size)` splits the stream into consecutive, non-overlapping windows and returns each window's accuracy — a partial final window is dropped.
- `detect_concept_drift(window_accuracies, baseline_accuracy, drop_threshold)` returns `True` if ANY window's accuracy has fallen more than `drop_threshold` below `baseline_accuracy`.
- `first_drift_window` returns the INDEX of the first such window, or `None` if none qualify.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A single accuracy number computed over an entire long stream would completely hide a drift that happens partway through — the stable part and the degraded part would just average together into one misleadingly "okay" number. Windowing is what makes a mid-stream shift visible at all.

</details>

<details>
<summary>Hint 2</summary>

`detect_concept_drift` must check EVERY window, not just the most recent one — a drift that occurred and then recovered still counts as having happened, and a monitoring system that only glances at the latest reading would miss it entirely.

</details>

## Theory

### The simple version

Imagine a teacher grading a semester's worth of weekly quizzes for one student, but instead of computing a single semester-average grade (which could hide a student who did great for months and then suddenly struggled), the teacher looks at the WEEK-BY-WEEK trend — a sudden multi-week dip that a single average would smooth over becomes immediately obvious. This exercise applies exactly that "look at the trend over time, not just the overall average" idea to a deployed model's accuracy.

### The formula

```text
sliding_window_accuracy(predictions, labels, window_size):
    correct = (predictions == labels)
    for each consecutive, non-overlapping window of size window_size:
        append correct[window].mean()

detect_concept_drift(accuracies, baseline, drop_threshold) =
    any( baseline - accuracy > drop_threshold for accuracy in accuracies )

first_drift_window(...) = index of the FIRST accuracy satisfying that same condition, or None
```

This is a deliberately simple version of a real technique — production drift detectors (like DDM, the Drift Detection Method) use more sophisticated statistical tests involving the error rate's variance, not just a fixed drop threshold — but the underlying principle (window the stream, compare against a baseline, flag a meaningful drop) is exactly the same shape this exercise implements from scratch.

### How PyTorch actually implements this

Context only, untested by your submission: concept drift is a well-documented, real phenomenon in production ML systems that data drift monitoring alone cannot catch, since it's specifically about `P(target | input)` changing while `P(input)` itself stays put — real ML monitoring platforms track exactly this kind of windowed performance metric over time, often alongside `01-data-drift-psi`'s input-distribution check, since the two failure modes are genuinely independent and neither one implies the other.

## Explanation

`sliding_window_accuracy` computes accuracy separately within each fixed-size, non-overlapping chunk of the stream — `tests.py` confirms the exact windowing behavior (correctly dropping a partial final window) and demonstrates a genuine, obvious accuracy collapse becoming visible in the windowed output where a single overall average would have hidden it.

`detect_concept_drift` scans every window's accuracy against the baseline — `tests.py`'s final oracle test specifically constructs a "dip then recovery" scenario (accuracy drops sharply in the middle, then returns to normal) and confirms drift is STILL correctly detected, directly ruling out a mutant that only checks the most recent window.

`first_drift_window` reuses the identical drop condition to additionally report WHERE (by window index) the first qualifying drift occurred — genuinely useful for a real on-call engineer trying to correlate a detected drift with what else changed around that same time.
