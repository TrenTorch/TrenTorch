// buildTestHarness returns one string, but it has two parts that run on either
// side of the student's code: the dependency solutions and helpers the student's
// code may use while it is being defined (a base class to subclass, a function
// used as a default argument), and the tests themselves. This line separates
// them; the runner in processes/code-execution/build-test-runner-script.ts splits
// on it. A harness without the marker is treated as all tests, as before.
export const STUDENT_CODE_MARKER = '# __student_code_runs_here__';
