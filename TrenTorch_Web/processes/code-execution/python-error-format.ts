// Python helpers shared by every script the worker runs (see
// pyodide-setup-script.ts), so the three ways of running code -- Run, custom
// input and the test suite -- report problems the same way.
//
// What a student should see is what Python on their own machine would show:
// the frames of their code, then the error line. Frames from the runner itself
// (`File "<exec>", line 76, in __run_user_code`, `_pyodide/_base.py`) are noise
// they cannot act on, so only frames from code compiled under USER_FILENAMES
// are kept. Library frames are dropped for the same reason: the student's own
// call into the library is still listed, and that is the frame they can fix.
export const STUDENT_FILENAME = '<student-code>';
export const TESTS_FILENAME = '<trentorch-tests>';
export const PREVIEW_FILENAME = '<trentorch-preview>';

export const PYTHON_ERROR_FORMAT = `
import linecache

USER_FILENAMES = (${JSON.stringify(STUDENT_FILENAME)}, ${JSON.stringify(TESTS_FILENAME)}, ${JSON.stringify(PREVIEW_FILENAME)})


def compile_user_code(source, filename):
    # Registering the source lets tracebacks print the offending line, which a
    # bare exec() of a string cannot do.
    linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
    return compile(source, filename, "exec")


def user_error_text(error):
    """The traceback Python would print, limited to the student's frames.

    Returns None for a clean exit (sys.exit() or sys.exit(0)): a program that
    asks to stop is not a failure.
    """
    if isinstance(error, SystemExit):
        code = error.code
        if code is None or code == 0:
            return None
        return "Process exited with status " + str(code) + " (sys.exit was called)."
    frames = [f for f in traceback.extract_tb(error.__traceback__) if f.filename in USER_FILENAMES]
    text = ""
    if frames:
        text = "Traceback (most recent call last):\\n" + "".join(traceback.format_list(frames))
    return text + "".join(traceback.format_exception_only(type(error), error))
`;
