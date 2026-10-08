"""
pytest data/app_data/12-research-papers/06-computer-vision/06-clip/03-zero-shot/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-clip-zero-shot")
zero_shot_predict = _module.zero_shot_predict


import numpy as np


def test_1_picks_the_most_similar_prompt():
    classes = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert zero_shot_predict(np.array([0.1, 0.9]), classes) == 1


def test_2_scale_of_the_image_embedding_does_not_matter():
    classes = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert zero_shot_predict(np.array([5.0, 0.0]), classes) == 0


def test_3_returns_a_python_int():
    assert isinstance(zero_shot_predict(np.ones(2), np.eye(2)), int)


def test_4_single_class_is_always_chosen():
    assert zero_shot_predict(np.ones(3), np.ones((1, 3))) == 0


def test_5_scale_of_class_embeddings_does_not_matter():
    classes = np.array([[2.0, 0.0], [0.0, 9.0]])
    assert zero_shot_predict(np.array([1.0, 0.1]), classes) == 0


def test_6_does_not_mutate_inputs():
    img = np.array([3.0, 4.0])
    zero_shot_predict(img, np.eye(2))
    np.testing.assert_array_equal(img, [3.0, 4.0])

