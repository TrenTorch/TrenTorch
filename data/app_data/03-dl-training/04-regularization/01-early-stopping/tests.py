"""
pytest data/app_data/03-dl-training/04-regularization/01-early-stopping/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/04-regularization/{Path(__file__).resolve().parent.name}")
EarlyStopping = _module.EarlyStopping


def test_first_call_always_counts_as_an_improvement():
    es = EarlyStopping(patience=3)
    should_stop = es.step(5.0)
    assert should_stop is False
    assert es.best_loss == 5.0
    assert es.counter == 0


def test_does_not_stop_while_still_improving():
    es = EarlyStopping(patience=2)
    for loss in [5.0, 4.0, 3.0, 2.0, 1.0]:
        should_stop = es.step(loss)
        assert should_stop is False
    assert es.best_loss == 1.0


def test_stops_after_patience_consecutive_non_improving_epochs():
    es = EarlyStopping(patience=3)
    es.step(5.0)  # best = 5.0
    assert es.step(5.5) is False  # counter=1
    assert es.step(5.2) is False  # counter=2
    assert es.step(5.1) is True  # counter=3 -> stop


def test_an_improvement_in_the_middle_resets_the_counter():
    es = EarlyStopping(patience=3)
    es.step(5.0)  # best=5.0, counter=0
    es.step(5.5)  # counter=1
    es.step(4.0)  # improvement! best=4.0, counter=0
    assert es.counter == 0
    assert es.should_stop is False
    es.step(4.5)  # counter=1
    es.step(4.6)  # counter=2
    assert es.should_stop is False


def test_min_delta_requires_more_than_a_tiny_improvement():
    es = EarlyStopping(patience=2, min_delta=0.1)
    es.step(5.0)  # best=5.0
    es.step(4.95)  # improvement of only 0.05 < min_delta=0.1: NOT counted as improvement
    assert es.counter == 1
    assert es.best_loss == 5.0


def test_min_delta_zero_counts_any_strict_improvement():
    es = EarlyStopping(patience=5, min_delta=0.0)
    es.step(5.0)
    es.step(4.9999)
    assert es.counter == 0
    assert es.best_loss == 4.9999


def test_best_state_tracks_the_state_from_the_best_epoch():
    es = EarlyStopping(patience=5)
    es.step(5.0, state="checkpoint_A")
    es.step(3.0, state="checkpoint_B")  # improvement
    es.step(4.0, state="checkpoint_C")  # not an improvement
    assert es.best_state == "checkpoint_B"


def test_should_stop_remains_true_once_triggered():
    es = EarlyStopping(patience=1)
    es.step(5.0)
    es.step(6.0)  # triggers should_stop
    assert es.should_stop is True
    es.step(1.0)  # even a huge improvement afterward...
    assert es.should_stop is True  # ...should_stop was never reset


def test_step_returns_the_current_should_stop_value():
    es = EarlyStopping(patience=2)
    assert es.step(5.0) == es.should_stop
    assert es.step(6.0) == es.should_stop
    assert es.step(6.0) == es.should_stop


def test_counter_only_accumulates_on_consecutive_non_improvements_not_just_any_call():
    # Directly targets a mutant that increments counter on EVERY call
    # instead of only on non-improving ones (e.g. forgetting the if/else
    # split entirely): a steadily-improving loss sequence would then
    # still trigger should_stop after `patience` epochs, even though
    # every single epoch was an improvement.
    es = EarlyStopping(patience=3)
    for loss in [10.0, 9.0, 8.0, 7.0, 6.0, 5.0]:
        should_stop = es.step(loss)
    assert should_stop is False
    assert es.counter == 0
