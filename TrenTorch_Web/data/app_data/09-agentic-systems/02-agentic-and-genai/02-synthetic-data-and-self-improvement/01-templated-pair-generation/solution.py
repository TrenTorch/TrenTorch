def generate_pairs(templates: list[str], variable_sets: list[dict[str, str]]) -> list[str]:
    pairs = []
    for template in templates:
        for variables in variable_sets:
            pairs.append(template.format(**variables))
    return pairs
