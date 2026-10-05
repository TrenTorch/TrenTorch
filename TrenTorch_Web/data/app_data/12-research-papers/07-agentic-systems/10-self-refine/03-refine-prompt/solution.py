def build_refine_prompt(task, draft, feedback):
    return f"Task: {task}\nDraft:\n{draft}\nFeedback: {feedback}\nRewrite the draft to address the feedback."
