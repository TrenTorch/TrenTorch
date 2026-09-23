import hashlib
import math


def assign_variant(user_id: str, variant_names: list, weights: list) -> str:
    """
    Deterministically assigns a user to one of several weighted A/B
    variants -- the SAME user_id always gets the SAME variant
    (04-canary-deployment's same deterministic-hash-routing idea,
    generalized from a single canary percentage to several named,
    weighted buckets), and across many users, each variant gets
    roughly its proportional share of traffic.
    """
    # TODO: hash user_id into a bucket in [0, 10000) (same technique as
    # 04-canary-deployment's hash_bucket). Scale that bucket by the
    # total weight to get a threshold. Walk variant_names/weights,
    # accumulating weight, and return the first variant whose
    # cumulative weight exceeds the threshold (fall back to the last
    # variant name as a safety net for floating-point edge cases).
    pass


def _standard_normal_cdf(x: float) -> float:
    """
    The standard normal CDF, Φ(x) -- computed via math.erf (available
    in the standard library) rather than depending on scipy, since
    scipy isn't part of this project's Pyodide runtime.
    """
    # TODO: 0.5 * (1 + math.erf(x / sqrt(2)))
    pass


def evaluate_ab_test(conversions_control: int, visitors_control: int, conversions_treatment: int, visitors_treatment: int):
    """
    A two-proportion z-test comparing the control (existing model) and
    treatment (new model) conversion rates. Returns (z_statistic,
    p_value): z_statistic POSITIVE means control outperformed
    treatment.
    """
    # TODO: p_control = conversions_control / visitors_control (same
    # for treatment). p_pooled = (both conversions summed) / (both
    # visitors summed). standard_error = sqrt(p_pooled * (1-p_pooled)
    # * (1/visitors_control + 1/visitors_treatment)). z_statistic =
    # (p_control - p_treatment) / standard_error. p_value = 2 * (1 -
    # _standard_normal_cdf(abs(z_statistic))). Return (z_statistic,
    # p_value).
    pass


def decide_rollback(z_statistic: float, p_value: float, alpha: float = 0.05) -> bool:
    """
    The actual decision rule: roll the new (treatment) model back
    ONLY when the difference is BOTH statistically significant
    (p_value < alpha) AND in the WRONG direction (control beat
    treatment, z_statistic > 0) -- a treatment that's merely no better
    (not significant) or genuinely better should never be rolled back.
    """
    # TODO: is_significant = p_value < alpha. treatment_is_worse =
    # z_statistic > 0. Return is_significant and treatment_is_worse.
    pass
