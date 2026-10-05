def build_reflection_prompt(task, trajectory, feedback):
    """
    task: the task description
    trajectory: the actions and observations of the failed attempt
    feedback: the environment's signal about the failure

    Returns:
        A prompt asking the model to reflect on the failure and what to change next time.
    """
    # TODO: Combine the task, trajectory and feedback into the reflection prompt (see Theory).
    pass
