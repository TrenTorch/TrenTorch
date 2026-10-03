"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
rebuild_cost = _module.rebuild_cost


APP_FILES = ["requirements.txt", "app.py", "model.py"]

NAIVE = [
    {"cmd": "FROM", "files": [], "cost": 5},
    {"cmd": "COPY", "files": APP_FILES, "cost": 1},
    {"cmd": "RUN", "files": [], "cost": 100},  # pip install
]

CACHE_FRIENDLY = [
    {"cmd": "FROM", "files": [], "cost": 5},
    {"cmd": "COPY", "files": ["requirements.txt"], "cost": 1},
    {"cmd": "RUN", "files": [], "cost": 100},  # pip install
    {"cmd": "COPY", "files": ["app.py", "model.py"], "cost": 1},
]


def test_nothing_changed_costs_nothing():
    assert rebuild_cost(NAIVE, set()) == 0
    assert rebuild_cost(CACHE_FRIENDLY, set()) == 0


def test_unrelated_file_costs_nothing():
    assert rebuild_cost(CACHE_FRIENDLY, {"README.md"}) == 0


def test_source_edit_naive_order_reruns_the_install():
    assert rebuild_cost(NAIVE, {"app.py"}) == 101


def test_source_edit_cache_friendly_order_skips_the_install():
    assert rebuild_cost(CACHE_FRIENDLY, {"app.py"}) == 1


def test_dependency_change_invalidates_install_in_both():
    assert rebuild_cost(NAIVE, {"requirements.txt"}) == 101
    assert rebuild_cost(CACHE_FRIENDLY, {"requirements.txt"}) == 102


def test_run_steps_are_not_invalidated_directly():
    steps = [{"cmd": "RUN", "files": ["app.py"], "cost": 50}]
    assert rebuild_cost(steps, {"app.py"}) == 0


def test_add_behaves_like_copy():
    steps = [
        {"cmd": "ADD", "files": ["data.tar"], "cost": 3},
        {"cmd": "RUN", "files": [], "cost": 7},
    ]
    assert rebuild_cost(steps, {"data.tar"}) == 10


def test_cheaper_ordering_is_really_cheaper_for_a_code_edit():
    edit = {"model.py"}
    assert rebuild_cost(CACHE_FRIENDLY, edit) < rebuild_cost(NAIVE, edit)
