"""
pytest data/app_data/01-classical-ml/06-unsupervised/09-tsne-umap/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gaussian_affinities = load_solution(
    f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}"
).gaussian_affinities


def test_diagonal_is_zero():
    input = np.array([[0.0], [1.0], [2.0]])
    result = gaussian_affinities(input, sigma=1.0)
    assert np.allclose(np.diag(result), 0.0)


def test_rows_sum_to_one():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(10, 3))
    result = gaussian_affinities(input, sigma=1.0)
    assert np.allclose(result.sum(axis=1), 1.0)


def test_matches_hand_computation():
    input = np.array([[0.0], [1.0], [3.0]])
    result = gaussian_affinities(input, sigma=1.0)
    # row 0: distances to 1 and 3 are 1 and 3
    unnorm = np.array([np.exp(-1**2 / 2), np.exp(-3**2 / 2)])
    expected = unnorm / unnorm.sum()
    assert np.isclose(result[0, 1], expected[0])
    assert np.isclose(result[0, 2], expected[1])


def test_closer_points_get_higher_affinity():
    input = np.array([[0.0], [1.0], [10.0]])
    result = gaussian_affinities(input, sigma=2.0)
    assert result[0, 1] > result[0, 2]


def test_smaller_sigma_concentrates_more_on_the_nearest_neighbor():
    input = np.array([[0.0], [1.0], [5.0]])
    wide = gaussian_affinities(input, sigma=10.0)
    narrow = gaussian_affinities(input, sigma=0.5)
    # a smaller sigma should make row 0's distribution more peaked on
    # its nearest neighbor (index 1) relative to the far point (index 2)
    assert narrow[0, 1] > wide[0, 1]


def test_diagonal_exclusion_is_not_dropped():
    # Directly targets a mutant that forgets to zero the diagonal:
    # distance-to-self is always 0, the smallest possible distance, so
    # without excluding it, p[i,i] would dominate every row and every
    # OTHER affinity would be pulled down noticeably by the extra mass
    # in the normalization sum.
    input = np.array([[0.0], [1.0]])
    result = gaussian_affinities(input, sigma=1.0)
    assert result[0, 0] == 0.0
    assert result[0, 1] == 1.0  # only one other point -- it gets all the mass
