"""
pytest data/app_data/01-classical-ml/06-unsupervised/03-pca-projection/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/06-unsupervised/{Path(__file__).resolve().parent.name}")
pca_fit = _module.pca_fit
pca_transform = _module.pca_transform


def test_components_are_unit_vectors():
    rng = np.random.default_rng(0)
    input = rng.normal(size=(20, 4))
    model = pca_fit(input, n_components=3)
    norms = np.linalg.norm(model["components"], axis=1)
    assert np.allclose(norms, 1.0)


def test_recovers_the_obvious_direction_of_variance():
    # All variance lies exactly along the line y=x -- the first
    # component must point along (1,1)/sqrt(2) (or its negation before
    # sign-fixing), and explain essentially all the variance.
    input = np.array([[-2.0, -2.0], [-1.0, -1.0], [0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
    model = pca_fit(input, n_components=2)
    first_component = model["components"][0]
    assert np.isclose(abs(first_component[0]), abs(first_component[1]), atol=1e-6)
    assert model["explained_variance"][0] > 100 * model["explained_variance"][1]


def test_sign_convention_makes_the_largest_magnitude_entry_positive():
    rng = np.random.default_rng(1)
    input = rng.normal(size=(30, 5))
    model = pca_fit(input, n_components=3)
    for component in model["components"]:
        max_idx = np.argmax(np.abs(component))
        assert component[max_idx] > 0


def test_projection_shape_matches_n_components():
    rng = np.random.default_rng(2)
    input = rng.normal(size=(25, 6))
    model = pca_fit(input, n_components=2)
    projected = pca_transform(model, input)
    assert projected.shape == (25, 2)


def test_full_rank_projection_reconstructs_exactly():
    # With n_components == n_features, PCA is a pure (lossless)
    # rotation -- projecting then un-projecting must recover the
    # original centered data exactly.
    rng = np.random.default_rng(3)
    input = rng.normal(size=(20, 4))
    model = pca_fit(input, n_components=4)
    projected = pca_transform(model, input)
    reconstructed = projected @ model["components"] + model["mean"]
    assert np.allclose(reconstructed, input, atol=1e-8)


def test_transform_uses_the_fitted_mean_not_the_new_datas_own_mean():
    # Directly targets a mutant that recomputes the mean inside
    # pca_transform instead of using the stored one: projecting the
    # exact training data must exactly match the projection obtained
    # during fitting.
    rng = np.random.default_rng(4)
    input = rng.normal(size=(15, 3))
    model = pca_fit(input, n_components=2)
    training_projection = (input - model["mean"]) @ model["components"].T
    assert np.allclose(pca_transform(model, input), training_projection)


def test_matches_real_sklearn_pca_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(3)
    #   X = rng.normal(size=(30, 4)) @ rng.normal(size=(4, 4))
    #   pca = PCA(n_components=2)
    #   pca.fit(X)
    #   pca.components_, pca.explained_variance_  # baked below
    #
    # This test needs no scikit-learn installed to run.
    input = np.array(
        [
            [-6.385878, -0.358192, -2.15539, 0.087012], [-3.509019, -0.90519, -3.298568, 1.700718],
            [8.116935, 0.491604, 2.29126, -0.513352], [-2.874689, -0.107803, -2.557068, 0.59598],
            [0.763857, 0.534382, 0.847825, -0.891713], [4.198397, 0.491044, 1.173134, -0.663908],
            [4.743295, 1.695312, 2.649439, -2.295897], [0.786934, -0.423269, -0.893456, 0.763132],
            [0.357125, -1.299046, 1.617347, 0.997941], [3.490887, 2.709861, -3.1631, -1.717207],
            [0.588292, 0.186062, -1.678982, 0.057498], [2.196482, 0.42444, 3.009089, -1.014706],
            [1.90313, 0.226174, -0.813126, -0.090424], [0.393848, -0.10536, -0.999703, 0.181611],
            [-4.211342, 0.421136, -0.220195, -0.661302], [-0.112967, -0.030827, -0.203708, 0.49604],
            [1.144252, 1.395854, 1.921471, -1.450172], [1.786191, 2.566475, -0.943606, -2.214767],
            [-3.170519, 0.077108, -1.938002, -0.237127], [-1.744971, -0.0002, -3.050967, 0.169035],
            [1.003327, -1.862777, 3.394317, 1.131216], [-2.905374, -0.096299, -2.774933, 0.460651],
            [-5.319187, -0.990499, -2.361145, 1.082637], [-0.90729, 0.187251, -3.861724, 0.441789],
            [3.780469, 0.15029, 2.291837, -0.488262], [0.325509, -0.649415, 1.108163, 0.64195],
            [0.752893, 0.085597, 0.734752, -0.011635], [7.352149, -0.789232, 6.270379, -0.090441],
            [0.125303, 0.815988, -0.380692, -0.353931], [6.7635, 3.445452, 0.303431, -3.284407],
        ]
    )
    expected_components = np.array(
        [
            [0.8639352734116786, 0.10622812100020129, 0.4680085229043209, -0.1526415806809228],
            [-0.28714003229386326, -0.495152452813491, 0.7503191781342452, 0.3307503306891984],
        ]
    )
    expected_variance = np.array([16.251015535467435, 3.48853489302128])

    model = pca_fit(input, n_components=2)
    assert np.allclose(model["components"], expected_components, atol=1e-6)
    assert np.allclose(model["explained_variance"], expected_variance, atol=1e-6)
