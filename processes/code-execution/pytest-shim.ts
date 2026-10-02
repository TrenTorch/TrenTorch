// Question tests are real pytest files (see data/app_data/README.md) and the
// in-browser runner collects their test_* functions itself, so there is no
// pytest package in Pyodide. Tests that write `import pytest` and use
// `pytest.raises` crashed with "ModuleNotFoundError: No module named 'pytest'"
// before any check ran. This registers a small stand-in module for the one
// feature the content uses. Anything else fails with a clear message instead of
// a confusing one, so a new pytest feature in a question is noticed straight away.
//
// Guarded on sys.modules so it is a no-op if a real pytest is ever available,
// and plain Python with no dependencies so it can be tested outside Pyodide.
export const PYTEST_SHIM = `
if "pytest" not in sys.modules:
    import types

    class _RaisesContext:
        def __init__(self, expected, match=None):
            self.expected = expected
            self.match = match
            self.type = None
            self.value = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, exc_tb):
            if exc_type is None:
                name = getattr(self.expected, "__name__", str(self.expected))
                raise AssertionError("DID NOT RAISE " + name)
            if not issubclass(exc_type, self.expected):
                return False
            self.type = exc_type
            self.value = exc_value
            if self.match is not None:
                import re
                if not re.search(self.match, str(exc_value)):
                    raise AssertionError(
                        "Regex pattern " + repr(self.match) + " does not match " + repr(str(exc_value))
                    )
            return True

    def _pytest_unsupported(name):
        raise AttributeError("pytest." + name + " is not available in the in-browser test runner")

    _pytest_module = types.ModuleType("pytest")
    _pytest_module.raises = lambda expected, match=None: _RaisesContext(expected, match)
    _pytest_module.__getattr__ = _pytest_unsupported
    sys.modules["pytest"] = _pytest_module
`;
