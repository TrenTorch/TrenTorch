def generate_pairs(templates: list[str], variable_sets: list[dict[str, str]]) -> list[str]:
    """Each template is a string with `{name}`-style placeholders. Return
    every combination of a template filled in with a variable set --
    template-major order: all of the first template's fills, in
    variable_sets order, then all of the second template's fills, and so
    on. `template.format(**variables)` fills in one template with one
    variable set.
    """
    # TODO: implement
    pass
