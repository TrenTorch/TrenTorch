def apply_critique_revision_step(response: str, principle, critique_fn, revise_fn) -> dict:
    """
    Constitutional AI's core loop step (Bai et al., 2022): ask
    critique_fn whether `response` violates `principle` at all (it
    returns None if not, or a description of the problem if so); if it
    DID find a problem, ask revise_fn to produce a fixed response.
    Returns {"response": ..., "revised": bool, "critique": ... or
    None}. No HUMAN ever writes the critique or the revision here --
    both come from calling the model on itself.
    """
    # TODO: critique = critique_fn(response, principle). If critique is
    # None, return {"response": response, "revised": False,
    # "critique": None}. Otherwise, revised_response =
    # revise_fn(response, critique), and return {"response":
    # revised_response, "revised": True, "critique": critique}.
    pass


def constitutional_ai_pipeline(response: str, principles: list, critique_fn, revise_fn) -> dict:
    """
    Runs apply_critique_revision_step once per principle, IN ORDER,
    feeding each step's (possibly revised) response into the next
    principle's check -- a real response might get revised multiple
    times if it violates several principles. Returns {"final_response":
    ..., "critiques_applied": [list of every critique that actually
    triggered a revision, in order]}.
    """
    # TODO: loop over principles, calling apply_critique_revision_step
    # each time with the CURRENT (possibly already-revised) response,
    # updating current_response and collecting critiques whenever
    # step_result["revised"] is True.
    pass
