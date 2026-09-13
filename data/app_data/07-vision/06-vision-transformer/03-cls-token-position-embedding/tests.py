"""
pytest data/app_data/07-vision/06-vision-transformer/03-cls-token-position-embedding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

add_cls_token_and_position_embedding = load_solution(
    f"07-vision/06-vision-transformer/{Path(__file__).resolve().parent.name}"
).add_cls_token_and_position_embedding


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_output_has_one_more_sequence_position_than_input():
    rng = np.random.default_rng(0)
    patch_embeddings = rng.normal(size=(4, 6))
    cls_token = rng.normal(size=(1, 6))
    position_embedding = rng.normal(size=(5, 6))
    out = add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert out.shape == (5, 6)


def test_02_zero_position_embedding_leaves_cls_and_patches_concatenated_unchanged():
    rng = np.random.default_rng(1)
    patch_embeddings = rng.normal(size=(3, 4))
    cls_token = rng.normal(size=(1, 4))
    position_embedding = np.zeros((4, 4))
    out = add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert np.allclose(out[0], cls_token[0])
    assert np.allclose(out[1:], patch_embeddings)


# --- Shape / general-case coverage -----------------------------------


def test_03_cls_token_occupies_position_zero():
    cls_token = np.array([[9.0, 9.0]])
    patch_embeddings = np.array([[1.0, 1.0], [2.0, 2.0]])
    position_embedding = np.zeros((3, 2))
    out = add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert np.allclose(out[0], [9.0, 9.0])
    assert np.allclose(out[1], [1.0, 1.0])
    assert np.allclose(out[2], [2.0, 2.0])


def test_04_position_embedding_is_added_elementwise_per_position():
    patch_embeddings = np.zeros((2, 3))
    cls_token = np.zeros((1, 3))
    position_embedding = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    out = add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert np.allclose(out, position_embedding)


# --- Parameter handling -------------------------------------------------


def test_05_single_patch_sequence():
    patch_embeddings = np.array([[1.0, 2.0]])
    cls_token = np.array([[0.5, 0.5]])
    position_embedding = np.zeros((2, 2))
    out = add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert out.shape == (2, 2)


# --- Edge cases ---------------------------------------------------------


def test_06_larger_d_model_works_the_same_way():
    rng = np.random.default_rng(2)
    patch_embeddings = rng.normal(size=(9, 16))
    cls_token = rng.normal(size=(1, 16))
    position_embedding = rng.normal(size=(10, 16))
    out = add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert out.shape == (10, 16)


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(3)
    patch_embeddings = rng.normal(size=(4, 5))
    cls_token = rng.normal(size=(1, 5))
    position_embedding = rng.normal(size=(5, 5))
    p_copy, c_copy, pos_copy = patch_embeddings.copy(), cls_token.copy(), position_embedding.copy()
    add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert np.array_equal(patch_embeddings, p_copy)
    assert np.array_equal(cls_token, c_copy)
    assert np.array_equal(position_embedding, pos_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_cat_plus_add_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   patch_embeds = torch.randn(4, 3)
    #   cls_token = torch.randn(1, 3)
    #   pos_embed = torch.randn(5, 3)
    #   seq = torch.cat([cls_token, patch_embeds], dim=0)
    #   out = seq + pos_embed
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    patch_embeddings = np.array(
        [
            [1.4219, -0.2314, 0.3739],
            [-0.4679, -0.7236, 0.2429],
            [-0.6248, -0.6197, 1.2227],
            [0.3883, -0.3857, 0.0355],
        ]
    )
    cls_token = np.array([[-0.8352, 0.1746, 0.1864]])
    position_embedding = np.array(
        [
            [-1.5302, -0.3911, 0.2571],
            [-0.4725, -0.6068, -0.0303],
            [-1.6768, 1.1485, -0.9118],
            [-0.7921, 0.1596, -0.9332],
            [-0.3956, -0.7537, -0.6565],
        ]
    )
    expected = np.array(
        [
            [-2.3654, -0.2165, 0.4435],
            [0.9494, -0.8383, 0.3436],
            [-2.1448, 0.4250, -0.6689],
            [-1.4169, -0.4601, 0.2895],
            [-0.0072, -1.1394, -0.6210],
        ]
    )

    out = add_cls_token_and_position_embedding(patch_embeddings, cls_token, position_embedding)
    assert np.allclose(out, expected, atol=1e-3)
