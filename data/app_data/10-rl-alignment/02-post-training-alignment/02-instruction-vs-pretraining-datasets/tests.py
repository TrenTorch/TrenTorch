"""
pytest data/app_data/10-rl-alignment/02-post-training-alignment/02-instruction-vs-pretraining-datasets/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/02-post-training-alignment/{Path(__file__).resolve().parent.name}")
build_instruction_example = _module.build_instruction_example
build_pretraining_example = _module.build_pretraining_example
fraction_of_tokens_supervised = _module.fraction_of_tokens_supervised


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_instruction_example_masks_prompt_tokens():
    ex = build_instruction_example(prompt_ids=[1, 2, 3], response_ids=[4, 5], eos_token_id=0)
    assert list(ex["loss_mask"]) == [False, False, False, True, True, True]


def test_02_pretraining_example_supervises_every_token():
    ex = build_pretraining_example([1, 2, 3, 4])
    assert fraction_of_tokens_supervised(ex) == 1.0


# --- General-case coverage --------------------------------------------


def test_03_instruction_example_concatenates_correctly():
    ex = build_instruction_example(prompt_ids=[7, 8], response_ids=[9], eos_token_id=99)
    assert list(ex["input_ids"]) == [7, 8, 9, 99]


def test_04_fraction_supervised_matches_response_length_ratio():
    ex = build_instruction_example(prompt_ids=[1, 2, 3, 4], response_ids=[5, 6], eos_token_id=0)
    # 2 response tokens + 1 EOS = 3 supervised, out of 7 total.
    assert np.isclose(fraction_of_tokens_supervised(ex), 3 / 7)


def test_05_pretraining_fraction_always_one_regardless_of_length():
    for length in (1, 5, 100):
        ex = build_pretraining_example(list(range(length)))
        assert fraction_of_tokens_supervised(ex) == 1.0


# --- Parameter handling -------------------------------------------------


def test_06_instruction_example_input_and_mask_same_length():
    ex = build_instruction_example(prompt_ids=[1, 2], response_ids=[3, 4, 5], eos_token_id=6)
    assert len(ex["input_ids"]) == len(ex["loss_mask"])


def test_07_longer_prompt_means_lower_supervised_fraction():
    short_prompt = build_instruction_example(prompt_ids=[1], response_ids=[2, 3], eos_token_id=0)
    long_prompt = build_instruction_example(prompt_ids=[1, 2, 3, 4, 5, 6, 7, 8], response_ids=[2, 3], eos_token_id=0)
    assert fraction_of_tokens_supervised(long_prompt) < fraction_of_tokens_supervised(short_prompt)


# --- Edge cases ---------------------------------------------------------


def test_08_empty_prompt_supervises_everything_including_eos():
    ex = build_instruction_example(prompt_ids=[], response_ids=[1, 2], eos_token_id=3)
    assert fraction_of_tokens_supervised(ex) == 1.0


def test_09_single_response_token_plus_eos():
    ex = build_instruction_example(prompt_ids=[1, 2, 3], response_ids=[4], eos_token_id=5)
    assert list(ex["input_ids"]) == [1, 2, 3, 4, 5]
    assert ex["loss_mask"].sum() == 2  # the response token AND the eos token


# --- Independent correctness oracle -----------------------------------


def test_10_eos_token_is_included_in_the_supervised_region():
    # Directly targets a mutant that masks in only response_ids and
    # forgets the trailing EOS token needs to be supervised too (the
    # model must learn WHEN to stop generating, which is exactly what
    # predicting EOS correctly trains).
    ex = build_instruction_example(prompt_ids=[1, 2], response_ids=[3, 4, 5], eos_token_id=99)
    assert ex["input_ids"][-1] == 99
    assert bool(ex["loss_mask"][-1]) is True
