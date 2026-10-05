def running_sum(values: list, partitions: list) -> list:
    totals = {}
    result = []
    for value, partition in zip(values, partitions):
        totals[partition] = totals.get(partition, 0) + value
        result.append(totals[partition])
    return result


def rank(values: list, partitions: list) -> list:
    result = []
    for value, partition in zip(values, partitions):
        larger = sum(1 for v, p in zip(values, partitions) if p == partition and v > value)
        result.append(1 + larger)
    return result


def lag(values: list, partitions: list, offset: int, default=None) -> list:
    seen = {}
    result = []
    for value, partition in zip(values, partitions):
        history = seen.setdefault(partition, [])
        position = len(history) - offset
        result.append(history[position] if position >= 0 else default)
        history.append(value)
    return result


def moving_average(values: list, window: int) -> list:
    result = []
    for i in range(len(values)):
        chunk = values[max(0, i - window + 1) : i + 1]
        result.append(sum(chunk) / len(chunk))
    return result
