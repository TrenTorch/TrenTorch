def build_reflection_prompt(task, trajectory, feedback):
    return (
        f"Task: {task}\n"
        f"Trajectory:\n{trajectory}\n"
        f"Feedback: {feedback}\n"
        "Reflect on what went wrong and what to do differently."
    )
