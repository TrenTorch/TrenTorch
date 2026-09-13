"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/03-preference-datasets-chosen-rejected/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
build_preference_pair = _module.build_preference_pair
shares_common_prompt_prefix = _module.shares_common_prompt_prefix
response_lengths = _module.response_lengths


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_preference_pair_shares_the_prompt_prefix():
    pair = build_preference_pair(prompt_ids=[1, 2, 3], chosen_ids=[4, 5], rejected_ids=[6])
    assert shares_common_prompt_prefix(pair)


def test_02_response_lengths_computed_correctly():
    pair = build_preference_pair(prompt_ids=[1, 2, 3], chosen_ids=[4, 5], rejected_ids=[6])
    chosen_len, rejected_len = response_lengths(pair)
    assert chosen_len == 2
    assert rejected_len == 1


# --- General-case coverage --------------------------------------------


def test_03_chosen_and_rejected_sequences_built_correctly():
    pair = build_preference_pair(prompt_ids=[10, 11], chosen_ids=[1, 2, 3], rejected_ids=[9])
    assert list(pair["chosen"]) == [10, 11, 1, 2, 3]
    assert list(pair["rejected"]) == [10, 11, 9]


def test_04_prompt_len_recorded_correctly():
    pair = build_preference_pair(prompt_ids=[1, 2, 3, 4], chosen_ids=[5], rejected_ids=[6, 7])
    assert pair["prompt_len"] == 4


def test_05_equal_length_responses():
    pair = build_preference_pair(prompt_ids=[1], chosen_ids=[2, 3], rejected_ids=[4, 5])
    assert response_lengths(pair) == (2, 2)


# --- Parameter handling -------------------------------------------------


def test_06_shares_common_prefix_detects_a_mismatched_prompt():
    # Manually construct a pair whose two sequences DON'T actually
    # share a prompt, to verify the check can genuinely fail too.
    broken_pair = {
        "prompt_len": 3,
        "chosen": [1, 2, 3, 4, 5],
        "rejected": [1, 2, 99, 6],
    }
    import numpy as np

    broken_pair = {k: (np.array(v) if k != "prompt_len" else v) for k, v in broken_pair.items()}
    assert not shares_common_prompt_prefix(broken_pair)


def test_07_response_lengths_with_empty_response():
    pair = build_preference_pair(prompt_ids=[1, 2], chosen_ids=[3], rejected_ids=[])
    assert response_lengths(pair) == (1, 0)


# --- Edge cases ---------------------------------------------------------


def test_08_empty_prompt_still_shares_a_trivially_common_prefix():
    pair = build_preference_pair(prompt_ids=[], chosen_ids=[1, 2], rejected_ids=[3])
    assert shares_common_prompt_prefix(pair)


def test_09_single_token_prompt():
    pair = build_preference_pair(prompt_ids=[42], chosen_ids=[1, 2, 3], rejected_ids=[4])
    assert pair["prompt_len"] == 1
    assert shares_common_prompt_prefix(pair)


# --- Independent correctness oracle -----------------------------------


def test_10_response_lengths_derived_from_actual_sequences_not_inputs():
    # Directly targets a mutant that just returns len(chosen_ids),
    # len(rejected_ids) from the ORIGINAL inputs instead of deriving
    # response length from the built sequence minus prompt_len --
    # these should agree here, but only if response_lengths is
    # actually reading prompt_len off the pair correctly.
    pair = build_preference_pair(prompt_ids=[1, 2, 3], chosen_ids=[4, 5, 6, 7], rejected_ids=[8])
    chosen_len, rejected_len = response_lengths(pair)
    assert chosen_len == len(pair["chosen"]) - pair["prompt_len"]
    assert rejected_len == len(pair["rejected"]) - pair["prompt_len"]
    assert chosen_len == 4
    assert rejected_len == 1
