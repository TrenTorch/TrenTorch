import hashlib
import math


def assign_variant(user_id: str, variant_names: list, weights: list) -> str:
    digest = hashlib.sha256(user_id.encode()).hexdigest()
    bucket = int(digest, 16) % 10_000
    total_weight = sum(weights)
    cumulative = 0.0
    threshold = bucket / 10_000 * total_weight
    for name, weight in zip(variant_names, weights):
        cumulative += weight
        if threshold < cumulative:
            return name
    return variant_names[-1]


def _standard_normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def evaluate_ab_test(conversions_control: int, visitors_control: int, conversions_treatment: int, visitors_treatment: int):
    p_control = conversions_control / visitors_control
    p_treatment = conversions_treatment / visitors_treatment
    p_pooled = (conversions_control + conversions_treatment) / (visitors_control + visitors_treatment)

    standard_error = math.sqrt(p_pooled * (1.0 - p_pooled) * (1.0 / visitors_control + 1.0 / visitors_treatment))
    z_statistic = (p_control - p_treatment) / standard_error
    p_value = 2.0 * (1.0 - _standard_normal_cdf(abs(z_statistic)))
    return z_statistic, p_value


def decide_rollback(z_statistic: float, p_value: float, alpha: float = 0.05) -> bool:
    is_significant = p_value < alpha
    treatment_is_worse = z_statistic > 0
    return is_significant and treatment_is_worse
