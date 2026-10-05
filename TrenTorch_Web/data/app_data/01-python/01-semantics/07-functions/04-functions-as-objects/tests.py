"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
alias_and_call = _module.alias_and_call
apply_selected = _module.apply_selected
same_function = _module.same_function
apply_once = _module.apply_once
apply_twice = _module.apply_twice
apply_n_times = _module.apply_n_times
transform_all = _module.transform_all
make_square_function = _module.make_square_function
make_offset_function = _module.make_offset_function
apply_lambda = _module.apply_lambda


def test_alias_preserves_the_function_object():
    calls = []

    def record(x):
        calls.append(x)
        return x * 2

    result = alias_and_call(record, 5)
    assert result == 10
    assert calls == [5]


def test_calling_through_an_alias():
    assert alias_and_call(lambda x: x * 2, 5) == 10


def test_function_selection_by_index():
    assert apply_selected([abs, str], 0, -7) == 7
    assert apply_selected([abs, str], 1, 42) == "42"
    assert apply_selected([abs, str], -1, 42) == "42"


def test_identity_rather_than_result_equality():
    def f(x):
        return x

    def g(x):
        return x

    assert same_function(f, f) is True
    assert same_function(f, g) is False
    a = f
    assert same_function(f, a) is True


def test_input_functions_untouched():
    functions = [abs, str]
    apply_selected(functions, 0, -1)
    assert functions == [abs, str]


def test_function_receives_correct_value():
    assert apply_once(abs, -8) == 8
    assert apply_once(str, 42) == "42"


def test_sequential_application():
    def add_one(x):
        return x + 1

    assert apply_twice(add_one, 5) == 7


def test_zero_and_negative_counts():
    assert apply_n_times(lambda x: x * 2, 3, 0) == 3
    assert apply_n_times(lambda x: x * 2, 3, -5) == 3


def test_apply_n_times_multiple():
    def double(x):
        return x * 2

    assert apply_n_times(double, 3, 3) == 24


def test_order_preservation():
    assert transform_all([1, -2, 3], abs) == [1, 2, 3]


def test_input_list_unchanged():
    values = [1, -2, 3]
    transform_all(values, abs)
    assert values == [1, -2, 3]


def test_different_supplied_functions():
    assert transform_all(["a", "bb"], len) == [1, 2]
    assert apply_once(len, "hello") == 5


def test_returned_object_is_callable():
    square = make_square_function()
    assert callable(square)


def test_lambda_computation():
    square = make_square_function()
    assert square(6) == 36
    assert square(0) == 0


def test_captured_offset():
    add_five = make_offset_function(5)
    add_ten = make_offset_function(10)
    assert add_five(10) == 15
    assert add_ten(10) == 20


def test_works_with_externally_supplied_functions():
    assert apply_lambda([1, 2, 3], abs) == [1, 2, 3]
    assert apply_lambda([1, 2, 3], lambda x: x * 2) == [2, 4, 6]


def test_input_preservation():
    values = [1, 2, 3]
    apply_lambda(values, lambda x: x * 2)
    assert values == [1, 2, 3]
