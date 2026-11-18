def build_react_prompt(question, steps):
    parts = [f"Question: {question}"]
    for thought, action, observation in steps:
        parts.append(f"Thought: {thought}\nAction: {action}\nObservation: {observation}")
    return "\n".join(parts)
