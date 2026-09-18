"""
pytest data/app_data/01-classical-ml/08-tabular-foundation-models/04-in-context-prediction/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"01-classical-ml/08-tabular-foundation-models/{Path(__file__).resolve().parent.name}"
)
build_incontext_table = _module.build_incontext_table
in_context_predict = _module.in_context_predict
two_way_attention_block = load_solution(
    "01-classical-ml/08-tabular-foundation-models/03-two-way-attention-block"
).two_way_attention_block


def test_table_shape_and_layout_matches_hand_computation():
    train_features = np.array([[1.0, 2.0], [3.0, 4.0]])
    train_targets = np.array([10.0, 20.0])
    query_features = np.array([[5.0, 6.0]])
    table = build_incontext_table(train_features, train_targets, query_features)

    assert table.shape == (3, 3, 1)
    assert np.allclose(table[0, :, 0], [1.0, 2.0, 10.0])
    assert np.allclose(table[1, :, 0], [3.0, 4.0, 20.0])
    assert np.allclose(table[2, :2, 0], [5.0, 6.0])


def test_query_target_column_is_masked_to_zero():
    train_features = np.array([[1.0]])
    train_targets = np.array([99.0])
    query_features = np.array([[2.0], [3.0]])
    table = build_incontext_table(train_features, train_targets, query_features)
    assert np.allclose(table[1:, -1, 0], 0.0)


def test_predict_output_shape_matches_number_of_query_rows():
    rng = np.random.default_rng(0)
    train_features = rng.normal(size=(5, 3))
    train_targets = rng.normal(size=5)
    query_features = rng.normal(size=(4, 3))
    row_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))
    predictions = in_context_predict(
        train_features, train_targets, query_features, row_weights, col_weights
    )
    assert predictions.shape == (4,)


def test_predict_matches_manual_table_build_and_forward_pass():
    rng = np.random.default_rng(1)
    train_features = rng.normal(size=(4, 2))
    train_targets = rng.normal(size=4)
    query_features = rng.normal(size=(3, 2))
    row_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))

    manual_table = build_incontext_table(train_features, train_targets, query_features)
    manual_output = two_way_attention_block(manual_table, row_weights, col_weights)
    manual_predictions = manual_output[4:, -1, 0]

    predictions = in_context_predict(
        train_features, train_targets, query_features, row_weights, col_weights
    )
    assert np.allclose(predictions, manual_predictions)


def test_no_training_loop_needed_different_datasets_give_immediate_different_predictions():
    # The actual point of the exercise: the SAME fixed weights, applied
    # to two completely different train/query datasets in two separate
    # single calls, give different predictions immediately -- there is
    # no per-dataset fitting step for this function to have skipped.
    rng = np.random.default_rng(2)
    row_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))

    train_features_a = rng.normal(size=(5, 2))
    train_targets_a = rng.normal(size=5)
    query_features = rng.normal(size=(2, 2))
    predictions_a = in_context_predict(
        train_features_a, train_targets_a, query_features, row_weights, col_weights
    )

    train_features_b = rng.normal(size=(5, 2))
    train_targets_b = rng.normal(size=5)
    predictions_b = in_context_predict(
        train_features_b, train_targets_b, query_features, row_weights, col_weights
    )

    assert not np.allclose(predictions_a, predictions_b)


def test_reads_the_query_rows_not_the_training_rows():
    # Directly targets a mutant that slices the wrong rows (e.g. reads
    # from the start of the output instead of after n_train): training
    # rows have a real, nonzero target BEFORE the forward pass even
    # runs, reading their post-attention target-column value instead of
    # the query rows' is a real, plausible off-by-slice bug.
    rng = np.random.default_rng(3)
    train_features = rng.normal(size=(3, 2))
    train_targets = np.array([100.0, 200.0, 300.0])  # distinctly large, easy to spot if leaked
    query_features = rng.normal(size=(2, 2))
    row_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))
    col_weights = tuple(rng.normal(size=(1, 1)) for _ in range(3))

    predictions = in_context_predict(
        train_features, train_targets, query_features, row_weights, col_weights
    )
    assert predictions.shape == (2,)
    # predictions should not literally equal any of the raw training targets
    assert not np.any(np.isin(np.round(predictions, 6), [100.0, 200.0, 300.0]))
