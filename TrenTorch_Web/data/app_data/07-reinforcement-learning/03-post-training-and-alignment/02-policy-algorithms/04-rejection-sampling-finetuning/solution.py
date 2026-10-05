import numpy as np


def filter_top_k_by_reward(responses: list, rewards: list, k: int) -> list:
    rewards = np.asarray(rewards, dtype=float)
    order = np.argsort(-rewards, kind="stable")
    top_k_indices = order[:k]
    return [responses[i] for i in top_k_indices]


def build_rejection_sampling_sft_dataset(prompts: list, response_groups: list, reward_groups: list, k: int) -> list:
    dataset = []
    for prompt, responses, rewards in zip(prompts, response_groups, reward_groups):
        kept = filter_top_k_by_reward(responses, rewards, k)
        for response in kept:
            dataset.append((prompt, response))
    return dataset
