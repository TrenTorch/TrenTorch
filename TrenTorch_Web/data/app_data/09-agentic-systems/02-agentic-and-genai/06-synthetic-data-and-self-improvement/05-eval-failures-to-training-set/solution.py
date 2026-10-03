def failures_to_training_examples(eval_results: list[tuple[str, str, bool]]) -> list[dict]:
    return [
        {"input": input_text, "expected_output": expected_output}
        for input_text, expected_output, passed in eval_results
        if not passed
    ]
