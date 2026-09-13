"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/15-adapter-methods-prefix-prompt-tuning/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
prefix_tuning_augment = _module.prefix_tuning_augment
prompt_tuning_augment = _module.prompt_tuning_augment
count_trainable_parameters_prefix_tuning = _module.count_trainable_parameters_prefix_tuning
count_trainable_parameters_prompt_tuning = _module.count_trainable_parameters_prompt_tuning
scaled_dot_product_attention = _module.scaled_dot_product_attention


def _random_attention_setup(seed, seq_len=5, prefix_len=2, d=4, n_queries=3):
    rng = np.random.default_rng(seed)
    q = rng.normal(size=(n_queries, d))
    k = rng.normal(size=(seq_len, d))
    v = rng.normal(size=(seq_len, d))
    pk = rng.normal(size=(prefix_len, d))
    pv = rng.normal(size=(prefix_len, d))
    return q, k, v, pk, pv


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_prefix_tuning_prepends_the_prefix_first():
    key = np.array([[1.0, 1.0], [2.0, 2.0]])
    value = np.array([[9.0, 9.0], [8.0, 8.0]])
    prefix_key = np.array([[0.0, 0.0]])
    prefix_value = np.array([[5.0, 5.0]])
    aug_key, aug_value = prefix_tuning_augment(key, value, prefix_key, prefix_value)
    assert np.allclose(aug_key, [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]])
    assert np.allclose(aug_value, [[5.0, 5.0], [9.0, 9.0], [8.0, 8.0]])


def test_02_prompt_tuning_changes_effective_sequence_length():
    embeddings = np.zeros((6, 4))
    soft_prompt = np.ones((3, 4))
    augmented = prompt_tuning_augment(embeddings, soft_prompt)
    assert augmented.shape[0] == 9


# --- General-case coverage --------------------------------------------


def test_03_prefix_tuning_genuinely_changes_attention_output():
    q, k, v, pk, pv = _random_attention_setup(0)
    out_plain, _ = scaled_dot_product_attention(q, k, v)
    aug_k, aug_v = prefix_tuning_augment(k, v, pk, pv)
    out_aug, _ = scaled_dot_product_attention(q, aug_k, aug_v)
    assert not np.allclose(out_plain, out_aug)


def test_04_prefix_tuning_output_shape_unaffected_for_queries():
    q, k, v, pk, pv = _random_attention_setup(1, n_queries=7)
    aug_k, aug_v = prefix_tuning_augment(k, v, pk, pv)
    out, weights = scaled_dot_product_attention(q, aug_k, aug_v)
    assert out.shape == (7, aug_v.shape[-1])
    assert weights.shape == (7, aug_k.shape[0])


def test_05_prompt_tuning_preserves_original_embeddings_unchanged():
    embeddings = np.array([[1.0, 2.0], [3.0, 4.0]])
    soft_prompt = np.array([[9.0, 9.0]])
    augmented = prompt_tuning_augment(embeddings, soft_prompt)
    assert np.allclose(augmented[-2:], embeddings)


# --- Parameter handling -------------------------------------------------


def test_06_prefix_tuning_scales_with_num_layers():
    single_layer = count_trainable_parameters_prefix_tuning(num_layers=1, prefix_len=10, hidden_dim=64)
    many_layers = count_trainable_parameters_prefix_tuning(num_layers=12, prefix_len=10, hidden_dim=64)
    assert many_layers == single_layer * 12


def test_07_prompt_tuning_is_independent_of_num_layers():
    params = count_trainable_parameters_prompt_tuning(prompt_len=20, hidden_dim=768)
    assert params == 20 * 768


# --- Edge cases ---------------------------------------------------------


def test_08_prompt_tuning_trains_far_fewer_params_than_prefix_tuning():
    prompt_params = count_trainable_parameters_prompt_tuning(prompt_len=20, hidden_dim=768)
    prefix_params = count_trainable_parameters_prefix_tuning(num_layers=24, prefix_len=20, hidden_dim=768)
    assert prompt_params < prefix_params


def test_09_zero_length_prefix_leaves_attention_unchanged():
    q, k, v, _, _ = _random_attention_setup(2)
    pk = np.zeros((0, k.shape[-1]))
    pv = np.zeros((0, v.shape[-1]))
    aug_k, aug_v = prefix_tuning_augment(k, v, pk, pv)
    out_plain, _ = scaled_dot_product_attention(q, k, v)
    out_aug, _ = scaled_dot_product_attention(q, aug_k, aug_v)
    assert np.allclose(out_plain, out_aug)


# --- Independent correctness oracle -----------------------------------


def test_10_prefix_tuning_parameter_count_includes_both_key_and_value():
    # Directly targets a mutant that forgets the factor of 2 (counting
    # only the learnable K prefix, or only V, not both).
    num_layers, prefix_len, hidden_dim = 6, 8, 32
    expected = num_layers * prefix_len * hidden_dim * 2
    assert count_trainable_parameters_prefix_tuning(num_layers, prefix_len, hidden_dim) == expected
    half_of_expected = expected // 2
    assert count_trainable_parameters_prefix_tuning(num_layers, prefix_len, hidden_dim) != half_of_expected
