class Recorder:
    """
    A context manager that records events in a list.

    __init__(self, log): store the list `log`.
    __enter__(self): append "enter" to the log and return self.
    __exit__(self, exc_type, exc_value, traceback):
        Append "exit" to the log. If an exception occurred
        (exc_type is not None), also append
        "error:" followed by the exception type's label
        (exc_type.__name__), for example "error:ValueError",
        AFTER "exit". Do not suppress the exception (return
        False).
    """

    def __init__(self, log):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class SuppressAndRecord:
    """
    A context manager that suppresses one kind of exception.

    __init__(self, exception_type): store the type.
    __enter__(self): initialize an attribute `caught` to None
        and return self.
    __exit__(self, exc_type, exc_value, traceback):
        If an exception occurred and it is an instance of the
        stored type (use issubclass(exc_type, stored_type)),
        store the exception object in self.caught and return
        True (suppress it). Otherwise return False.
    """

    def __init__(self, exception_type):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def temporary_value(settings: dict, key, value):
    """
    A context manager written as a generator function decorated
    with contextlib.contextmanager (import it at the top of your
    solution).

    Set settings[key] = value at the start of the block, and
    restore settings[key] to its previous value at the end of the
    block, EVEN IF the block raises an exception. `key` exists in
    `settings` before the block starts. Yield nothing useful (a
    bare `yield`).
    """
    pass


def write_lines(path: str, lines: list) -> None:
    """
    Write each string in `lines` to the file at `path`, one per
    line (each followed by "\\n"), replacing any existing
    contents. Use `with open(path, "w") as f`.
    """
    pass


def read_lines(path: str) -> list:
    """
    Return a list of the lines of the file at `path` with the
    trailing newline of each line removed. Use `with open`. An
    empty file returns [].
    """
    pass
