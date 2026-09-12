"""
pytest data/app_data/03-dl-training/01-optimizers/05-adamw-decoupled-weight-decay/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
adamw_step = _module.adamw_step


def test_adamw_step_matches_known_oracle_across_multiple_steps_from_pytorch():
    # generated once, offline, via torch.optim.AdamW(lr=0.001, weight_decay=0.01)
    params = [np.array([1.0, 2.0])]
    m_list = [np.array([0.0, 0.0])]
    v_list = [np.array([0.0, 0.0])]
    expected_after_each_step = [
        [0.99899, 1.99898],
        [0.99798, 1.99796],
        [0.99697, 1.99694],
    ]
    for t, expected in enumerate(expected_after_each_step, start=1):
        grads = [2.0 * params[0]]
        params, m_list, v_list = adamw_step(params, grads, m_list, v_list, t=t, lr=0.001, weight_decay=0.01)
        assert np.allclose(params[0], expected, atol=1e-3)


def test_adamw_with_zero_weight_decay_matches_plain_adam():
    adam_step = load_solution("03-dl-training/01-optimizers/04-adam-full-update").adam_step

    params_a = [np.array([1.0, 2.0])]
    params_b = [np.array([1.0, 2.0])]
    m_a, v_a = [np.array([0.0, 0.0])], [np.array([0.0, 0.0])]
    m_b, v_b = [np.array([0.0, 0.0])], [np.array([0.0, 0.0])]

    for t in range(1, 4):
        grads_a = [2.0 * params_a[0]]
        grads_b = [2.0 * params_b[0]]
        params_a, m_a, v_a = adamw_step(params_a, grads_a, m_a, v_a, t=t, lr=0.001, weight_decay=0.0)
        params_b, m_b, v_b = adam_step(params_b, grads_b, m_b, v_b, t=t, lr=0.001)
        assert np.allclose(params_a[0], params_b[0], atol=1e-9)


def test_weight_decay_shrinks_a_parameter_even_with_zero_gradient():
    # A parameter with NO gradient signal at all should still shrink
    # toward zero, purely from the decoupled decay term.
    params = [np.array([10.0])]
    grads = [np.array([0.0])]
    m_list = [np.array([0.0])]
    v_list = [np.array([0.0])]
    new_params, _, _ = adamw_step(params, grads, m_list, v_list, t=1, lr=0.1, weight_decay=0.5)
    assert new_params[0][0] < 10.0
    assert np.isclose(new_params[0][0], 10.0 - 0.1 * 0.5 * 10.0)


def test_larger_weight_decay_produces_more_shrinkage():
    params = [np.array([10.0])]
    grads = [np.array([0.0])]
    m_list = [np.array([0.0])]
    v_list = [np.array([0.0])]
    weak_decay, _, _ = adamw_step(params, grads, m_list, v_list, t=1, lr=0.1, weight_decay=0.01)
    strong_decay, _, _ = adamw_step(params, grads, m_list, v_list, t=1, lr=0.1, weight_decay=0.5)
    assert strong_decay[0][0] < weak_decay[0][0]


def test_adamw_does_not_mix_weight_decay_into_the_gradient_before_moments():
    # Directly targets a mutant that folds weight_decay into `grad`
    # before computing moments (the plain-Adam-with-L2 approach AdamW
    # exists to avoid), rather than applying it as a separate,
    # decoupled term.
    #
    # Under CORRECT decoupled decay, m and v are computed from the RAW
    # gradient alone, so they must be identical to plain Adam's own m/v
    # for the same raw gradient, regardless of weight_decay.
    adam_step = load_solution("03-dl-training/01-optimizers/04-adam-full-update").adam_step

    params = [np.array([5.0])]
    grads = [np.array([1.0])]
    m_list = [np.array([0.0])]
    v_list = [np.array([0.0])]

    _, m_from_adamw, v_from_adamw = adamw_step(
        params, grads, m_list, v_list, t=1, lr=0.1, weight_decay=0.5
    )
    _, m_from_adam, v_from_adam = adam_step(params, grads, m_list, v_list, t=1, lr=0.1)

    assert np.allclose(m_from_adamw[0], m_from_adam[0])
    assert np.allclose(v_from_adamw[0], v_from_adam[0])
