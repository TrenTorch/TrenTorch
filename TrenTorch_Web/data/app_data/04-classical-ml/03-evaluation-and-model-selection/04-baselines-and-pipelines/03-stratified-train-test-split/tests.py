"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
stratified_train_test_split = _module.stratified_train_test_split


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def _labels():
    # 30 zeros, 10 ones: a 75/25 class mix
    return np.array([0] * 30 + [1] * 10)


def test_every_index_appears_exactly_once():
    train, test = stratified_train_test_split(_labels(), test_fraction=0.25, seed=1)
    combined = np.sort(np.concatenate([train, test]))
    assert np.array_equal(combined, np.arange(40))


def test_train_and_test_are_disjoint():
    train, test = stratified_train_test_split(_labels(), test_fraction=0.3, seed=2)
    assert len(np.intersect1d(train, test)) == 0


def test_each_class_contributes_the_rounded_test_count():
    y = _labels()
    _, test = stratified_train_test_split(y, test_fraction=0.25, seed=3)
    assert np.sum(y[test] == 0) == round(0.25 * 30)
    assert np.sum(y[test] == 1) == round(0.25 * 10)


def test_class_proportions_match_on_both_sides():
    y = _labels()
    # 0.2 * 10 and 0.2 * 30 are whole numbers, so both sides match exactly
    train, test = stratified_train_test_split(y, test_fraction=0.2, seed=4)
    assert np.isclose(np.mean(y[test] == 1), np.mean(y == 1))
    assert np.isclose(np.mean(y[train] == 1), np.mean(y == 1))


def test_outputs_are_sorted():
    train, test = stratified_train_test_split(_labels(), seed=5)
    assert np.all(np.diff(train) > 0)
    assert np.all(np.diff(test) > 0)


def test_same_seed_gives_the_same_split():
    a = stratified_train_test_split(_labels(), seed=6)
    b = stratified_train_test_split(_labels(), seed=6)
    assert np.array_equal(a[0], b[0])
    assert np.array_equal(a[1], b[1])


def test_different_seeds_change_which_examples_are_selected():
    _, test_a = stratified_train_test_split(_labels(), seed=7)
    _, test_b = stratified_train_test_split(_labels(), seed=8)
    assert not np.array_equal(test_a, test_b)


def test_zero_fraction_puts_everything_in_train():
    train, test = stratified_train_test_split(_labels(), test_fraction=0.0, seed=9)
    assert test.size == 0
    assert train.size == 40


def test_full_fraction_puts_everything_in_test():
    train, test = stratified_train_test_split(_labels(), test_fraction=1.0, seed=10)
    assert train.size == 0
    assert test.size == 40


def test_fraction_outside_zero_to_one_raises():
    assert _raises_value_error(stratified_train_test_split, _labels(), 1.5, 0)
    assert _raises_value_error(stratified_train_test_split, _labels(), -0.1, 0)


def test_returns_integer_index_arrays():
    train, test = stratified_train_test_split(_labels(), seed=11)
    assert np.issubdtype(train.dtype, np.integer)
    assert np.issubdtype(test.dtype, np.integer)


def test_string_labels_are_stratified_too():
    y = np.array(["a"] * 8 + ["b"] * 4)
    _, test = stratified_train_test_split(y, test_fraction=0.5, seed=12)
    assert np.sum(y[test] == "a") == 4
    assert np.sum(y[test] == "b") == 2


def test_does_not_modify_the_labels():
    y = _labels()
    y_before = y.copy()
    stratified_train_test_split(y, seed=13)
    assert np.array_equal(y, y_before)
