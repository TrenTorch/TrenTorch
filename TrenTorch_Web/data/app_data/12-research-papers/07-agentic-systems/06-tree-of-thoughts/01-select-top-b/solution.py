def select_top_b(states, scores, b):
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    return [states[i] for i in order[:b]]
