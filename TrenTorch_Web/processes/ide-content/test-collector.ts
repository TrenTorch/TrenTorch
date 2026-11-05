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
// - assertion failures include the test source line and a readable fallback
//   when the author did not supply an assertion message.
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
    import contextlib
    import io
    import sys

    tests = []
    for name, fn in _test_fns:
        captured = io.StringIO()
        try:
            with contextlib.redirect_stdout(captured):
                _call_test(fn)
            tests.append({"name": name, "passed": True, "error": None})
        except Exception as e:
            if getattr(e, "skipped", False):
                tests.append({"name": name, "passed": True, "skipped": True, "error": str(e).strip()})
                continue
            import linecache
            import traceback

            detail = str(e).strip()
            if isinstance(e, AssertionError):
                reason = "Assertion failed: " + detail if detail else "Assertion failed; the expected condition was false."
            else:
                reason = type(e).__name__ + (": " + detail if detail else "")

            frames = traceback.extract_tb(e.__traceback__)
            frame = next((item for item in reversed(frames) if item.name == name), None)
            if frame:
                source = linecache.getline(frame.filename, frame.lineno).strip()
                if source:
                    reason += "\\nLine " + str(frame.lineno) + ": " + source

            tests.append({"name": name, "passed": False, "error": reason})
        finally:
            # What a test printed is shown with its result, and still reaches the Console.
            printed = captured.getvalue()
            if printed and tests:
                tests[-1]["stdout"] = printed
                sys.stdout.write(printed)
    return tests
`;
