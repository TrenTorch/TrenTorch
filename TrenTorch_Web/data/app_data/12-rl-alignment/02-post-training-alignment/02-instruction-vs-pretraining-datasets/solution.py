import numpy as np


def build_instruction_example(prompt_ids: list, response_ids: list, eos_token_id: int) -> dict:
    input_ids = list(prompt_ids) + list(response_ids) + [eos_token_id]
    loss_mask = [0] * len(prompt_ids) + [1] * (len(response_ids) + 1)
    return {"input_ids": np.array(input_ids), "loss_mask": np.array(loss_mask, dtype=bool)}


def build_pretraining_example(token_ids: list) -> dict:
    input_ids = np.array(token_ids)
    loss_mask = np.ones(len(token_ids), dtype=bool)
    return {"input_ids": input_ids, "loss_mask": loss_mask}


def fraction_of_tokens_supervised(example: dict) -> float:
    return float(example["loss_mask"].mean())
