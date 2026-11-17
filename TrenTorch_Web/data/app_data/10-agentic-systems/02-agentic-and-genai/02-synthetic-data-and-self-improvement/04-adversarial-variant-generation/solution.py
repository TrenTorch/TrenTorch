def generate_adversarial_variants(base_example: str, perturbations: dict[str, str]) -> list[str]:
    variants = []
    for find, replace in perturbations.items():
        if find in base_example:
            variants.append(base_example.replace(find, replace, 1))
    return variants
