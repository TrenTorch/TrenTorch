def make_pipeline(*transformations):
    def pipeline(value):
        for transform in transformations:
            value = transform(value)
        return value

    def wrapper(value):
        wrapper.calls += 1
        return pipeline(value)

    wrapper.calls = 0
    return wrapper
