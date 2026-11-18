import re


def extract_final_answer(text):
    """
    text: a model's full reasoning output

    Returns:
        The text after the last "The answer is", up to the next period or newline, stripped.
        None if the phrase is absent.
    """
    # TODO: Find every "The answer is ..." and return the last one's content (see Theory).
    pass
