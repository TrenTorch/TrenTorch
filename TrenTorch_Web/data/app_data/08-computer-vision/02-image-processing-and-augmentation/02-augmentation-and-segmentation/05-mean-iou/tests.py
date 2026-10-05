"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
confusion_matrix = _module.confusion_matrix
mean_iou = _module.mean_iou


def test_1_confusion_matrix_hand_computed():
    pred = np.array([0, 1, 1, 2, 2, 2])
    target = np.array([0, 0, 1, 2, 2, 1])
    expected = np.array([[1, 1, 0], [0, 1, 1], [0, 0, 2]])
    assert np.array_equal(confusion_matrix(pred, target, 3), expected)


def test_2_total_equals_number_of_pixels():
    rng = np.random.RandomState(0)
    p, t = rng.randint(0, 4, (5, 6)), rng.randint(0, 4, (5, 6))
    assert confusion_matrix(p, t, 4).sum() == 30


def test_3_miou_hand_computed():
    conf = np.array([[1, 1, 0], [0, 1, 1], [0, 0, 2]])
    miou, ious = mean_iou(conf)
    # class0: 1/(2+1-1)=0.5 ; class1: 1/(2+2-1)=1/3 ; class2: 2/(2+3-2)=2/3
    assert np.allclose(ious, [0.5, 1 / 3, 2 / 3]) and np.isclose(miou, np.mean([0.5, 1 / 3, 2 / 3]))


def test_4_perfect_prediction_gives_one():
    t = np.random.RandomState(1).randint(0, 3, (8, 8))
    miou, _ = mean_iou(confusion_matrix(t, t, 3))
    assert np.isclose(miou, 1.0)


def test_5_absent_class_is_nan_and_ignored():
    conf = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 0]])
    miou, ious = mean_iou(conf)
    assert np.isnan(ious[2]) and np.isclose(miou, 1.0)


def test_6_missed_class_scores_zero_not_nan():
    conf = np.array([[0, 3], [0, 3]])  # class 0 exists but is never predicted
    _, ious = mean_iou(conf)
    assert ious[0] == 0.0


def test_7_iou_equals_tp_over_tp_fp_fn_and_inputs_untouched():
    rng = np.random.RandomState(2)
    p, t = rng.randint(0, 3, 200), rng.randint(0, 3, 200)
    sp = p.copy()
    _, ious = mean_iou(confusion_matrix(p, t, 3))
    for c in range(3):
        tp = ((p == c) & (t == c)).sum()
        fp = ((p == c) & (t != c)).sum()
        fn = ((p != c) & (t == c)).sum()
        assert np.isclose(ious[c], tp / (tp + fp + fn))
    assert np.array_equal(p, sp)
