def sum_with_index(numbers: list) -> dict:
    result = {}
    running_total = 0
    for index, value in enumerate(numbers):
        running_total += value
        result[index] = running_total
    return result


def manual_iteration_trace(items: list) -> list:
    result = []
    iterator = iter(items)
    while True:
        try:
            result.append(next(iterator))
        except StopIteration:
            break
    return result
