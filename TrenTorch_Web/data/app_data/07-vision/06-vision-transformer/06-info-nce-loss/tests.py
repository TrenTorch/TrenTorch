"""
pytest data/app_data/07-vision/06-vision-transformer/06-info-nce-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

info_nce_loss = load_solution(
    f"07-vision/06-vision-transformer/{Path(__file__).resolve().parent.name}"
).info_nce_loss


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_returns_a_positive_float():
    rng = np.random.default_rng(0)
    image_embeds = rng.normal(size=(4, 5))
    text_embeds = rng.normal(size=(4, 5))
    loss = info_nce_loss(image_embeds, text_embeds)
    assert isinstance(loss, float)
    assert loss > 0.0


def test_02_perfectly_matched_and_separated_pairs_give_near_zero_loss():
    # Each image's embedding is IDENTICAL to its matching text's
    # embedding, and completely different (orthogonal) from every other
    # pair -- the easiest possible case for the model to get right.
    image_embeds = np.eye(4) * 100.0  # huge magnitude -> very sharp/confident similarities
    text_embeds = np.eye(4) * 100.0
    loss = info_nce_loss(image_embeds, text_embeds, temperature=0.1)
    assert loss < 1e-3


# --- Shape / general-case coverage -----------------------------------


def test_03_symmetric_in_the_sense_of_averaging_both_directions():
    rng = np.random.default_rng(1)
    image_embeds = rng.normal(size=(5, 6))
    text_embeds = rng.normal(size=(5, 6))
    loss_forward = info_nce_loss(image_embeds, text_embeds)
    loss_swapped_args = info_nce_loss(text_embeds, image_embeds)
    # swapping which array is "image" and which is "text" swaps the two
    # directions being averaged, but the average of the two is the same
    assert abs(loss_forward - loss_swapped_args) < 1e-9


def test_04_scale_invariant_to_the_embeddings_own_magnitude():
    # L2 normalization means only DIRECTION matters, not magnitude.
    rng = np.random.default_rng(2)
    image_embeds = rng.normal(size=(4, 5))
    text_embeds = rng.normal(size=(4, 5))
    loss_a = info_nce_loss(image_embeds, text_embeds)
    loss_b = info_nce_loss(image_embeds * 37.0, text_embeds * 0.02)
    assert abs(loss_a - loss_b) < 1e-6


# --- Parameter handling -------------------------------------------------


def test_05_lower_temperature_sharpens_correct_confident_predictions_toward_zero_loss():
    image_embeds = np.eye(3) + 0.01  # nearly-identity, slightly noisy
    text_embeds = np.eye(3) + 0.01
    loss_high_temp = info_nce_loss(image_embeds, text_embeds, temperature=1.0)
    loss_low_temp = info_nce_loss(image_embeds, text_embeds, temperature=0.05)
    assert loss_low_temp < loss_high_temp


# --- Edge cases ---------------------------------------------------------


def test_06_batch_size_of_one_is_always_zero_loss():
    # With only one (image, text) pair, there's nothing to distinguish
    # it from -- the "1-way classification" problem is trivial.
    image_embeds = np.array([[1.0, 2.0, 3.0]])
    text_embeds = np.array([[4.0, -1.0, 0.5]])
    loss = info_nce_loss(image_embeds, text_embeds)
    assert loss < 1e-6


# --- Array hygiene ------------------------------------------------------


def test_07_does_not_mutate_its_inputs():
    rng = np.random.default_rng(3)
    image_embeds = rng.normal(size=(4, 5))
    text_embeds = rng.normal(size=(4, 5))
    img_copy, txt_copy = image_embeds.copy(), text_embeds.copy()
    info_nce_loss(image_embeds, text_embeds)
    assert np.array_equal(image_embeds, img_copy)
    assert np.array_equal(text_embeds, txt_copy)


# --- Independent correctness oracle -----------------------------------


def test_08_matches_real_pytorch_symmetric_cross_entropy_on_a_baked_reference_case():
    # Ground truth from the actual library, not our own derivation.
    # Generated once, offline, with:
    #   img, txt = torch.randn(4, 5), torch.randn(4, 5)
    #   img_n, txt_n = img / img.norm(dim=1, keepdim=True), txt / txt.norm(dim=1, keepdim=True)
    #   temp = 0.5
    #   logits = img_n @ txt_n.T / temp
    #   labels = torch.arange(4)
    #   loss = (torch.nn.functional.cross_entropy(logits, labels)
    #           + torch.nn.functional.cross_entropy(logits.T, labels)) / 2
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    image_embeds = np.array(
        [
            [-1.7416, -0.3635, 0.9803, -1.7387, 0.4931],
            [-1.4283, 0.5608, -0.0931, 1.1193, -0.2895],
            [0.0828, -0.5578, 1.0631, -1.8166, 0.7760],
            [-0.6707, -0.9656, 0.9489, -0.3962, -0.0368],
        ]
    )
    text_embeds = np.array(
        [
            [1.7731, 0.1969, 0.6445, 1.4340, -0.3593],
            [-0.4258, 1.2241, -0.5136, -3.3939, 0.5125],
            [2.0572, -0.3627, -0.3550, 0.2548, -0.3719],
            [-0.8919, -0.7806, 1.0954, 1.0561, 0.5673],
        ]
    )
    expected_loss = 1.8254

    loss = info_nce_loss(image_embeds, text_embeds, temperature=0.5)
    assert abs(loss - expected_loss) < 1e-2
