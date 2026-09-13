def apply_critique_revision_step(response: str, principle, critique_fn, revise_fn) -> dict:
    critique = critique_fn(response, principle)
    if critique is None:
        return {"response": response, "revised": False, "critique": None}
    revised_response = revise_fn(response, critique)
    return {"response": revised_response, "revised": True, "critique": critique}


def constitutional_ai_pipeline(response: str, principles: list, critique_fn, revise_fn) -> dict:
    current_response = response
    critiques_applied = []
    for principle in principles:
        step_result = apply_critique_revision_step(current_response, principle, critique_fn, revise_fn)
        current_response = step_result["response"]
        if step_result["revised"]:
            critiques_applied.append(step_result["critique"])
    return {"final_response": current_response, "critiques_applied": critiques_applied}
