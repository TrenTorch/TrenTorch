import numpy as np


def filter_top_k_by_reward(responses: list, rewards: list, k: int) -> list:
    """
    Keeps only the k highest-reward responses out of a sampled batch,
    discarding the rest -- the "rejection" in rejection sampling.
    """
    # TODO: np.argsort(-rewards) gives indices best-to-worst (argsort
    # is ascending, so negate to sort descending). Take the first k
    # indices, index back into responses.
    pass


def build_rejection_sampling_sft_dataset(prompts: list, response_groups: list, reward_groups: list, k: int) -> list:
    """
    For EACH prompt, several candidate responses were sampled and
    scored (response_groups[i]/reward_groups[i] correspond to
    prompts[i]) -- keep only the top k per prompt and pair each
    surviving response back with its prompt, producing a clean
    (prompt, response) dataset ready for another round of ordinary SFT
    (this is what "rejection sampling fine-tuning" / RAFT actually is:
    generate, filter by reward, then just do SFT on the survivors).
    """
    # TODO: for each (prompt, responses, rewards) triple, call
    # filter_top_k_by_reward, then append (prompt, response) for every
    # response that survived.
    pass
