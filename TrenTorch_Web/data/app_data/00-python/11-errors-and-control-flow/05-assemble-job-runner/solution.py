class TransientError(Exception):
    pass


class JobFailedError(Exception):
    def __init__(self, label, attempts):
        super().__init__(f"job {label} failed after {attempts} attempt(s)")
        self.label = label
        self.attempts = attempts


class JobLogger:
    def __init__(self, label, log):
        self.label = label
        self.log = log

    def __enter__(self):
        self.log.append(f"start {self.label}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.log.append(f"end {self.label}")
        return False


def run_job(label: str, func, max_attempts: int, log: list):
    with JobLogger(label, log):
        last_transient = None
        for n in range(1, max_attempts + 1):
            log.append(f"attempt {n}")
            try:
                result = func()
            except TransientError as e:
                last_transient = e
                continue
            except Exception as e:
                raise JobFailedError(label, n) from e
            else:
                return result
        raise JobFailedError(label, max_attempts) from last_transient


def run_jobs(jobs: list, max_attempts: int, log: list) -> dict:
    results = {}
    failed = {}
    for label, func in jobs:
        try:
            results[label] = run_job(label, func, max_attempts, log)
        except JobFailedError as e:
            failed[label] = e.attempts
    return {"results": results, "failed": failed}
