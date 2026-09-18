def build_capstone_report(
    project_name: str, baseline_stats: dict, optimized_stats: dict, correctness_verified: bool
) -> dict:
    """
    Assembles 02-apply-optimization-measure-improvement's raw
    benchmark numbers into a structured capstone submission: a
    project only "passes" if it's BOTH verified correct AND actually
    faster than the baseline -- a big speedup on broken code, or a
    "correct but slower" result, is not a passing submission.
    """
    # TODO: speedup_factor = baseline_stats["median"] /
    # optimized_stats["median"]. passed = correctness_verified and
    # speedup_factor > 1.0. Build a one-line f-string `summary`
    # mentioning project_name, the speedup (formatted to 2 decimals),
    # and whether correctness was verified. Return a dict with keys
    # "project_name", "speedup_factor", "correctness_verified",
    # "passed", "summary".
    pass


def compare_capstone_reports(reports: list) -> dict:
    """
    Given several build_capstone_report results (e.g. one per
    submitted project), finds the best PASSING one by speedup_factor
    -- a fast-but-broken submission must never win over a slower,
    genuinely correct one.
    """
    # TODO: filter reports to only "passed" ones. If none pass, return
    # {"best_project": None, "best_speedup_factor": None,
    # "num_passing": 0}. Otherwise, find the passing report with the
    # highest speedup_factor and return {"best_project": its
    # project_name, "best_speedup_factor": its speedup_factor,
    # "num_passing": how many passed}.
    pass
