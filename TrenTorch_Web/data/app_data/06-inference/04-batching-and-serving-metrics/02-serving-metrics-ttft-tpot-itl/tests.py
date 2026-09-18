"""
pytest data/app_data/06-inference/04-batching-and-serving-metrics/02-serving-metrics-ttft-tpot-itl/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

serving_metrics = load_solution(
    f"06-inference/04-batching-and-serving-metrics/{Path(__file__).resolve().parent.name}"
).serving_metrics


def test_example_from_description():
    result = serving_metrics(0, [0.5, 0.7, 0.9, 1.3])
    assert abs(result["ttft"] - 0.5) < 1e-9
    assert [round(x, 6) for x in result["itl"]] == [0.2, 0.2, 0.4]
    assert abs(result["tpot"] - (0.2 + 0.2 + 0.4) / 3) < 1e-6
    assert abs(result["throughput_tokens_per_sec"] - 4 / 1.3) < 1e-9


def test_single_token_tpot_is_none():
    result = serving_metrics(1.0, [1.4])
    assert abs(result["ttft"] - 0.4) < 1e-9
    assert result["itl"] == []
    assert result["tpot"] is None


def test_uniform_spacing():
    result = serving_metrics(2.0, [2.1, 2.2, 2.3, 2.4, 2.5])
    assert abs(result["ttft"] - 0.1) < 1e-9
    assert all(abs(x - 0.1) < 1e-9 for x in result["itl"])
    assert abs(result["tpot"] - 0.1) < 1e-9


def test_throughput_matches_n_over_total_time():
    result = serving_metrics(0.0, [1.0, 2.0, 3.0])
    assert abs(result["throughput_tokens_per_sec"] - 1.0) < 1e-9
