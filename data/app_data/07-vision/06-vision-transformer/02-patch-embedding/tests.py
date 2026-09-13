"""
pytest data/app_data/07-vision/06-vision-transformer/02-patch-embedding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

patch_embedding = load_solution(
    f"07-vision/06-vision-transformer/{Path(__file__).resolve().parent.name}"
).patch_embedding
linear = load_solution("01-classical-ml/01-linear-regression/01-hypothesis-function").linear


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_shape_is_num_patches_by_d_model():
    rng = np.random.default_rng(0)
    patches = rng.normal(size=(4, 8))
    weight = rng.normal(size=(6, 8))
    bias = rng.normal(size=6)
    out = patch_embedding(patches, weight, bias)
    assert out.shape == (4, 6)


def test_02_matches_the_reused_linear_function_directly():
    rng = np.random.default_rng(1)
    patches = rng.normal(size=(5, 12))
    weight = rng.normal(size=(4, 12))
    bias = rng.normal(size=4)
    out = patch_embedding(patches, weight, bias)
    assert np.allclose(out, linear(patches, weight, bias))


# --- Shape / general-case coverage -----------------------------------


def test_03_each_patch_embedded_independently():
    rng = np.random.default_rng(2)
    patches = rng.normal(size=(3, 6))
    weight = rng.normal(size=(2, 6))
    bias = rng.normal(size=2)
    out = patch_embedding(patches, weight, bias)
    single = patch_embedding(patches[1:2], weight, bias)
    assert np.allclose(out[1], single[0])


def test_04_zero_weight_gives_bias_broadcast_to_every_patch():
    rng = np.random.default_rng(3)
    patches = rng.normal(size=(4, 5))
    weight = np.zeros((3, 5))
    bias = np.array([1.0, -2.0, 0.5])
    out = patch_embedding(patches, weight, bias)
    assert np.allclose(out, np.tile(bias, (4, 1)))


# --- Parameter handling -------------------------------------------------


def test_05_single_patch_input():
    rng = np.random.default_rng(4)
    patches = rng.normal(size=(1, 8))
    weight = rng.normal(size=(4, 8))
    bias = rng.normal(size=4)
    out = patch_embedding(patches, weight, bias)
    assert out.shape == (1, 4)


# --- Edge cases ---------------------------------------------------------


def test_06_identity_weight_and_zero_bias_reproduces_the_patches():
    patches = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    weight = np.eye(3)
    bias = np.zeros(3)
    out = patch_embedding(patches, weight, bias)
    assert np.allclose(out, patches)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(5)
    patches = rng.normal(size=(3, 6))
    weight = rng.normal(size=(4, 6))
    bias = rng.normal(size=4)
    p_copy, w_copy, b_copy = patches.copy(), weight.copy(), bias.copy()
    patch_embedding(patches, weight, bias)
    assert np.array_equal(patches, p_copy)
    assert np.array_equal(weight, w_copy)
    assert np.array_equal(bias, b_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_linear_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   patches = torch.randn(4, 8)
    #   weight = torch.randn(6, 8)
    #   bias = torch.randn(6)
    #   out = torch.nn.functional.linear(patches, weight, bias)
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    patches = np.array(
        [
            [-0.1813, -0.3241, 0.7616, -0.9424, -0.6432, 1.2079, -1.2855, -0.6099],
            [0.6995, 0.9954, 0.2515, 0.7539, -0.1812, 0.2017, -0.6194, -0.9761],
            [0.4755, -0.3544, 0.3759, 1.1238, -0.0369, 1.0072, -0.1696, 2.0859],
            [0.6673, -0.4191, -0.4144, -1.1207, 2.0851, -1.2788, -2.1060, -0.2033],
        ]
    )
    weight = np.array(
        [
            [-0.7428, -0.3428, -0.1913, -0.6468, 0.0076, -2.1827, -1.2434, 0.4862],
            [0.5422, -2.0742, -0.0359, 0.8048, 0.6246, -0.4893, 0.3736, -0.1829],
            [0.6572, -0.4997, 2.8876, -0.0574, 0.0205, -1.3112, -0.2605, 0.3284],
            [1.4427, -0.3629, 0.3957, 0.9343, -0.4292, 0.1507, 1.0873, -0.5364],
            [-0.0017, 0.3502, -0.6820, 0.1160, 1.9558, -0.8680, -2.1850, -0.8094],
            [-0.5262, -0.9421, -1.8529, 0.9826, 1.4322, 0.8042, 0.0580, -0.8488],
        ]
    )
    bias = np.array([1.0143, 0.6943, 0.5169, -0.3033, 0.7950, 0.1610])
    expected = np.array(
        [
            [0.3844, -0.8792, 1.3505, -1.6388, 1.0491, -1.2821],
            [-0.5283, -0.6581, 0.7348, 1.1067, 2.6723, -0.1746],
            [-0.9900, 1.6176, 1.4352, 0.5744, -1.7202, -0.3708],
            [6.7932, 2.2166, 2.2341, -3.6680, 10.7537, 1.8792],
        ]
    )

    out = patch_embedding(patches, weight, bias)
    assert np.allclose(out, expected, atol=1e-2)
