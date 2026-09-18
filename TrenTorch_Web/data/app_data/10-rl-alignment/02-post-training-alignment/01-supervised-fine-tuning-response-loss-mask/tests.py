"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/01-supervised-fine-tuning-response-loss-mask/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
make_response_mask = _module.make_response_mask
sft_loss = _module.sft_loss
raw_pretraining_loss = _module.raw_pretraining_loss
cross_entropy_forward = _module.cross_entropy_forward


def _random_example(seed, seq_len=6, vocab=5):
    rng = np.random.default_rng(seed)
    logits = rng.normal(size=(seq_len, vocab))
    targets = rng.integers(0, vocab, size=seq_len)
    return logits, targets


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_response_mask_marks_only_response_positions():
    mask = make_response_mask(prompt_len=3, total_len=6)
    assert list(mask) == [False, False, False, True, True, True]


def test_02_sft_loss_matches_manual_slice_based_cross_entropy():
    logits, targets = _random_example(0)
    prompt_len = 3
    loss = sft_loss(logits, targets, prompt_len)
    manual = cross_entropy_forward(logits[prompt_len:], targets[prompt_len:], reduction="mean")
    assert np.isclose(loss, manual)


# --- General-case coverage --------------------------------------------


def test_03_sft_loss_ignores_prompt_token_predictions_entirely():
    logits, targets = _random_example(1)
    prompt_len = 4
    loss_normal = sft_loss(logits, targets, prompt_len)
    # Corrupting the PROMPT region's logits must not change the loss at all.
    corrupted_logits = logits.copy()
    corrupted_logits[:prompt_len] += 100.0
    loss_corrupted = sft_loss(corrupted_logits, targets, prompt_len)
    assert np.isclose(loss_normal, loss_corrupted)


def test_04_sft_loss_is_sensitive_to_response_token_predictions():
    logits, targets = _random_example(2)
    prompt_len = 3
    loss_normal = sft_loss(logits, targets, prompt_len)
    # Adding the SAME constant to every class's logit in a row is a
    # softmax no-op (softmax is shift-invariant) -- perturb the target
    # class specifically, which genuinely changes the loss.
    corrupted_logits = logits.copy()
    response_rows = np.arange(prompt_len, logits.shape[0])
    corrupted_logits[response_rows, targets[prompt_len:]] += 100.0
    loss_corrupted = sft_loss(corrupted_logits, targets, prompt_len)
    assert not np.isclose(loss_normal, loss_corrupted)


def test_05_raw_pretraining_loss_matches_full_sequence_cross_entropy():
    logits, targets = _random_example(3)
    assert np.isclose(raw_pretraining_loss(logits, targets), cross_entropy_forward(logits, targets, "mean"))


# --- Parameter handling -------------------------------------------------


def test_06_sft_and_raw_loss_differ_when_prompt_is_a_real_fraction():
    logits, targets = _random_example(4, seq_len=10)
    sft = sft_loss(logits, targets, prompt_len=5)
    raw = raw_pretraining_loss(logits, targets)
    # Not a mathematical law in general, but for random data the two
    # averages (over different-sized, different subsets) essentially
    # never land on the exact same float.
    assert sft != raw


def test_07_response_mask_shape_and_count():
    mask = make_response_mask(prompt_len=2, total_len=9)
    assert mask.shape == (9,)
    assert mask.sum() == 7


# --- Edge cases ---------------------------------------------------------


def test_08_zero_length_prompt_matches_raw_pretraining_loss():
    logits, targets = _random_example(5)
    assert np.isclose(sft_loss(logits, targets, prompt_len=0), raw_pretraining_loss(logits, targets))


def test_09_prompt_covering_everything_but_one_token():
    logits, targets = _random_example(6, seq_len=5)
    loss = sft_loss(logits, targets, prompt_len=4)
    manual = cross_entropy_forward(logits[4:], targets[4:], reduction="mean")
    assert np.isclose(loss, manual)


# --- Independent correctness oracle -----------------------------------


def test_10_sft_loss_equals_weighted_average_not_full_sequence_average():
    # Directly targets a mutant that computes the full-sequence mean
    # loss and just multiplies by the mask (which would silently
    # divide by the WRONG denominator -- total_len instead of the
    # number of response tokens).
    logits, targets = _random_example(7, seq_len=8)
    prompt_len = 6  # only 2 response tokens out of 8
    loss = sft_loss(logits, targets, prompt_len)
    per_token = cross_entropy_forward(logits, targets, reduction="none")
    wrong_denominator = per_token[prompt_len:].sum() / len(per_token)
    correct = per_token[prompt_len:].mean()
    assert np.isclose(loss, correct)
    assert not np.isclose(loss, wrong_denominator)
