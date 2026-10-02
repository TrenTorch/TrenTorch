def safe_int(text, default: int) -> int:
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


def parse_pair(text: str):
    parts = text.split(":")
    if len(parts) != 2:
        return None
    try:
        a = int(parts[0])
        b = int(parts[1])
    except ValueError:
        return None
    return (a, b)


def run_steps(log: list, fail: bool) -> None:
    try:
        log.append("try")
        if fail:
            raise ValueError("x")
    except ValueError:
        log.append("except")
    else:
        log.append("else")
    finally:
        log.append("finally")


def count_convertible(items: list) -> int:
    count = 0
    for item in items:
        try:
            int(item)
        except (ValueError, TypeError):
            continue
        count += 1
    return count


def cleanup_return(log: list, flag: bool) -> str:
    try:
        if flag:
            return "early"
    finally:
        log.append("cleanup")
    return "end"
