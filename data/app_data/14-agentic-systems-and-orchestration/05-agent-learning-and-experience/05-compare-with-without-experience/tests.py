"""
pytest data/app_data/14-agentic-systems-and-orchestration/05-agent-learning-and-experience/05-compare-with-without-experience/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

compare_experience_impact = load_solution(
    f"14-agentic-systems-and-orchestration/05-agent-learning-and-experience/{Path(__file__).resolve().parent.name}"
).compare_experience_impact


def _approx_dict(result, expected, keys_to_check_float):
    for key in expected:
        if key in keys_to_check_float:
            assert abs(result[key] - expected[key]) < 1e-9, key
        else:
            assert result[key] == expected[key], key


def test_1_experience_helps_on_every_task():
    with_exp = [True, True, True]
    without_exp = [False, False, False]
    result = compare_experience_impact(with_exp, without_exp)
    _approx_dict(
        result,
        {
            "with_success_rate": 1.0,
            "without_success_rate": 0.0,
            "tasks_only_with_helped": 3,
            "delta": 1.0,
        },
        {"with_success_rate", "without_success_rate", "delta"},
    )


def test_2_no_difference_between_the_two():
    with_exp = [True, False, True]
    without_exp = [True, False, True]
    result = compare_experience_impact(with_exp, without_exp)
    _approx_dict(
        result,
        {
            "with_success_rate": 2 / 3,
            "without_success_rate": 2 / 3,
            "tasks_only_with_helped": 0,
            "delta": 0.0,
        },
        {"with_success_rate", "without_success_rate", "delta"},
    )


def test_3_mixed_results_partial_help():
    with_exp = [True, True, False, True]
    without_exp = [True, False, False, False]
    result = compare_experience_impact(with_exp, without_exp)
    _approx_dict(
        result,
        {
            "with_success_rate": 0.75,
            "without_success_rate": 0.25,
            "tasks_only_with_helped": 2,
            "delta": 0.5,
        },
        {"with_success_rate", "without_success_rate", "delta"},
    )


def test_4_experience_never_hurts_metric_only_counts_where_with_succeeds():
    # without_experience succeeding where with_experience fails is NOT
    # counted in tasks_only_with_helped (that metric is one-directional).
    with_exp = [False, True]
    without_exp = [True, True]
    result = compare_experience_impact(with_exp, without_exp)
    assert result["tasks_only_with_helped"] == 0
    assert abs(result["delta"] - (-0.5)) < 1e-9


def test_5_single_task():
    result = compare_experience_impact([True], [False])
    assert result["tasks_only_with_helped"] == 1
    assert abs(result["with_success_rate"] - 1.0) < 1e-9
    assert abs(result["without_success_rate"] - 0.0) < 1e-9
