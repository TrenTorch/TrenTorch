"""
pytest data/app_data/00-python/12-bridging-to-numpy-ml/04-comprehensions-as-vectorized-thinking/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/12-bridging-to-numpy-ml/{Path(__file__).resolve().parent.name}")
elementwise = _module.elementwise
mask_select = _module.mask_select
broadcast_add = _module.broadcast_add
normalize = _module.normalize


def test_elementwise_arity_and_length():
    assert elementwise(lambda a, b: a + b, [1, 2], [10, 20]) == [11, 22]
    assert elementwise(lambda a: a * 2, [1, 2, 3]) == [2, 4, 6]
    assert elementwise(lambda a, b, c: a + b + c, [1, 2], [10, 20], [100, 200, 300]) == [111, 222]
    assert elementwise(lambda: 1) == []


def test_mask_select_truthiness_and_lengths():
    assert mask_select([5, 6, 7], [True, False, True]) == [5, 7]
    assert mask_select([5, 6, 7], [1, 0, ""]) == [5]
    assert mask_select([5, 6, 7], [False, False, False]) == []
    assert mask_select([5, 6], [True, True, True]) == [5, 6]


def test_broadcast_add_scalar_vs_sequence():
    values = [1, 2, 3]
    assert broadcast_add(values, 10) == [11, 12, 13]
    assert broadcast_add(values, [1, 1, 1]) == [2, 3, 4]
    assert broadcast_add(values, (1, 1, 1)) == [2, 3, 4]
    assert values == [1, 2, 3]


def test_normalize_statistics():
    result = normalize([1.0, 2.0, 3.0], 1e-8)
    mean = sum(result) / len(result)
    assert abs(mean) < 1e-6
    variance = sum((x - mean) ** 2 for x in result) / len(result)
    assert abs(variance - 1.0) < 1e-3


def test_normalize_degenerate_inputs():
    assert normalize([5, 5, 5], 1e-5) == [0.0, 0.0, 0.0]
    assert normalize([5], 1e-5) == [0.0]
    assert normalize([], 1e-5) == []


def test_no_mutation_and_fresh_lists():
    values = [1, 2, 3]
    result = elementwise(lambda a: a, values)
    assert result is not values
    normalize(values, 1e-5)
    assert values == [1, 2, 3]
