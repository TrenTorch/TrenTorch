import numpy as np


def build_preference_pair(prompt_ids: list, chosen_ids: list, rejected_ids: list) -> dict:
    """
    A preference example is TWO full sequences sharing the same
    prompt: prompt+chosen and prompt+rejected -- both real, complete
    responses to the identical question, one marked as the human's
    preferred answer.
    """
    # TODO: chosen_sequence = np.array(prompt_ids + chosen_ids).
    # rejected_sequence = np.array(prompt_ids + rejected_ids). Return
    # {"prompt_len": len(prompt_ids), "chosen": chosen_sequence,
    # "rejected": rejected_sequence}.
    pass


def shares_common_prompt_prefix(preference_pair: dict) -> bool:
    """
    A real preference pair's two sequences MUST agree on their first
    prompt_len tokens -- otherwise the two responses aren't actually
    answers to the same question, and the comparison is meaningless.
    """
    # TODO: slice both "chosen" and "rejected" to their first
    # prompt_len tokens and compare with np.array_equal.
    pass


def response_lengths(preference_pair: dict) -> tuple:
    """
    Returns (chosen_response_length, rejected_response_length) -- the
    number of tokens AFTER the shared prompt in each sequence.
    """
    # TODO: subtract prompt_len from each sequence's total length.
    pass
