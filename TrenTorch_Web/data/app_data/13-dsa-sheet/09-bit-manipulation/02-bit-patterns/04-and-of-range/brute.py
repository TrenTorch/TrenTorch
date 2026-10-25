def and_of_range(left, right):
    result = left
    for value in range(left + 1, right + 1):
        result &= value
    return result
