import { STUDENT_FILENAME } from '../code-execution/python-error-format';

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
// - pytest.mark.parametrize runs the test once per case, named test_x[id], and a
//   skipped test (pytest.skip(), mark.skip, mark.skipif) is left out of the results
//   instead of being counted as a pass or a failure. The shim records both on the
//   function (see code-execution/pytest-shim.ts).
// Any other fixture is named in the error rather than failing obscurely.
export const TEST_COLLECTOR = `

def _call_test(fn, given=None):
    import inspect

    given = given or {}
    parameters = [name for name in inspect.signature(fn).parameters if name not in given]
    if not parameters:
        return fn(**given)
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
        return fn(Path(directory), **given)
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def _param_cases(fn):
    """[(suffix, {argument: value})] for a test: one empty case unless it is parametrized."""
    cases = [("", {})]
    for argnames, argvalues, ids in getattr(fn, "__trentorch_params__", []):
        names = [n.strip() for n in argnames.split(",")] if isinstance(argnames, str) else list(argnames)
        expanded = []
        for index, value in enumerate(argvalues):
            row = (value,) if len(names) == 1 else tuple(value)
            if ids is not None and index < len(ids) and ids[index] is not None:
                label = str(ids[index])
            else:
                label = "-".join(
                    str(v) if isinstance(v, (str, int, float, bool, type(None))) else names[i] + str(index)
                    for i, v in enumerate(row)
                )
            expanded.append((label, dict(zip(names, row))))
        cases = [
            ((before + "-" + label) if before else label, {**given, **more})
            for before, given in cases
            for label, more in expanded
        ]
    return cases


def run_tests(limit=None):
    _test_fns = sorted(
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    )
    # Skipped tests are not run and not reported; neither is a pass.
    _cases = [
        (name + ("[" + suffix + "]" if suffix else ""), name, fn, given)
        for name, fn in _test_fns
        if getattr(fn, "__trentorch_skip__", None) is None
        for suffix, given in _param_cases(fn)
    ]
    if limit is not None:
        _cases = _cases[:limit]
    tests = []
    for label, name, fn, given in _cases:
        try:
            _call_test(fn, given)
            tests.append({"name": label, "passed": True, "error": None})
        except BaseException as e:
            if type(e).__name__ == "Skipped":
                continue
            import linecache
            import traceback

            detail = str(e).strip()
            if isinstance(e, AssertionError):
                reason = "Assertion failed: " + detail if detail else "Assertion failed; the expected condition was false."
            elif isinstance(e, SystemExit):
                # Not an Exception, so it would otherwise end the whole run.
                reason = "SystemExit: your code called sys.exit(" + (repr(e.code) if e.code is not None else "") + ")"
            else:
                reason = type(e).__name__ + (": " + detail if detail else "")

            frames = traceback.extract_tb(e.__traceback__)
            frame = next((item for item in reversed(frames) if item.name == name), None)
            if frame:
                source = linecache.getline(frame.filename, frame.lineno).strip()
                if source:
                    reason += "\\nLine " + str(frame.lineno) + ": " + source

            # Where in the student's own code it went wrong, when it did: the
            # test line alone says only which call failed, not what inside it.
            mine = next((item for item in reversed(frames) if item.filename == ${JSON.stringify(STUDENT_FILENAME)}), None)
            if mine and not isinstance(e, AssertionError):
                source = linecache.getline(mine.filename, mine.lineno).strip()
                where = "line " + str(mine.lineno) + (" in " + mine.name if mine.name != "<module>" else "")
                reason += "\\nYour code, " + where + (": " + source if source else "")

            tests.append({"name": label, "passed": False, "error": reason})
    return tests
`;
