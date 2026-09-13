def pipeline_bubble_fraction(num_stages: int, num_microbatches: int) -> float:
    """
    The fraction of total pipeline wall-time spent idle ("bubble"),
    using the standard textbook model: (p - 1) / (p - 1 + m), where p
    is the number of pipeline stages and m the number of microbatches.
    """
    # TODO: implement
    pass


def pipeline_wall_time(num_stages: int, num_microbatches: int, microbatch_time: float) -> float:
    """
    Total wall-clock time for the whole pipeline to finish m
    microbatches across p stages: (p - 1 + m) * microbatch_time -- the
    p - 1 steps to fill/drain the pipeline, plus m steps of steady
    -state throughput.
    """
    # TODO: implement
    pass


def ideal_wall_time(num_microbatches: int, microbatch_time: float) -> float:
    """
    The wall-time a hypothetical ZERO-bubble pipeline would take: just
    m microbatches back to back, with no fill/drain overhead at all.
    """
    # TODO: implement
    pass


def pipeline_stage_utilization(num_stages: int, num_microbatches: int) -> float:
    """
    The fraction of time each stage is actually doing useful work --
    the complement of the bubble fraction.
    """
    # TODO: 1.0 - pipeline_bubble_fraction(num_stages, num_microbatches)
    pass
