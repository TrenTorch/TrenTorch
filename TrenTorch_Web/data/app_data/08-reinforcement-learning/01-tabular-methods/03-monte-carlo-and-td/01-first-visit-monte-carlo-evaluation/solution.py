import numpy as np


def first_visit_mc(episodes: list, gamma: float) -> dict:
    returns = {}
    for episode in episodes:
        returns_at = [0.0] * len(episode)
        g = 0.0
        for t in range(len(episode) - 1, -1, -1):
            g = episode[t][1] + gamma * g
            returns_at[t] = g
        seen = set()
        for t, (state, _) in enumerate(episode):
            if state not in seen:
                seen.add(state)
                returns.setdefault(state, []).append(returns_at[t])
    return {state: float(np.mean(values)) for state, values in returns.items()}
