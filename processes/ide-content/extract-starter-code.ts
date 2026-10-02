import { collapseSignatures } from './collapse-signatures';

// The problem statement always includes the function signature(s) to
// implement as its own fenced code block -- authors write that once,
// here, rather than duplicating it into a separate starter file. This
// pulls that first fence out verbatim (docstring included, no body) as
// the editor's starting content.
//
// The student's code execs standalone, before the test harness (which
// is where `import numpy as np` would otherwise come from) -- and every
// signature here is typed against np.ndarray. On Pyodide's actual
// Python (3.12), a parameter annotation is evaluated the moment `def`
// executes, so without this the very first Run on unmodified starter
// code crashes with NameError before a student writes anything. (This
// only reproduces on the interpreter version Pyodide actually ships --
// Python 3.14 defers annotation evaluation by default and would hide
// the bug entirely; always verify against 3.12 specifically.)
export function extractStarterCode(statementMarkdown: string): string {
	const match = statementMarkdown.match(/```python\n([\s\S]*?)```/);
	if (!match) return '';
	return `import numpy as np\n\n\n${collapseSignatures(match[1].trimEnd())}\n`;
}
