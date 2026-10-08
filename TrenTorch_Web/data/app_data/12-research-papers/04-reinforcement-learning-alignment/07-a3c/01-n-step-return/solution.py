def n_step_return(rewards, bootstrap, gamma):
    G = bootstrap
    for r in reversed(rewards):
        G = r + gamma * G
    return float(G)
