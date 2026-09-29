def run_react_loop(
    steps: list[tuple[str, str, str]],
    observations: dict[tuple[str, str], str],
    max_steps: int,
) -> list[tuple[str, str, str, str]]:
    trace = []
    for i, (thought, action, action_input) in enumerate(steps):
        if i >= max_steps:
            break
        if action == "finish":
            trace.append((thought, action, action_input, ""))
            break
        observation = observations.get((action, action_input), "NO_OBSERVATION_FOUND")
        trace.append((thought, action, action_input, observation))
    return trace
