import { PYTEST_SHIM } from './pytest-shim';

// Imports + OutputCapture, shared by the one-time setup in
// initialize-pyodide.ts AND prepended to every run/test script (see
// pyodide-worker.ts's 'run' and 'test' action handlers). Two separate
// runPythonAsync calls are supposed to share one persistent
// pyodide.globals -- in practice, a run/test request that lands while
// the one-time setup is still executing (student clicks Run/Submit in
// the first second or two of the page, before "ready") can still hit
// `NameError: name 'json'` or `NameError: name 'OutputCapture'`,
// reproduced directly: the JS-level `await` chain guarantees ordering
// of the *outer* promises, not that the interpreter-level globals from
// one runPythonAsync call are visible to the very next one issued in
// quick succession. Redefining a class is a harmless no-op the second
// time, so making every script self-contained removes the dependency
// on that ordering entirely instead of relying on it being fixed
// upstream.
export const SETUP_SCRIPT = `
import sys
import io
import json
import base64
import traceback
import numpy as np
${PYTEST_SHIM}
class OutputCapture:
    def __init__(self):
        self.stdout = io.StringIO()
        self.stderr = io.StringIO()
        self._old_stdout = None
        self._old_stderr = None

    def __enter__(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

    def get_stdout(self):
        return self.stdout.getvalue()

    def get_stderr(self):
        return self.stderr.getvalue()
`;
