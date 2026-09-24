def run_pipeline(values: list, *transformations, **options) -> list:
    unique = options.pop("unique", False)
    limit = options.pop("limit", None)
    if options:
        raise TypeError(f"Unsupported options: {sorted(options)}")

    if limit == 0:
        return []

    seen = set()
    result = []
    for value in values:
        for transform in transformations:
            value = transform(value)

        if unique:
            if value in seen:
                continue
            seen.add(value)

        result.append(value)
        if limit is not None and len(result) >= limit:
            break

    return result
