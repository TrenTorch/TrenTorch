"""
pytest data/app_data/05-transformers-llm/04-llm-engineering/08-resume-from-checkpoint/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"05-transformers-llm/04-llm-engineering/{Path(__file__).resolve().parent.name}")
save_checkpoint = _module.save_checkpoint
train_n_steps = _module.train_n_steps
resume_from_full_checkpoint = _module.resume_from_full_checkpoint
resume_from_weights_only = _module.resume_from_weights_only


def _grads_sequence(rng, shape, n):
    return [[rng.randn(*shape)] for _ in range(n)]


def test_save_checkpoint_copies_not_references():
    params = [np.array([1.0, 2.0])]
    m_list = [np.array([0.1, 0.2])]
    v_list = [np.array([0.01, 0.02])]
    checkpoint = save_checkpoint(params, m_list, v_list, t=5)

    params[0][0] = 999.0  # mutate the original after checkpointing
    assert checkpoint["params"][0][0] == 1.0  # checkpoint must be unaffected
    assert checkpoint["t"] == 5


def test_full_checkpoint_resume_matches_an_uninterrupted_run_exactly():
    rng = np.random.RandomState(0)
    shape = (3,)
    initial_params = [rng.randn(*shape)]
    initial_m = [np.zeros(shape)]
    initial_v = [np.zeros(shape)]
    lr = 0.05

    all_grads = _grads_sequence(rng, shape, 10)

    # Uninterrupted: run all 10 steps in one go.
    continuous_params, _, _, _ = train_n_steps(initial_params, initial_m, initial_v, 1, all_grads, lr)

    # Interrupted: run the first 6 steps, checkpoint, then resume for the
    # remaining 4 using the FULL checkpoint (params + optimizer state).
    params, m_list, v_list, t = train_n_steps(initial_params, initial_m, initial_v, 1, all_grads[:6], lr)
    checkpoint = save_checkpoint(params, m_list, v_list, t)
    resumed_params, _, _, _ = resume_from_full_checkpoint(checkpoint, all_grads[6:], lr)

    assert np.allclose(resumed_params[0], continuous_params[0], atol=1e-12)


def test_weights_only_resume_diverges_from_the_uninterrupted_run():
    # The whole point of this question: resuming from WEIGHTS ONLY
    # (discarding Adam's m/v state and resetting t) produces a
    # DIFFERENT result from an uninterrupted run, even with the exact
    # same gradients, because Adam's update depends on its own history.
    rng = np.random.RandomState(1)
    shape = (3,)
    initial_params = [rng.randn(*shape)]
    initial_m = [np.zeros(shape)]
    initial_v = [np.zeros(shape)]
    lr = 0.1

    all_grads = _grads_sequence(rng, shape, 10)

    continuous_params, _, _, _ = train_n_steps(initial_params, initial_m, initial_v, 1, all_grads, lr)

    params, m_list, v_list, t = train_n_steps(initial_params, initial_m, initial_v, 1, all_grads[:6], lr)
    weights_only_params = [p.copy() for p in params]
    resumed_params, _, _, _ = resume_from_weights_only(weights_only_params, all_grads[6:], lr)

    assert not np.allclose(resumed_params[0], continuous_params[0], atol=1e-6)


def test_train_n_steps_advances_t_by_exactly_the_number_of_steps():
    rng = np.random.RandomState(2)
    shape = (2,)
    params = [rng.randn(*shape)]
    m_list = [np.zeros(shape)]
    v_list = [np.zeros(shape)]
    grads = _grads_sequence(rng, shape, 7)

    _, _, _, final_t = train_n_steps(params, m_list, v_list, t=1, grads_sequence=grads, lr=0.01)
    assert final_t == 8


def test_resume_from_full_checkpoint_continues_the_step_counter_correctly():
    rng = np.random.RandomState(3)
    shape = (2,)
    params = [rng.randn(*shape)]
    m_list = [np.zeros(shape)]
    v_list = [np.zeros(shape)]
    grads = _grads_sequence(rng, shape, 5)

    checkpoint = save_checkpoint(params, m_list, v_list, t=4)
    _, _, _, final_t = resume_from_full_checkpoint(checkpoint, grads, lr=0.01)
    assert final_t == 9  # 4 + 5 steps
