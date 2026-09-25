class TransientError(Exception):
    """
    A temporary failure that may succeed if tried again.
    A plain subclass of Exception; no other behavior needed.
    """

    pass


class JobFailedError(Exception):
    """
    Raised when a job cannot be completed.

    __init__(self, label, attempts):
        Call the parent's __init__ with the message
            f"job {label} failed after {attempts} attempt(s)"
        and store `label` and `attempts` as attributes.
    """

    def __init__(self, label, attempts):
        pass


class JobLogger:
    """
    A context manager that logs around a job.

    __init__(self, label, log): store both.
    __enter__(self): append f"start {label}" to the log and
        return self.
    __exit__(self, exc_type, exc_value, traceback): append
        f"end {label}" to the log, always. Never suppress an
        exception (return False).
    """

    def __init__(self, label, log):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def run_job(label: str, func, max_attempts: int, log: list):
    """
    Run `func()` (a function taking no arguments) as one job.

    Everything below happens inside `with JobLogger(label, log):`
    so "start"/"end" entries are always written.

    Make up to `max_attempts` attempts (max_attempts >= 1):
      - Before each attempt append f"attempt {n}" to the log,
        where n counts from 1.
      - If func() returns, return that value immediately (use the
        try statement's `else` block for the return).
      - If func() raises TransientError, try again if attempts
        remain.
      - If func() raises any other Exception, do NOT retry:
        raise JobFailedError(label, n) chained (`from`) to that
        exception, where n is the attempt just made.
    If every attempt raised TransientError, raise
    JobFailedError(label, max_attempts) chained to the last
    TransientError.
    """
    pass


def run_jobs(jobs: list, max_attempts: int, log: list) -> dict:
    """
    `jobs` is a list of (label, func) tuples. Run each job in
    order with run_job(label, func, max_attempts, log). A failing
    job must not stop the remaining jobs.

    Return a dictionary with two keys:
      "results": dict mapping the label of each successful job to
                 its returned value
      "failed":  dict mapping the label of each failed job to the
                 number of attempts recorded on its
                 JobFailedError
    """
    pass
