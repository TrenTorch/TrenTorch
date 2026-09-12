"""
pytest data/app_data/03-dl-training/01-optimizers/04-adam-full-update/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/01-optimizers/{Path(__file__).resolve().parent.name}")
adam_step = _module.adam_step


def test_adam_step_matches_known_oracle_across_multiple_steps_from_pytorch():
    # generated once, offline, via torch.optim.Adam(lr=0.001)
    params = [np.array([1.0, 2.0])]
    m_list = [np.array([0.0, 0.0])]
    v_list = [np.array([0.0, 0.0])]
    expected_after_each_step = [
        [0.999, 1.999],
        [0.998, 1.998],
        [0.997, 1.997],
    ]
    for t, expected in enumerate(expected_after_each_step, start=1):
        grads = [2.0 * params[0]]
        params, m_list, v_list = adam_step(params, grads, m_list, v_list, t=t, lr=0.001)
        assert np.allclose(params[0], expected, atol=1e-3)


def test_adam_step_moves_opposite_the_gradient():
    params = [np.array([0.0])]
    grads = [np.array([1.0])]
    m_list = [np.array([0.0])]
    v_list = [np.array([0.0])]
    new_params, _, _ = adam_step(params, grads, m_list, v_list, t=1, lr=0.1)
    assert new_params[0][0] < 0.0


def test_adam_step_threads_m_and_v_forward_correctly():
    params = [np.array([1.0])]
    m_list = [np.array([0.0])]
    v_list = [np.array([0.0])]
    grads = [np.array([2.0])]
    _, new_m, new_v = adam_step(params, grads, m_list, v_list, t=1, lr=0.001)
    assert not np.isclose(new_m[0][0], 0.0)
    assert not np.isclose(new_v[0][0], 0.0)


def test_adam_step_gives_a_shrunken_step_for_large_historical_gradients():
    # A parameter whose moments already reflect a large historical
    # gradient magnitude should get a proportionally SMALLER step than
    # one whose gradients have been small, for the SAME current gradient.
    params = [np.array([0.0]), np.array([0.0])]
    grads = [np.array([1.0]), np.array([1.0])]
    m_list = [np.array([0.0]), np.array([0.0])]
    v_small_history = [np.array([0.001])]
    v_large_history = [np.array([100.0])]

    small_hist_result, _, _ = adam_step(
        [params[0]], [grads[0]], [m_list[0]], v_small_history, t=5, lr=0.01
    )
    large_hist_result, _, _ = adam_step(
        [params[1]], [grads[1]], [m_list[1]], v_large_history, t=5, lr=0.01
    )
    assert abs(small_hist_result[0][0]) > abs(large_hist_result[0][0])


def test_adam_step_does_not_forget_to_divide_by_sqrt_v_hat():
    # Directly targets a mutant that omits the v_hat-based
    # normalization entirely (reducing to plain momentum-like behavior):
    # comparing two very different v-histories for the SAME gradient
    # and m should produce clearly different step sizes only if the
    # v_hat division is genuinely applied.
    params = [np.array([0.0])]
    grads = [np.array([1.0])]
    m_list = [np.array([0.0])]

    result_tiny_v, _, _ = adam_step(params, grads, m_list, [np.array([1e-10])], t=10, lr=0.01)
    result_huge_v, _, _ = adam_step(params, grads, m_list, [np.array([1e6])], t=10, lr=0.01)
    assert abs(result_tiny_v[0][0]) != abs(result_huge_v[0][0])
    assert abs(result_tiny_v[0][0]) > abs(result_huge_v[0][0])
