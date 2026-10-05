def run_react_loop(
    steps: list[tuple[str, str, str]],
    observations: dict[tuple[str, str], str],
    max_steps: int,
) -> list[tuple[str, str, str, str]]:
    """
    steps: the model's scripted (thought, action, action_input) turns, in
    order, as if already generated -- no real model call here.
    observations: (action, action_input) -> the tool's observation text
    for that exact call, simulating tool execution.
    max_steps: hard cap on how many steps the loop may take.

    Process steps in order, up to max_steps. For each step, look up its
    observation (or "NO_OBSERVATION_FOUND" if this exact call was never
    scripted) and append (thought, action, action_input, observation) to
    the trace. Stop immediately -- without a tool lookup -- the moment
    action == "finish", recording that final step with an empty
    observation.

    Returns the trace built so far.
    """
    # TODO: Implement the ReAct loop from Theory.
    pass
