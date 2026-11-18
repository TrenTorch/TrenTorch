def pipeline_bubble_fraction(num_stages: int, num_microbatches: int) -> float:
    return (num_stages - 1) / (num_stages - 1 + num_microbatches)

def pipeline_wall_time(num_stages: int, num_microbatches: int, microbatch_time: float) -> float:
    return (num_stages - 1 + num_microbatches) * microbatch_time

def ideal_wall_time(num_microbatches: int, microbatch_time: float) -> float:
    return num_microbatches * microbatch_time

def pipeline_stage_utilization(num_stages: int, num_microbatches: int) -> float:
    return 1.0 - pipeline_bubble_fraction(num_stages, num_microbatches)
