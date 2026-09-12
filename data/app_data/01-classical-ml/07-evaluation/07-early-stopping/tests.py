"""
pytest data/app_data/01-classical-ml/07-evaluation/07-early-stopping/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
best_epoch_with_min_delta = _module.best_epoch_with_min_delta
early_stopping_should_stop = _module.early_stopping_should_stop
train_with_early_stopping = _module.train_with_early_stopping


def test_best_epoch_matches_hand_computation():
    history = [10.0, 8.0, 6.0, 5.0, 4.0, 3.0, 3.5, 4.0, 4.5]
    assert best_epoch_with_min_delta(history) == 5


def test_min_delta_prevents_tiny_improvements_from_counting():
    history = [5.0, 4.9999, 4.9998]  # tiny wiggles, none real improvements
    assert best_epoch_with_min_delta(history, min_delta=0.01) == 0


def test_should_stop_matches_hand_computation():
    history = [10.0, 8.0, 6.0, 5.0, 4.0, 3.0, 3.5, 4.0, 4.5]  # best at index 5, now at index 8
    assert early_stopping_should_stop(history, patience=3) is True
    assert early_stopping_should_stop(history, patience=4) is False


def test_should_stop_is_false_for_empty_history():
    assert early_stopping_should_stop([], patience=3) is False


def test_train_with_early_stopping_returns_the_best_checkpoint_not_the_last():
    losses = [10, 8, 6, 5, 4, 3, 3.5, 4, 4.5, 5, 5.5, 6]

    def step_fn(epoch):
        return f"state_{epoch}", losses[epoch]

    result = train_with_early_stopping(step_fn, max_epochs=12, patience=3)
    assert result["best_state"] == "state_5"
    assert result["best_loss"] == 3
    assert result["stopped_epoch"] == 8
    assert len(result["history"]) == 9


def test_training_runs_full_length_when_always_improving():
    def step_fn(epoch):
        return f"state_{epoch}", 10.0 - epoch  # strictly decreasing

    result = train_with_early_stopping(step_fn, max_epochs=5, patience=2)
    assert result["stopped_epoch"] == 4
    assert result["best_state"] == "state_4"
    assert len(result["history"]) == 5


def test_keeps_the_minimum_loss_not_the_maximum():
    # Directly targets a mutant that flips the improvement comparison
    # (keeps the WORST loss seen instead of the best): with a clear
    # single minimum, that specific epoch's state must be returned.
    losses = [5.0, 1.0, 8.0, 9.0]

    def step_fn(epoch):
        return f"state_{epoch}", losses[epoch]

    result = train_with_early_stopping(step_fn, max_epochs=4, patience=10)
    assert result["best_state"] == "state_1"
    assert result["best_loss"] == 1.0
