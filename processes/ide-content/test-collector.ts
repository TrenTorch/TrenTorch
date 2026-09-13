// Every test file gets the same generic collector appended: gather
// every module-level test_* function and run it, pytest-style, in the
// {name, passed, error} shape processes/code-execution/pyodide-worker.ts's
// run_tests() contract expects. Content authors never write this
// themselves -- they just write normal pytest, same as
// data/app_data/README.md documents.
export const TEST_COLLECTOR = `

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
            fn()
            tests.append({"name": name, "passed": True, "error": None})
        except Exception as e:
            tests.append({"name": name, "passed": False, "error": str(e)})
    return tests
`;
