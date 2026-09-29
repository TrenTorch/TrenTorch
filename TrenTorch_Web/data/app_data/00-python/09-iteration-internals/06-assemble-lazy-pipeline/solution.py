def build_pipeline(source, transformations=(), predicates=()):
    for value in source:
        for transform in transformations:
            value = transform(value)

        passed = True
        for predicate in predicates:
            if not predicate(value):
                passed = False
                break

        if passed:
            yield value
