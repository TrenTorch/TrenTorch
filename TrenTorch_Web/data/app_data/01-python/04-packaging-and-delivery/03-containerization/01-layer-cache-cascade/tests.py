"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
rebuilt_steps = _module.rebuilt_steps


BASE = [
    ("FROM python:3.12", "d0"),
    ("COPY requirements.txt .", "r1"),
    ("RUN pip install -r requirements.txt", "i1"),
    ("COPY . .", "s1"),
]


def test_nothing_changed_everything_cached():
    assert rebuilt_steps(BASE, list(BASE)) == []


def test_last_step_changed_only_it_rebuilds():
    current = BASE[:3] + [("COPY . .", "s2")]
    assert rebuilt_steps(BASE, current) == [3]


def test_change_cascades_to_identical_later_steps():
    current = [BASE[0], ("COPY requirements.txt .", "r2"), BASE[2], BASE[3]]
    assert rebuilt_steps(BASE, current) == [1, 2, 3]


def test_first_step_changed_rebuilds_everything():
    current = [("FROM python:3.13", "d9")] + BASE[1:]
    assert rebuilt_steps(BASE, current) == [0, 1, 2, 3]


def test_appended_steps_are_always_rebuilt():
    current = BASE + [("RUN pytest", "t1")]
    assert rebuilt_steps(BASE, current) == [4]


def test_removed_trailing_step_costs_nothing():
    assert rebuilt_steps(BASE, BASE[:2]) == []


def test_first_ever_build_rebuilds_all():
    assert rebuilt_steps([], BASE) == [0, 1, 2, 3]


def test_instruction_text_change_invalidates():
    current = [BASE[0], BASE[1], ("RUN pip install --no-cache-dir -r requirements.txt", "i1"), BASE[3]]
    assert rebuilt_steps(BASE, current) == [2, 3]
