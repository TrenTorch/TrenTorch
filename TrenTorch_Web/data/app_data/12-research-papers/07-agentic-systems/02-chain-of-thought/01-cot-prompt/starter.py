def build_cot_prompt(examples, question):
    """
    examples: list of (question, reasoning, answer) demonstrations
    question: the new question to answer

    Returns:
        A few-shot prompt where each example shows its reasoning before the answer,
        followed by the new question with an open answer.
    """
    # TODO: Format each demonstration with its reasoning, then append the new question (see Theory).
    pass
