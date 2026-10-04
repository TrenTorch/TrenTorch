"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
transformer_params = _module.transformer_params
training_flops = _module.training_flops
chinchilla_tokens = _module.chinchilla_tokens


def test_1_gpt2_small_configuration():
    assert transformer_params(12, 768, 50257) == 123_532_032


def test_2_hand_computed_tiny_model():
    # per layer: 4*4 + 2*2*8 = 16 + 32 = 48 ; 2 layers = 96 ; embedding 10*2 = 20
    assert transformer_params(2, 2, 10, d_ff=8) == 116


def test_3_untied_head_doubles_the_embedding():
    tied = transformer_params(2, 4, 100)
    untied = transformer_params(2, 4, 100, tied=False)
    assert untied - tied == 100 * 4


def test_4_default_ff_width_is_four_times_d():
    assert transformer_params(3, 8, 5) == transformer_params(3, 8, 5, d_ff=32)


def test_5_training_flops_hand_computed():
    assert training_flops(1e9, 2e9) == 12e18


def test_6_chinchilla_tokens():
    assert chinchilla_tokens(7e9) == 140e9


def test_7_layers_scale_linearly_and_return_int():
    a = transformer_params(1, 16, 0)
    assert transformer_params(5, 16, 0) == 5 * a
    assert isinstance(transformer_params(2, 4, 7), int)
