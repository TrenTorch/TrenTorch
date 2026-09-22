def compute_run_cost(calls: list[tuple[int, int, float, float]]) -> dict:
    """Each call is (input_tokens, output_tokens, input_price_per_1k,
    output_price_per_1k). Return a dict with "total_input_tokens",
    "total_output_tokens", and "total_cost" (sum over all calls of
    input_tokens/1000 * input_price_per_1k + output_tokens/1000 *
    output_price_per_1k) summed across every call.
    """
    # TODO: implement
    pass
