def refine_loop(generate, feedback, refine, steps):
    """
    generate: function returning the first draft
    feedback: function returning feedback on a draft, or "OK" if it is acceptable
    refine: function taking the draft and its feedback and returning an improved draft
    steps: maximum number of refinement rounds

    Returns:
        The final draft.
    """
    # TODO: Generate a draft, then refine it until the feedback is OK or steps run out (see Theory).
    pass
