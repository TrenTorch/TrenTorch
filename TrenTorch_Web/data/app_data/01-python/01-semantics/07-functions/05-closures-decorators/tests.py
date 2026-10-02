"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
make_multiplier = _module.make_multiplier
make_prefixer = _module.make_prefixer
make_counter = _module.make_counter
add_call_count = _module.add_call_count
run_with_message = _module.run_with_message
decorate_result = _module.decorate_result


def test_retained_value():
    double = make_multiplier(2)
    assert double(7) == 14


def test_independent_closures():
    double = make_multiplier(2)
    triple = make_multiplier(3)
    assert double(5) == 10
    assert triple(5) == 15


def test_multiple_calls_use_same_retained_value():
    add_five = make_prefixer("ERROR: ")
    assert add_five("disk full") == "ERROR: disk full"
    assert add_five("timeout") == "ERROR: timeout"


def test_counter_state():
    counter = make_counter(10)
    assert counter() == 11
    assert counter() == 12


def test_independent_counter_state():
    a = make_counter(0)
    b = make_counter(0)
    assert a() == 1
    assert a() == 2
    assert b() == 1


def test_no_global_state_across_factory_calls():
    m1 = make_multiplier(10)
    m2 = make_multiplier(100)
    assert m1(1) == 10
    assert m2(1) == 100
    assert m1(1) == 10


def test_original_function_called_exactly_once():
    calls = []

    def record(x):
        calls.append(x)
        return x

    run_with_message(record, "msg", 5)
    assert calls == [5]


def test_return_value_preserved():
    def add(a, b):
        return a + b

    wrapped = add_call_count(add)
    assert wrapped(2, 3) == 5


def test_positional_and_keyword_forwarding():
    def add(a, b):
        return a + b

    assert run_with_message(add, "msg", 2, b=3) == 5
    wrapped = add_call_count(add)
    assert wrapped(2, b=3) == 5


def test_independent_call_counts():
    def add(a, b):
        return a + b

    def sub(a, b):
        return a - b

    wrapped_add = add_call_count(add)
    wrapped_sub = add_call_count(sub)
    wrapped_add(1, 1)
    wrapped_add(1, 1)
    wrapped_sub(1, 1)
    assert wrapped_add.calls == 2
    assert wrapped_sub.calls == 1


def test_arguments_not_modified():
    def add(a, b):
        return a + b

    args = (2, 3)
    run_with_message(add, "msg", *args)
    assert args == (2, 3)


def test_result_transformation():
    def name(x):
        return x

    wrapped = decorate_result(name, "Name: ")
    assert wrapped("Ada") == "Name: Ada"
