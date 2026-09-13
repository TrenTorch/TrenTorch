import numpy as np


def select_best_by_proxy(candidates: list, proxy_rewards: list) -> int:
    return int(np.argmax(proxy_rewards))


def true_reward_of_selection(true_rewards: list, selected_index: int) -> float:
    return float(true_rewards[selected_index])


def reward_hacking_gap(true_rewards: list, proxy_rewards: list) -> float:
    proxy_choice = select_best_by_proxy(true_rewards, proxy_rewards)
    oracle_choice = int(np.argmax(true_rewards))
    return float(true_rewards[oracle_choice] - true_rewards[proxy_choice])
