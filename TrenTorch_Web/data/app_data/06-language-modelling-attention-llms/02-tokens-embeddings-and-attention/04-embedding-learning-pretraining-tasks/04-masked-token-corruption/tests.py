"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mask_tokens = _module.mask_tokens
IDS = np.arange(10, 30)


def test_1_replays_the_stated_random_stream():
    inputs, labels = mask_tokens(IDS, 0, 1000, set(), np.random.RandomState(3), 0.3)
    r = np.random.RandomState(3)
    u = r.random_sample(20)
    chosen = u < 0.3
    k = chosen.sum()
    rr = r.random_sample(k)
    rt = r.randint(0, 1000, size=k)
    exp_in, exp_lab = IDS.copy(), np.full(20, -100)
    pos = np.where(chosen)[0]
    for m, p in enumerate(pos):
        exp_lab[p] = IDS[p]
        if rr[m] < 0.8:
            exp_in[p] = 0
        elif rr[m] < 0.9:
            exp_in[p] = rt[m]
    assert np.array_equal(inputs, exp_in) and np.array_equal(labels, exp_lab)


def test_2_special_tokens_are_never_chosen():
    ids = np.array([101, 5, 6, 102] * 50)
    inputs, labels = mask_tokens(ids, 103, 1000, {101, 102}, np.random.RandomState(0), 1.0)
    assert (labels[ids == 101] == -100).all() and (inputs[ids == 102] == 102).all()
    assert (labels[(ids == 5) | (ids == 6)] != -100).all()


def test_3_unchosen_positions_are_untouched():
    inputs, labels = mask_tokens(IDS, 0, 1000, set(), np.random.RandomState(1), 0.1)
    assert (inputs[labels == -100] == IDS[labels == -100]).all()


def test_4_about_15_percent_are_chosen():
    ids = np.arange(20000) % 500 + 10
    _, labels = mask_tokens(ids, 0, 1000, set(), np.random.RandomState(0))
    assert abs((labels != -100).mean() - 0.15) < 0.01


def test_5_eighty_ten_ten_split_among_chosen():
    ids = np.arange(40000) % 500 + 10
    inputs, labels = mask_tokens(ids, 0, 1000, set(), np.random.RandomState(1), 0.5)
    chosen = labels != -100
    frac_mask = (inputs[chosen] == 0).mean()
    frac_same = (inputs[chosen] == ids[chosen]).mean()
    assert abs(frac_mask - 0.8) < 0.02 and abs(frac_same - 0.1) < 0.02


def test_6_prob_zero_chooses_nothing_and_prob_one_chooses_everything():
    i0, l0 = mask_tokens(IDS, 0, 100, set(), np.random.RandomState(0), 0.0)
    _, l1 = mask_tokens(IDS, 0, 100, set(), np.random.RandomState(0), 1.0)
    assert np.array_equal(i0, IDS) and (l0 == -100).all() and np.array_equal(l1, IDS)


def test_7_input_untouched_and_shapes():
    ids = IDS.copy()
    inputs, labels = mask_tokens(ids, 0, 100, set(), np.random.RandomState(2))
    assert np.array_equal(ids, IDS) and inputs.shape == labels.shape == ids.shape
