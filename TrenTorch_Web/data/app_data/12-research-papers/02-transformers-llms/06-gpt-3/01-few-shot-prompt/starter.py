def build_few_shot_prompt(examples, query, sep="\n\n"):
    """
    examples: list of (input, output) pairs shown to the model
    query: the new input the model should complete
    sep: string placed between items

    Returns:
        One prompt string: each example as "input => output", then "query =>".
    """
    # TODO: Format each example, add the query with an empty answer, and join with sep (see Theory).
    pass
