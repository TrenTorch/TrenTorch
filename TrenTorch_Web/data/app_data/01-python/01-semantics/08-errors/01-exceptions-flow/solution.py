def validate_age(age: int) -> int:
    if not 0 <= age <= 150:
        raise ValueError("age must be between 0 and 150")
    return age


def level_three(log: list) -> None:
    log.append("L3 start")
    raise RuntimeError("boom")
    log.append("L3 end")


def level_two(log: list) -> None:
    log.append("L2 start")
    level_three(log)
    log.append("L2 end")


def level_one(log: list) -> None:
    log.append("L1 start")
    level_two(log)
    log.append("L1 end")


def first_element(items: list):
    return items[0]
