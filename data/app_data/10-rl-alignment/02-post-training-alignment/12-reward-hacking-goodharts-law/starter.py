import numpy as np


def select_best_by_proxy(candidates: list, proxy_rewards: list) -> int:
    """
    Picks the candidate the (imperfect) PROXY reward model scores
    highest -- exactly what 10-best-of-n-sampling's selection does,
    except here the proxy is deliberately allowed to disagree with
    what a response is ACTUALLY good for.
    """
    # TODO: return int(np.argmax(proxy_rewards))
    pass


def true_reward_of_selection(true_rewards: list, selected_index: int) -> float:
    """
    Looks up what the TRUE (ground-truth) reward of whichever
    candidate got selected actually was.
    """
    # TODO: return float(true_rewards[selected_index])
    pass


def reward_hacking_gap(true_rewards: list, proxy_rewards: list) -> float:
    """
    Goodhart's law, quantified: how much TRUE reward is left on the
    table by optimizing the PROXY instead of the true objective --
    the gap between the true reward of the proxy-optimal choice and
    the true reward of the ACTUALLY-best choice. Zero when the proxy
    and the true reward agree on what's best; positive whenever they
    disagree.
    """
    # TODO: proxy_choice = select_best_by_proxy(true_rewards,
    # proxy_rewards). oracle_choice = argmax(true_rewards). Return
    # true_rewards[oracle_choice] - true_rewards[proxy_choice].
    pass
