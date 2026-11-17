import re


def parse_action(text):
    """
    text: model output that may contain a line like "Action: Search[query]"

    Returns:
        (name, argument) from the first action line, or None if there is no action.
    """
    # TODO: Find the first "Action: name[arg]" and return its parts (see Theory).
    pass
