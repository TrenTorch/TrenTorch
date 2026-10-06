import { SETUP_SCRIPT } from './pyodide-setup-script';
import { STUDENT_FILENAME } from './python-error-format';

// The Python the worker runs for a 'run' request: execute the student's code and
// hand back what it printed and, if it failed, the error as Python would show it
// (see python-error-format.ts). Kept in one place, like the other two runner
// scripts, so the worker and pyodide-check/runner-behaviour.spec.ts cannot drift.
export function buildRunScript(options: { codeB64: string }): string {
	const { codeB64 } = options;
	// Prefixed with SETUP_SCRIPT -- see its comment for why this script can't
	// just rely on that having already run once.
	return `${SETUP_SCRIPT}

def __run_user_code():
    with OutputCapture() as cap:
        exec_globals = {"__name__": "__main__"}
        err = None
        try:
            raw_code = base64.b64decode("${codeB64}").decode("utf-8")
            exec(compile_user_code(raw_code, ${JSON.stringify(STUDENT_FILENAME)}), exec_globals)
        except BaseException as e:
            err = user_error_text(e)
        return {
            "stdout": cap.get_stdout(),
            "stderr": cap.get_stderr(),
            "error": err
        }

json.dumps(__run_user_code())
`;
}
