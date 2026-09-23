def generate_adversarial_variants(base_example: str, perturbations: dict[str, str]) -> list[str]:
    """`perturbations` maps a substring to find to its adversarial
    replacement. For each perturbation whose "find" substring actually
    appears in `base_example`, produce a variant with the FIRST occurrence
    of that substring replaced (leaving `base_example` itself untouched).
    Perturbations whose substring doesn't appear are skipped entirely.
    Return the list of variants, in the order `perturbations` was given.
    """
    # TODO: implement
    pass
