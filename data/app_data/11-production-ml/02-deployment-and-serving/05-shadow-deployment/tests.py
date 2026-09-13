"""
pytest data/app_data/11-production-ml/02-deployment-and-serving/05-shadow-deployment/tests.py
"""

import sys
from pathlib import Path

import math

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/02-deployment-and-serving/{Path(__file__).resolve().parent.name}")
shadow_deploy = _module.shadow_deploy
outputs_agree = _module.outputs_agree
compute_agreement_rate = _module.compute_agreement_rate


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_response_comes_from_the_live_model_only():
    result = shadow_deploy(5, lambda r: r * 2, lambda r: r * 100)
    assert result["response"] == 10  # NOT the shadow's 500


def test_02_shadow_output_is_recorded_but_not_returned_as_the_response():
    result = shadow_deploy(5, lambda r: "live", lambda r: "shadow")
    assert result["response"] == "live"
    assert result["shadow_output"] == "shadow"


# --- General-case coverage --------------------------------------------


def test_03_shadow_model_error_does_not_affect_the_real_response():
    def broken_shadow(r):
        raise RuntimeError("shadow blew up")

    result = shadow_deploy(5, lambda r: "safe response", broken_shadow)
    assert result["response"] == "safe response"
    assert result["shadow_output"] is None
    assert result["shadow_error"] is not None


def test_04_outputs_agree_within_floating_point_tolerance():
    assert outputs_agree(1.0000000001, 1.0000000002, tolerance=1e-6)


def test_05_outputs_agree_detects_real_disagreement():
    assert not outputs_agree(1.0, 2.0)
    assert not outputs_agree("a", "b")


# --- Parameter handling -------------------------------------------------


def test_06_agreement_rate_matches_hand_computation():
    comparisons = [(1.0, 1.0), (1.0, 2.0), (5.0, 5.0), (3.0, 4.0)]
    assert math.isclose(compute_agreement_rate(comparisons), 0.5)


def test_07_live_model_error_still_propagates_normally():
    def broken_live(r):
        raise RuntimeError("live model down")

    with pytest.raises(RuntimeError):
        shadow_deploy(5, broken_live, lambda r: "shadow")


# --- Edge cases ---------------------------------------------------------


def test_08_empty_comparison_list_is_vacuously_fully_agreeing():
    assert math.isclose(compute_agreement_rate([]), 1.0)


def test_09_string_outputs_use_exact_equality():
    assert outputs_agree("hello", "hello")
    assert not outputs_agree("hello", "hell")


# --- Independent correctness oracle -----------------------------------


def test_10_shadow_output_never_leaks_into_the_response_across_many_calls():
    # Directly targets a mutant that occasionally returns the shadow's
    # output instead of the live model's (e.g. picking whichever
    # finished "first" in some non-deterministic way): across many
    # calls with deliberately very different live/shadow outputs, the
    # response must ALWAYS be the live model's.
    for i in range(20):
        result = shadow_deploy(i, lambda r: f"live-{r}", lambda r: f"shadow-{r}")
        assert result["response"] == f"live-{i}"
        assert result["response"] != result["shadow_output"]
