def shadow_deploy(request, live_model_fn, shadow_model_fn) -> dict:
    live_output = live_model_fn(request)
    try:
        shadow_output = shadow_model_fn(request)
        shadow_error = None
    except Exception as error:
        shadow_output = None
        shadow_error = str(error)

    return {
        "response": live_output,
        "shadow_output": shadow_output,
        "shadow_error": shadow_error,
    }


def outputs_agree(live_output, shadow_output, tolerance: float = 1e-9) -> bool:
    if isinstance(live_output, (int, float)) and isinstance(shadow_output, (int, float)):
        return abs(live_output - shadow_output) <= tolerance
    return live_output == shadow_output


def compute_agreement_rate(comparisons: list) -> float:
    if not comparisons:
        return 1.0
    agreements = [outputs_agree(live, shadow) for live, shadow in comparisons]
    return sum(agreements) / len(agreements)
