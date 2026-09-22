// Every test file gets the same generic collector appended: gather
// every module-level test_* function and run it, pytest-style, in the
// {name, passed, error} shape processes/code-execution/pyodide-worker.ts's
// run_tests() contract expects. Content authors never write this
// themselves -- they just write normal pytest, same as
// data/app_data/README.md documents.
//
// Two pytest behaviours are reproduced because question tests rely on them:
// - a `tmp_path` parameter gets a fresh temporary directory (a pathlib.Path),
//   removed again afterwards. Pyodide has an in-memory file system, so tests
//   that save and load a file work.
// - a failing bare `assert` has no message, so the error falls back to the
//   exception's name instead of an empty string.
// Any other fixture is named in the error rather than failing obscurely.
export const TEST_COLLECTOR = `

def _call_test(fn):
    import inspect

    parameters = list(inspect.signature(fn).parameters)
    if not parameters:
        return fn()
    unsupported = [name for name in parameters if name != "tmp_path"]
    if unsupported:
        raise TypeError(
            "pytest fixture " + repr(unsupported[0]) + " is not available in the in-browser test runner"
        )
    import shutil
    import tempfile
    from pathlib import Path

    directory = tempfile.mkdtemp()
    try:
        return fn(Path(directory))
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def run_tests(limit=None):
    _test_fns = sorted(
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    if limit is not None:
        _test_fns = _test_fns[:limit]
    tests = []
    for name, fn in _test_fns:
        try:
            _call_test(fn)
            tests.append({"name": name, "passed": True, "error": None})
        except Exception as e:
            tests.append({"name": name, "passed": False, "error": str(e) or type(e).__name__})
    return tests
`;
