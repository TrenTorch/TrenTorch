def countdown_with_skip(start: int) -> list:
    result = []
    current = start
    while current >= 1:
        if current == 3:
            current -= 1
            continue
        result.append(current)
        current -= 1
    return result


def find_first_negative(numbers: list) -> int | None:
    index = 0
    while index < len(numbers):
        if numbers[index] < 0:
            found = numbers[index]
            break
        index += 1
    else:
        return None
    return found
