def compute_run_cost(calls: list[tuple[int, int, float, float]]) -> dict:
    total_input_tokens = 0
    total_output_tokens = 0
    total_cost = 0.0
    for input_tokens, output_tokens, input_price_per_1k, output_price_per_1k in calls:
        total_input_tokens += input_tokens
        total_output_tokens += output_tokens
        total_cost += (input_tokens / 1000) * input_price_per_1k
        total_cost += (output_tokens / 1000) * output_price_per_1k
    return {
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_cost": total_cost,
    }
