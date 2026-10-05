// Question tests are real pytest files (see data/app_data/README.md) and the
// in-browser runner collects their test_* functions itself, so there is no
// pytest package in Pyodide. Tests that write `import pytest` and use
// `pytest.raises` crashed with "ModuleNotFoundError: No module named 'pytest'"
// before any check ran. This registers a small stand-in module for the features
// the content uses: `raises` and `approx`. Anything else fails with a clear message
// instead of a confusing one, so a new pytest feature in a question is noticed
// straight away. `approx` follows pytest's rules (relative tolerance 1e-6 and absolute
// 1e-12 by default, `abs=` alone switches the relative part off, nested lists raise
// TypeError) so a test that passes here passes under real pytest too.
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

    class _Approx:
        # numpy must defer to __eq__ here when an array is on the left of ==
        __array_ufunc__ = None
        __array_priority__ = 100

        def __init__(self, expected, rel=None, abs=None, nan_ok=False):
            if isinstance(expected, (list, tuple)) and any(isinstance(e, (list, tuple, dict)) for e in expected):
                raise TypeError("pytest.approx() does not support nested data structures")
            self.expected = expected
            self.rel = rel
            self.abs = abs
            self.nan_ok = nan_ok

        def _tolerance(self, expected):
            import builtins

            if self.rel is None and self.abs is None:
                rel, absolute = 1e-6, 1e-12
            elif self.rel is None:
                rel, absolute = 0.0, self.abs
            elif self.abs is None:
                rel, absolute = self.rel, 1e-12
            else:
                rel, absolute = self.rel, self.abs
            return max(rel * builtins.abs(expected), absolute)

        def _close(self, actual, expected):
            import builtins
            import math

            if actual == expected:
                return True
            try:
                a, e = float(actual), float(expected)
            except (TypeError, ValueError):
                return False
            if a != a or e != e:
                return self.nan_ok and a != a and e != e
            if math.isinf(a) or math.isinf(e):
                return False
            return builtins.abs(a - e) <= self._tolerance(e)

        def __eq__(self, actual):
            expected = self.expected
            if isinstance(expected, dict):
                if not isinstance(actual, dict) or set(actual) != set(expected):
                    return False
                return all(self._close(actual[k], expected[k]) for k in expected)
            if getattr(expected, "ndim", 0) > 0 and hasattr(expected, "tolist"):  # arrays, not NumPy scalars
                if not hasattr(actual, "shape") and not isinstance(actual, (list, tuple)):
                    return False
                import numpy as _np

                actual_array = _np.asarray(actual)
                if actual_array.shape != expected.shape:
                    return False
                return all(self._close(a, e) for a, e in zip(actual_array.ravel().tolist(), expected.ravel().tolist()))
            if isinstance(expected, (list, tuple)):
                if hasattr(actual, "tolist"):
                    actual = actual.tolist()
                if not isinstance(actual, (list, tuple)) or len(actual) != len(expected):
                    return False
                return all(self._close(a, e) for a, e in zip(actual, expected))
            return self._close(actual, expected)

        def __ne__(self, actual):
            return not self.__eq__(actual)

        def __repr__(self):
            return "approx(" + repr(self.expected) + ")"

    def _pytest_unsupported(name):
        raise AttributeError("pytest." + name + " is not available in the in-browser test runner")

    _pytest_module = types.ModuleType("pytest")
    _pytest_module.raises = lambda expected, match=None: _RaisesContext(expected, match)
    _pytest_module.approx = _Approx
    _pytest_module.__getattr__ = _pytest_unsupported
    sys.modules["pytest"] = _pytest_module
`;
