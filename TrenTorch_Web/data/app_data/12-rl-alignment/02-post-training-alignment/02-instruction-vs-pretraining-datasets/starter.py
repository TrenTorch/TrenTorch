import numpy as np


def build_instruction_example(prompt_ids: list, response_ids: list, eos_token_id: int) -> dict:
    """
    Builds one instruction-tuning example: the prompt tokens followed
    by the response tokens followed by an end-of-sequence token, PLUS
    a loss_mask marking which positions actually count toward the loss
    (the response and its EOS, matching 01's make_response_mask idea
    -- the prompt is masked out).
    """
    # TODO: input_ids = prompt_ids + response_ids + [eos_token_id].
    # loss_mask = [False]*len(prompt_ids) + [True]*(len(response_ids)+1).
    # Return {"input_ids": np.array(input_ids), "loss_mask":
    # np.array(loss_mask, dtype=bool)}.
    pass


def build_pretraining_example(token_ids: list) -> dict:
    """
    Builds one RAW pretraining example: just the tokens, with EVERY
    position contributing to the loss -- there's no "prompt" the model
    is supposed to ignore, because raw pretraining has no concept of a
    prompt/response split at all.
    """
    # TODO: return {"input_ids": np.array(token_ids), "loss_mask":
    # np.ones(len(token_ids), dtype=bool)}.
    pass


def fraction_of_tokens_supervised(example: dict) -> float:
    """
    What fraction of an example's tokens actually contribute to the
    loss -- 1.0 for a pretraining example, always less than 1.0 for an
    instruction example with a nonempty prompt.
    """
    # TODO: example["loss_mask"].mean()
    pass
