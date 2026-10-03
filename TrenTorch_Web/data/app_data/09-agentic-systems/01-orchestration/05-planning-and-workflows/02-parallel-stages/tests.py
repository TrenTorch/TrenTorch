"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
parallel_stages = _module.parallel_stages
critical_path_length = _module.critical_path_length
DIAMOND = {"d": ["b", "c"], "b": ["a"], "c": ["a"], "a": []}


def test_1_stages_of_a_diamond():
    assert parallel_stages(DIAMOND) == [["a"], ["b", "c"], ["d"]]


def test_2_independent_tasks_share_stage_zero():
    assert parallel_stages({"x": [], "y": [], "z": []}) == [["x", "y", "z"]]


def test_3_stage_is_longest_dependency_chain_not_shortest():
    tasks = {"a": [], "b": ["a"], "c": ["b"], "d": ["a", "c"]}
    assert parallel_stages(tasks) == [["a"], ["b"], ["c"], ["d"]]


def test_4_empty_plan():
    assert parallel_stages({}) == [] and critical_path_length({}, {}) == 0.0


def test_5_critical_path_hand_computed():
    dur = {"a": 2.0, "b": 5.0, "c": 1.0, "d": 3.0}
    # a->b->d = 2+5+3 = 10 ; a->c->d = 2+1+3 = 6
    assert critical_path_length(DIAMOND, dur) == 10.0


def test_6_parallel_branches_do_not_add_up():
    tasks = {"s": [], "p1": ["s"], "p2": ["s"]}
    assert critical_path_length(tasks, {"s": 1.0, "p1": 4.0, "p2": 4.0}) == 5.0


def test_7_input_untouched_and_total_tasks_preserved():
    tasks = {"e": ["c", "d"], "d": ["b"], "c": ["a"], "b": [], "a": []}
    snap = {k: list(v) for k, v in tasks.items()}
    stages = parallel_stages(tasks)
    assert sorted(sum(stages, [])) == sorted(tasks) and tasks == snap
