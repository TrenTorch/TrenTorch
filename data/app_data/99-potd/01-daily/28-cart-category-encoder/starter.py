def encode_departments(departments: list[str]) -> tuple[list[str], list[list[int]]]:
    """
    One-hot encode a categorical department column, alphabetical columns.

    departments: n department names, may repeat.

    Return (distinct, rows), same convention as the amenity encoder:
    distinct is the k distinct departments sorted alphabetically, rows is
    n one-hot rows of length k. Names sharing a prefix ("dairy" vs
    "dairy_alt") are still distinct categories.
    """
    # TODO: sorted(set(departments)) gives the alphabetical column order directly.
    pass
