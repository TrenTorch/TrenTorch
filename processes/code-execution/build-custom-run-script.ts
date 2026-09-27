import { SETUP_SCRIPT } from './pyodide-setup-script';
import { STUDENT_CODE_MARKER } from '../ide-content/harness-marker';

export function buildCustomRunScript(options: {
	codeB64: string;
	testB64: string;
	functionB64: string;
	argumentsB64: string;
	expectedB64: string;
}): string {
	const { codeB64, testB64, functionB64, argumentsB64, expectedB64 } = options;
	return `${SETUP_SCRIPT}

def __run_custom_case():
    with OutputCapture() as cap:
        exec_globals = {"__name__": "__main__"}
        error = None
        result_text = ""
        try:
            raw_test = base64.b64decode("${testB64}").decode("utf-8")
            marker = ${JSON.stringify(STUDENT_CODE_MARKER)}
            before_code = raw_test.partition(marker)[0] if marker in raw_test else ""
            exec(before_code, exec_globals)

            raw_code = base64.b64decode("${codeB64}").decode("utf-8")
            import linecache
            code_filename = "<student-code>"
            linecache.cache[code_filename] = (len(raw_code), None, raw_code.splitlines(True), code_filename)
            exec(compile(raw_code, code_filename, "exec"), exec_globals)

            function_name = base64.b64decode("${functionB64}").decode("utf-8").strip()
            arguments = json.loads(base64.b64decode("${argumentsB64}").decode("utf-8"))
            expected_text = base64.b64decode("${expectedB64}").decode("utf-8").strip()
            if not function_name:
                raise ValueError("Enter the function name to run.")
            if not isinstance(arguments, list):
                raise ValueError("Arguments must be a JSON array, for example [2, 3].")

            function = exec_globals.get(function_name)
            if not callable(function):
                raise NameError("No callable function named " + repr(function_name) + " was found.")

            actual = function(*arguments)

            def normalize(value):
                if isinstance(value, np.ndarray):
                    return value.tolist()
                if isinstance(value, np.generic):
                    return value.item()
                if isinstance(value, tuple):
                    return [normalize(item) for item in value]
                if isinstance(value, list):
                    return [normalize(item) for item in value]
                if isinstance(value, dict):
                    return {str(key): normalize(item) for key, item in value.items()}
                return value

            def values_match(actual, expected):
                if isinstance(actual, (int, float)) and not isinstance(actual, bool) and isinstance(expected, (int, float)) and not isinstance(expected, bool):
                    return abs(float(actual) - float(expected)) <= 1e-5
                if isinstance(actual, list) and isinstance(expected, list):
                    return len(actual) == len(expected) and all(values_match(a, e) for a, e in zip(actual, expected))
                if isinstance(actual, dict) and isinstance(expected, dict):
                    return actual.keys() == expected.keys() and all(values_match(actual[key], expected[key]) for key in actual)
                return actual == expected

            actual_value = normalize(actual)
            actual_json = json.dumps(actual_value, sort_keys=True)
            result_text = "Returned: " + actual_json
            if expected_text:
                expected_value = normalize(json.loads(expected_text))
                expected_json = json.dumps(expected_value, sort_keys=True)
                if values_match(actual_value, expected_value):
                    result_text += "\\nExpected result matched."
                else:
                    error = "Expected " + expected_json + ", got " + actual_json + "."
        except Exception:
            error = traceback.format_exc()

        output = cap.get_stdout()
        if result_text:
            output += ("\\n" if output else "") + result_text
        if cap.get_stderr():
            output += ("\\n" if output else "") + "[STDERR]\\n" + cap.get_stderr()
        return {"output": output, "error": error, "success": error is None}

json.dumps(__run_custom_case())
`;
}
