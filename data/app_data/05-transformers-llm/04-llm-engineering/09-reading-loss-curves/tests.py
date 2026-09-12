"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/09-reading-loss-curves/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
detect_loss_spikes = _module.detect_loss_spikes
is_diverging = _module.is_diverging


def test_no_spikes_in_a_smoothly_decreasing_curve():
    loss_history = [10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0]
    spikes = detect_loss_spikes(loss_history, window=3, spike_ratio=1.5)
    assert spikes == []


def test_detects_a_single_injected_spike():
    loss_history = [5.0, 4.9, 4.8, 4.7, 50.0, 4.6, 4.5, 4.4]
    spikes = detect_loss_spikes(loss_history, window=3, spike_ratio=1.5)
    assert 4 in spikes


def test_spike_detection_respects_the_ratio_threshold():
    # A modest, non-alarming increase should NOT trigger with a lenient ratio.
    loss_history = [5.0, 5.0, 5.0, 5.5]
    spikes_lenient = detect_loss_spikes(loss_history, window=3, spike_ratio=2.0)
    spikes_strict = detect_loss_spikes(loss_history, window=3, spike_ratio=1.05)
    assert spikes_lenient == []
    assert 3 in spikes_strict


def test_no_spikes_detected_before_a_full_window_of_history_exists():
    loss_history = [5.0, 100.0]  # a huge jump, but no window of history yet
    spikes = detect_loss_spikes(loss_history, window=3, spike_ratio=1.5)
    assert spikes == []


def test_is_diverging_false_for_a_steadily_decreasing_loss():
    loss_history = [10.0, 9.0, 8.0, 7.0, 6.0, 5.0]
    assert is_diverging(loss_history, window=3) is False


def test_is_diverging_true_for_a_sustained_upward_trend():
    loss_history = [1.0, 1.1, 1.2, 3.0, 4.0, 5.0]
    assert is_diverging(loss_history, window=3) is True


def test_is_diverging_false_without_enough_history():
    loss_history = [1.0, 2.0, 3.0]
    assert is_diverging(loss_history, window=5) is False


def test_is_diverging_ignores_history_older_than_two_windows():
    # Directly targets a mutant that compares against the very START of
    # loss_history instead of the window immediately preceding the
    # recent one, which would miss a genuine recent uptick after an
    # initially-high loss.
    loss_history = [100.0, 100.0, 100.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0]
    # Earlier window (indices 3-5): mean 1.0. Recent window (indices 6-8): mean 2.0.
    # Should be diverging (recent > earlier), despite the very start (100.0) being much higher.
    assert is_diverging(loss_history, window=3) is True
