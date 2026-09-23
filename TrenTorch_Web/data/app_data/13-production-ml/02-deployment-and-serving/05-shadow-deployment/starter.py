def shadow_deploy(request, live_model_fn, shadow_model_fn) -> dict:
    """
    Runs BOTH the live model and a candidate "shadow" model on the
    same request -- but the caller only ever gets the LIVE model's
    output back as the real response. The shadow's output is computed
    and recorded for later comparison, but NEVER shown to the user or
    acted on -- that silence is the entire defining property of shadow
    deployment. If the shadow model errors, that must not affect the
    real response at all; just record the error instead.
    """
    # TODO: live_output = live_model_fn(request) (let this raise
    # normally -- the live model failing IS a real incident). Then try
    # shadow_output = shadow_model_fn(request), catching any Exception
    # into shadow_error (leaving shadow_output as None on failure).
    # Return {"response": live_output, "shadow_output": shadow_output,
    # "shadow_error": shadow_error}.
    pass


def outputs_agree(live_output, shadow_output, tolerance: float = 1e-9) -> bool:
    """
    Compares a live/shadow output pair for agreement -- numeric
    outputs are compared within a small floating-point tolerance,
    everything else with plain equality.
    """
    # TODO: if both are int/float, compare abs(live - shadow) <=
    # tolerance. Otherwise, plain equality.
    pass


def compute_agreement_rate(comparisons: list) -> float:
    """
    Given a list of (live_output, shadow_output) pairs collected over
    many shadow-deployed requests, returns the fraction that agreed --
    the real, practical signal a team watches before ever promoting a
    shadow model to be the new live one.
    """
    # TODO: if comparisons is empty, return 1.0. Otherwise, compute
    # outputs_agree for every pair and return the fraction that were True.
    pass
