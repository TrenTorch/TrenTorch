"""
pytest data/app_data/00-python/09-iteration-internals/06-assemble-lazy-pipeline/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/09-iteration-internals/{Path(__file__).resolve().parent.name}")
build_pipeline = _module.build_pipeline


def test_basic_transformation_pipeline():
    result = build_pipeline([1, 2, 3], transformations=[lambda x: x + 1, lambda x: x * 2])
    assert list(result) == [4, 6, 8]


def test_multiple_predicates():
    result = build_pipeline([1, 2, 3, 4, 5], predicates=[lambda x: x > 1, lambda x: x < 5])
    assert list(result) == [2, 3, 4]


def test_lazy_construction():
    consumed = []

    def source():
        for x in [1, 2, 3]:
            consumed.append(x)
            yield x

    build_pipeline(source())
    assert consumed == []


def test_lazy_partial_consumption():
    consumed = []

    def source():
        for x in [1, 2, 3, 4, 5]:
            consumed.append(x)
            yield x

    pipeline = build_pipeline(source())
    next(pipeline)
    assert consumed == [1]


def test_iterator_state_preservation():
    pipeline = build_pipeline([1, 2, 3])
    assert next(pipeline) == 1
    assert next(pipeline) == 2
    assert next(pipeline) == 3


def test_exhaustion_and_stop_iteration():
    import pytest

    pipeline = build_pipeline([1])
    next(pipeline)
    with pytest.raises(StopIteration):
        next(pipeline)


def test_empty_source():
    assert list(build_pipeline([])) == []


def test_all_values_rejected():
    result = build_pipeline([1, 2, 3], predicates=[lambda x: False])
    assert list(result) == []


def test_no_intermediate_materialization():
    pipeline = build_pipeline(range(10**9), transformations=[lambda x: x + 1])
    assert next(pipeline) == 1
    assert next(pipeline) == 2


def test_source_values_with_falsy_results():
    result = build_pipeline([0, 1, False, 2, None], predicates=[lambda x: x is not None])
    assert list(result) == [0, 1, False, 2]


def test_transformation_side_effects_only_on_request():
    calls = []

    def transform(x):
        calls.append(x)
        return x

    pipeline = build_pipeline([1, 2, 3], transformations=[transform])
    assert calls == []
    next(pipeline)
    assert calls == [1]


def test_pipeline_composition():
    result = build_pipeline(
        [1, 2, 3, 4, 5],
        transformations=[lambda x: x * 2],
        predicates=[lambda x: x > 5],
    )
    assert list(result) == [6, 8, 10]
