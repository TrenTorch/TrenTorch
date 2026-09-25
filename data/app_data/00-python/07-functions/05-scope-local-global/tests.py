"""
pytest data/app_data/00-python/07-functions/05-scope-local-global/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/07-functions/{Path(__file__).resolve().parent.name}")
local_double = _module.local_double
read_limit = _module.read_limit
increment_global = _module.increment_global
mutate_shared = _module.mutate_shared


def test_local_result():
    assert local_double(5) == 10
    assert local_double(0) == 0


def test_no_accidental_global_assignment():
    result = 100  # a module-level-looking name in the TEST, unrelated to the solution
    local_double(5)
    assert result == 100


def test_global_reassignment():
    _module.COUNTER = 4
    assert increment_global() == 5
    assert _module.COUNTER == 5


def test_repeated_calls_do_not_leak_local_state():
    assert local_double(3) == 6
    assert local_double(10) == 20


def test_mutation_versus_reassignment():
    xs = [1]
    result = mutate_shared(xs, 2)
    assert result == [1, 2]
    assert result is xs
    assert read_limit(5, 10) is True
    assert read_limit(15, 10) is False
