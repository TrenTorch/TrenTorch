import numpy as np


def build_preference_pair(prompt_ids: list, chosen_ids: list, rejected_ids: list) -> dict:
    chosen_sequence = np.array(list(prompt_ids) + list(chosen_ids))
    rejected_sequence = np.array(list(prompt_ids) + list(rejected_ids))
    return {"prompt_len": len(prompt_ids), "chosen": chosen_sequence, "rejected": rejected_sequence}


def shares_common_prompt_prefix(preference_pair: dict) -> bool:
    prompt_len = preference_pair["prompt_len"]
    chosen_prefix = preference_pair["chosen"][:prompt_len]
    rejected_prefix = preference_pair["rejected"][:prompt_len]
    return bool(np.array_equal(chosen_prefix, rejected_prefix))


def response_lengths(preference_pair: dict) -> tuple:
    prompt_len = preference_pair["prompt_len"]
    chosen_len = len(preference_pair["chosen"]) - prompt_len
    rejected_len = len(preference_pair["rejected"]) - prompt_len
    return chosen_len, rejected_len
