import numpy as np


def alignment_tax(base_model_scores: np.ndarray, aligned_model_scores: np.ndarray) -> float:
    """
    The average capability REGRESSION an alignment procedure (RLHF,
    DPO, etc.) causes across a suite of public capability benchmarks:
    the mean of (base_model_score - aligned_model_score) across
    matching benchmark pairs. Positive means the aligned model is, on
    average, LESS capable than the base model it was aligned from.
    """
    # TODO: mean(base_model_scores - aligned_model_scores)
    pass


def per_benchmark_regression(base_model_scores: np.ndarray, aligned_model_scores: np.ndarray) -> np.ndarray:
    """
    The SAME comparison as alignment_tax, but per benchmark instead of
    averaged -- alignment can help some benchmarks and hurt others,
    and this shows the full picture rather than a single number.
    """
    # TODO: base_model_scores - aligned_model_scores (elementwise)
    pass


def has_net_alignment_tax(base_model_scores: np.ndarray, aligned_model_scores: np.ndarray) -> bool:
    """
    Whether the alignment procedure incurred a NET capability cost
    overall (a positive average tax), even if it improved some
    individual benchmarks along the way.
    """
    # TODO: alignment_tax(...) > 0.0
    pass
