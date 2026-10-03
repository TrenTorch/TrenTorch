"""pytest tests.py"""

from _load import load_solution

generate_pairs = load_solution(__file__).generate_pairs


def test_1_single_template_multiple_variable_sets():
    templates = ["What is {n1} + {n2}?"]
    variable_sets = [{"n1": "2", "n2": "3"}, {"n1": "5", "n2": "7"}]
    assert generate_pairs(templates, variable_sets) == [
        "What is 2 + 3?",
        "What is 5 + 7?",
    ]


def test_2_multiple_templates_template_major_order():
    templates = ["Add {a} and {b}", "Multiply {a} by {b}"]
    variable_sets = [{"a": "1", "b": "2"}]
    assert generate_pairs(templates, variable_sets) == [
        "Add 1 and 2",
        "Multiply 1 by 2",
    ]


def test_3_cross_product_size():
    templates = ["T1: {x}", "T2: {x}"]
    variable_sets = [{"x": "a"}, {"x": "b"}, {"x": "c"}]
    result = generate_pairs(templates, variable_sets)
    assert len(result) == 6
    assert result == ["T1: a", "T1: b", "T1: c", "T2: a", "T2: b", "T2: c"]


def test_4_empty_variable_sets_returns_empty_list():
    assert generate_pairs(["Hello {name}"], []) == []


def test_5_empty_templates_returns_empty_list():
    assert generate_pairs([], [{"x": "1"}]) == []
