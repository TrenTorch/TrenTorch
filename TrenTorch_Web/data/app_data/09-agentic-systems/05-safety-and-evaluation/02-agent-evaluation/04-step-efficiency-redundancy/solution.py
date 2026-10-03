import json


def step_efficiency(n_steps, n_optimal, succeeded):
    if not succeeded:
        return 0.0
    return min(1.0, n_optimal / n_steps)


def redundancy_rate(actions):
    seen, repeats = set(), 0
    for name, args in actions:
        key = (name, json.dumps(args, sort_keys=True))
        if key in seen:
            repeats += 1
        seen.add(key)
    return repeats / len(actions) if actions else 0.0
