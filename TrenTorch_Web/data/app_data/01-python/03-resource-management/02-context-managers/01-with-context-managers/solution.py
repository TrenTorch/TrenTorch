from contextlib import contextmanager


class Recorder:
    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("enter")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.log.append("exit")
        if exc_type is not None:
            self.log.append(f"error:{exc_type.__name__}")
        return False


class SuppressAndRecord:
    def __init__(self, exception_type):
        self.exception_type = exception_type

    def __enter__(self):
        self.caught = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and issubclass(exc_type, self.exception_type):
            self.caught = exc_value
            return True
        return False


@contextmanager
def temporary_value(settings: dict, key, value):
    old = settings[key]
    settings[key] = value
    try:
        yield
    finally:
        settings[key] = old


def write_lines(path: str, lines: list) -> None:
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")


def read_lines(path: str) -> list:
    with open(path, "r") as f:
        return [line.rstrip("\n") for line in f]
