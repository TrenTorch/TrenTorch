import { SETUP_SCRIPT } from './pyodide-setup-script';
import { STUDENT_CODE_MARKER } from '../ide-content/harness-marker';

// The Python the worker runs for a 'test' request. Kept in one place so the
// worker and pyodide-check/questions.spec.ts (which runs every question through
// it) cannot drift apart.
//
// Order matters: the harness's first section (dependency solutions, renamed
// imports) runs before the student's code, so the code can use them while it is
// being defined; then the student's code; then the tests. See buildTestHarness.
export function buildTestRunnerScript(options: {
	codeB64: string;
	testB64: string;
	// Digits of the sample limit for "Run", empty for the whole suite on "Submit".
	limitArg: string;
}): string {
	const { codeB64, testB64, limitArg } = options;
	// Prefixed with SETUP_SCRIPT -- see its comment for why this script can't
	// just rely on that having already run once.
	return `${SETUP_SCRIPT}

def __run_module_tests():
    with OutputCapture() as cap:
        exec_globals = {"__name__": "__main__"}
        results = []
        raw_error = None
        try:
            raw_test = base64.b64decode("${testB64}").decode("utf-8")
            marker = ${JSON.stringify(STUDENT_CODE_MARKER)}
            if marker in raw_test:
                before_code, _, test_code = raw_test.partition(marker)
            else:
                before_code, test_code = "", raw_test

            # 1. Dependencies the student's code may use while it is defined
            exec(before_code, exec_globals)

            # 2. Execute student code
            raw_code = base64.b64decode("${codeB64}").decode("utf-8")
            exec(raw_code, exec_globals)

            # 3. Execute test harness
            exec(test_code, exec_globals)

            # 4. Call run_tests()
            if "run_tests" in exec_globals and callable(exec_globals["run_tests"]):
                results = exec_globals["run_tests"](${limitArg})
            else:
                raw_error = "Test harness does not contain a run_tests() function."
        except Exception as e:
            raw_error = traceback.format_exc()

        return {
            "stdout": cap.get_stdout(),
            "stderr": cap.get_stderr(),
            "error": raw_error,
            "results": results
        }

json.dumps(__run_module_tests())
`;
}
