"""
pytest data/app_data/09-systems-distributed/02-parallelism/02-pipeline-parallelism-bubble-fraction/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/02-parallelism/{Path(__file__).resolve().parent.name}")
pipeline_bubble_fraction = _module.pipeline_bubble_fraction
pipeline_wall_time = _module.pipeline_wall_time
ideal_wall_time = _module.ideal_wall_time
pipeline_stage_utilization = _module.pipeline_stage_utilization


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matches_the_gpipe_bubble_formula():
    assert math.isclose(pipeline_bubble_fraction(4, 8), 3 / 11)
    assert math.isclose(pipeline_bubble_fraction(2, 10), 1 / 11)


def test_02_wall_time_exceeds_ideal_time_by_exactly_the_bubble():
    p, m, t = 4, 8, 1.5
    wall = pipeline_wall_time(p, m, t)
    ideal = ideal_wall_time(m, t)
    assert math.isclose(wall - ideal, (p - 1) * t)


# --- General-case coverage --------------------------------------------


def test_03_bubble_fraction_derivable_from_wall_and_ideal_time():
    for p, m, t in [(4, 8, 1.0), (2, 10, 2.0), (8, 32, 0.5), (3, 3, 1.0)]:
        bubble = pipeline_bubble_fraction(p, m)
        wall = pipeline_wall_time(p, m, t)
        ideal = ideal_wall_time(m, t)
        assert math.isclose(bubble, 1 - ideal / wall, rel_tol=1e-9)


def test_04_more_stages_means_more_bubble_for_fixed_microbatches():
    small = pipeline_bubble_fraction(2, 8)
    large = pipeline_bubble_fraction(8, 8)
    assert large > small


def test_05_more_microbatches_means_less_bubble_for_fixed_stages():
    few = pipeline_bubble_fraction(4, 1)
    many = pipeline_bubble_fraction(4, 100)
    assert many < few


# --- Parameter handling -------------------------------------------------


def test_06_stage_utilization_is_bubble_complement():
    for p, m in [(4, 8), (2, 10), (8, 32)]:
        assert math.isclose(pipeline_stage_utilization(p, m), 1 - pipeline_bubble_fraction(p, m))


def test_07_utilization_approaches_one_as_microbatches_grow():
    assert pipeline_stage_utilization(4, 1000) > 0.99


# --- Edge cases ---------------------------------------------------------


def test_08_single_stage_has_zero_bubble():
    assert pipeline_bubble_fraction(1, 10) == 0.0
    assert pipeline_stage_utilization(1, 10) == 1.0


def test_09_single_microbatch_bubble_fraction():
    p = 5
    assert math.isclose(pipeline_bubble_fraction(p, 1), (p - 1) / p)


# --- Independent correctness oracle -----------------------------------


def test_10_bubble_fraction_bounded_between_zero_and_one():
    # Directly targets a mutant that inverts the formula (e.g. m / (p -
    # 1 + m) instead of (p - 1) / (p - 1 + m)), which would still look
    # plausible but violate "more stages = more bubble".
    for p in range(1, 10):
        for m in range(1, 50):
            b = pipeline_bubble_fraction(p, m)
            assert 0.0 <= b < 1.0
    assert pipeline_bubble_fraction(10, 1) > pipeline_bubble_fraction(2, 1)
