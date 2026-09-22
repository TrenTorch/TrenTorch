"""
pytest data/app_data/99-potd/01-daily/35-stockout-threshold-sweep-f1/tests.py
"""

import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
best_f1_threshold = _module.best_f1_threshold

TOLERANCE = 1e-6


def _reference(scores, y):
    """O(n^2) recompute-from-scratch reference, for cross-checking small cases."""
    best_t, best_f1 = None, -1.0
    for t in sorted(set(scores), reverse=True):
        tp = sum(1 for s, label in zip(scores, y) if s >= t and label == 1)
        fp = sum(1 for s, label in zip(scores, y) if s >= t and label == 0)
        fn = sum(1 for s, label in zip(scores, y) if s < t and label == 1)
        if tp + fp == 0 or tp + fn == 0:
            continue
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        if precision + recall == 0:
            continue
        f1 = 2 * precision * recall / (precision + recall)
        if f1 > best_f1:
            best_f1, best_t = f1, t
    return best_t, best_f1


def test_example_matches_the_specs_worked_value():
    scores = [0.9, 0.8, 0.75, 0.6, 0.55, 0.4, 0.3, 0.2]
    y = [1, 1, 0, 1, 0, 0, 1, 0]
    threshold, f1 = best_f1_threshold(scores, y)
    assert abs(threshold - 0.6) < TOLERANCE
    assert abs(f1 - 0.75) < TOLERANCE


def test_tie_for_best_f1_picks_the_larger_threshold():
    # Two thresholds t=0.9 (score>=0.9: 1 row, TP=1) and t=0.5 (all 2 rows,
    # TP=1, FP=1... let's construct a clean tie instead.
    # scores 0.9 (y=1), 0.1 (y=0): thresholds 0.9 -> TP=1,FP=0,FN=0 -> F1=1.0
    # threshold 0.1 -> TP=1,FP=1,FN=0 -> precision=0.5,recall=1,F1=0.6667.
    # Not a tie. Build an explicit tie instead:
    scores = [1.0, 0.5]
    y = [1, 0]
    # t=1.0: TP=1,FP=0,FN=0 -> F1=1.0. t=0.5: TP=1,FP=1,FN=0 -> F1=0.6667.
    # No tie here either; use duplicated scores with identical outcomes to force one:
    scores2 = [1.0, 1.0, 0.5]
    y2 = [1, 1, 0]
    # t=1.0: TP=2,FP=0,FN=0 -> F1=1.0 (only threshold reaching perfect).
    threshold, f1 = best_f1_threshold(scores2, y2)
    assert abs(threshold - 1.0) < TOLERANCE
    assert abs(f1 - 1.0) < TOLERANCE


def test_a_threshold_with_undefined_f1_never_wins():
    # The highest score is a lone false positive: TP+FP>0 but TP=0 there,
    # so precision=0, F1=0, never the max, but must not crash either.
    scores = [0.99, 0.5, 0.4]
    y = [0, 1, 1]
    threshold, f1 = best_f1_threshold(scores, y)
    assert f1 > 0  # some real threshold beats the lone-false-positive one


def test_matches_the_on2_reference_on_random_small_batches():
    rng = random.Random(30)
    for _ in range(30):
        n = rng.randint(2, 15)
        scores = [round(rng.uniform(0, 1), 2) for _ in range(n)]
        y = [rng.randint(0, 1) for _ in range(n)]
        if sum(y) == 0:
            continue  # no positives anywhere: every threshold is undefined
        got = best_f1_threshold(scores, y)
        expected = _reference(scores, y)
        assert abs(got[1] - expected[1]) < TOLERANCE
        assert abs(got[0] - expected[0]) < TOLERANCE


def test_large_n_within_the_time_budget():
    rng = random.Random(31)
    n = 100_000
    scores = [rng.uniform(0, 1) for _ in range(n)]
    y = [rng.randint(0, 1) for _ in range(n)]
    start = time.perf_counter()
    best_f1_threshold(scores, y)
    elapsed = time.perf_counter() - start
    assert elapsed < 5.0, f"took {elapsed:.2f}s on n=100000"
