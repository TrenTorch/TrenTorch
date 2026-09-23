def failures_to_training_examples(eval_results: list[tuple[str, str, bool]]) -> list[dict]:
    """Each eval result is (input, expected_output, passed). Return a
    {"input", "expected_output"} dict for every result where `passed` is
    False -- the failures worth turning into new training examples so the
    model can be improved on exactly what it's currently getting wrong.
    Passing results are excluded entirely.
    """
    # TODO: implement
    pass
