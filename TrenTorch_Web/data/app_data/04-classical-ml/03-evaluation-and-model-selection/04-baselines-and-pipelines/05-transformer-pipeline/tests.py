"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
MinMaxScaler = _module.MinMaxScaler
Pipeline = _module.Pipeline


def test_fit_transform_maps_the_training_range_to_zero_and_one():
    X = np.array([[1.0, 10.0], [3.0, 30.0], [5.0, 50.0]])
    scaled = MinMaxScaler().fit_transform(X)
    assert np.allclose(scaled.min(axis=0), 0.0)
    assert np.allclose(scaled.max(axis=0), 1.0)


def test_transform_uses_the_training_minimum_and_maximum():
    scaler = MinMaxScaler().fit(np.array([[0.0], [10.0]]))
    assert np.allclose(scaler.transform(np.array([[5.0], [20.0]])), [[0.5], [2.0]])


def test_values_outside_the_training_range_are_not_clipped():
    scaler = MinMaxScaler().fit(np.array([[0.0], [1.0]]))
    assert scaler.transform(np.array([[-1.0]]))[0, 0] < 0.0
    assert scaler.transform(np.array([[3.0]]))[0, 0] > 1.0


def test_fit_returns_the_scaler_itself():
    scaler = MinMaxScaler()
    assert scaler.fit(np.array([[1.0], [2.0]])) is scaler


def test_zero_range_column_maps_every_value_to_zero():
    scaler = MinMaxScaler().fit(np.array([[4.0], [4.0]]))
    assert np.allclose(scaler.transform(np.array([[4.0], [9.0], [-2.0]])), 0.0)


def test_fit_transform_equals_fit_then_transform():
    X = np.array([[2.0, 1.0], [4.0, 3.0], [6.0, 7.0]])
    assert np.allclose(MinMaxScaler().fit_transform(X), MinMaxScaler().fit(X).transform(X))


def test_pipeline_with_one_step_matches_that_step():
    X = np.array([[1.0], [5.0], [3.0]])
    assert np.allclose(Pipeline([MinMaxScaler()]).fit_transform(X), MinMaxScaler().fit_transform(X))


def test_pipeline_transform_uses_the_fitted_training_statistics():
    pipe = Pipeline([MinMaxScaler()])
    pipe.fit_transform(np.array([[0.0], [10.0]]))
    assert np.allclose(pipe.transform(np.array([[5.0]])), [[0.5]])


def test_pipeline_runs_steps_in_order():
    class AddOne:
        def fit_transform(self, X):
            return X + 1.0

        def transform(self, X):
            return X + 1.0

    class Double:
        def fit_transform(self, X):
            return X * 2.0

        def transform(self, X):
            return X * 2.0

    X = np.array([[1.0]])
    assert np.allclose(Pipeline([AddOne(), Double()]).fit_transform(X), [[4.0]])
    assert np.allclose(Pipeline([Double(), AddOne()]).fit_transform(X), [[3.0]])


def test_later_steps_fit_on_the_output_of_earlier_steps():
    class Recorder:
        def __init__(self):
            self.seen = None

        def fit_transform(self, X):
            self.seen = np.array(X, copy=True)
            return X

        def transform(self, X):
            return X

    recorder = Recorder()
    Pipeline([MinMaxScaler(), recorder]).fit_transform(np.array([[0.0], [4.0]]))
    assert np.allclose(recorder.seen, [[0.0], [1.0]])


def test_empty_pipeline_returns_its_input_unchanged():
    X = np.array([[1.0, 2.0]])
    assert np.array_equal(Pipeline([]).fit_transform(X), X)
    assert np.array_equal(Pipeline([]).transform(X), X)


def test_does_not_modify_the_input_matrix():
    X = np.array([[1.0], [3.0]])
    X_before = X.copy()
    Pipeline([MinMaxScaler()]).fit_transform(X)
    assert np.array_equal(X, X_before)


def test_stores_steps_as_a_list():
    scaler = MinMaxScaler()
    pipe = Pipeline((scaler,))
    assert isinstance(pipe.steps, list)
    assert pipe.steps[0] is scaler
