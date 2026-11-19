// Turns the raw error text of a failed check into something a student can read. The test
// harness raises plain strings ("Assertion failed: Wrong answer.\nInput: ...\nExpected: ...\nGot: ...",
// "Time limit exceeded: took 5031 ms, ...") and Python raises tracebacks; the results panel shows a
// title, a few labelled facts and an optional note instead of one wall of text.

export type FailureFact = { label: string; value: string };

export type ParsedFailure = {
	title: string;
	facts: FailureFact[];
	note?: string;
	/** The full Python traceback, for the student who wants it. */
	trace?: string;
};

const PREFIX = /^(?:Assertion failed|AssertionError):\s*/;

export function parseTestFailure(raw: string): ParsedFailure {
	const text = raw.trim().replace(PREFIX, '');

	const wrong = text.match(
		/^Wrong answer\.?\s*\nInput: ([\s\S]*?)\nExpected: ([\s\S]*?)\nGot: ([\s\S]*)$/
	);
	if (wrong) {
		return {
			title: 'Wrong answer',
			facts: [
				{ label: 'Input', value: wrong[1].trim() },
				{ label: 'Expected', value: wrong[2].trim() },
				{ label: 'Your output', value: wrong[3].trim() }
			]
		};
	}

	if (/^Wrong answer on a hidden test case/.test(text)) {
		return { title: 'Wrong answer', facts: [], note: 'The input of this test is hidden.' };
	}
	const random = text.match(/^Wrong answer on random case (\d+) of (\d+)/);
	if (random) {
		return { title: 'Wrong answer', facts: [], note: `Random case ${random[1]} of ${random[2]}.` };
	}

	const slow = text.match(/^Time limit exceeded: took (\d+) ms, the limit is (\d+) ms/);
	if (slow) {
		return {
			title: 'Time limit exceeded',
			facts: [
				{ label: 'Your code', value: `${slow[1]} ms` },
				{ label: 'Limit', value: `${slow[2]} ms` }
			],
			note: 'The answer is right but too slow. Look for a faster approach.'
		};
	}
	const slowBatch = text.match(
		/^Time limit exceeded: the random cases took (\d+) ms.*?limit is (\d+) ms/
	);
	if (slowBatch) {
		return {
			title: 'Time limit exceeded',
			facts: [
				{ label: 'Your code', value: `${slowBatch[1]} ms` },
				{ label: 'Limit', value: `${slowBatch[2]} ms` }
			],
			note: 'The answers are right but too slow. Look for a faster approach.'
		};
	}

	if (/^Skipped:/.test(text)) {
		return {
			title: 'Skipped',
			facts: [],
			note: text.replace(/^Skipped:\s*/, '').replace(/^./, (c) => c.toUpperCase())
		};
	}
	const runtime = text.match(/^Runtime error: ([\s\S]*)$/);
	if (runtime) {
		const lines = runtime[1].split('\n').filter((line) => line.trim());
		return {
			title: 'Runtime error',
			facts: [],
			note: lines[0],
			trace: lines.length > 1 ? runtime[1] : undefined
		};
	}

	const reads = text.match(
		/^Right answer, but too many reads: your code read the list (\d+) times and the limit is (\d+)/
	);
	if (reads) {
		return {
			title: 'Too many reads',
			facts: [
				{ label: 'Your code read', value: `${reads[1]} times` },
				{ label: 'Limit', value: reads[2] }
			],
			note: 'The answer is right, but reading every value is not allowed here. Halve the search range each step.'
		};
	}

	// A Python exception: the last line names it, the lines above are the traceback.
	const lines = text.split('\n').filter((line) => line.trim());
	if (
		/^Traceback \(most recent call last\)/m.test(text) ||
		/^\w*(Error|Exception|Interrupt)\b/.test(lines.at(-1) ?? '')
	) {
		const last = lines.at(-1) ?? text;
		return {
			title: last,
			facts: studentCodeFacts(text),
			trace: lines.length > 1 ? text : undefined
		};
	}

	return {
		title: lines[0] ?? 'This check failed',
		facts: [],
		note: lines.slice(1).join(' ') || undefined
	};
}

// The innermost traceback frame that is the student's own code, so a NameError or TypeError can point at
// the line that raised it instead of leaving the student to hunt through the full traceback.
function studentCodeFacts(trace: string): FailureFact[] {
	const frames = [
		...trace.matchAll(/^\s*File "<student-code>", line (\d+), in (.+)\n(?:\s+(.+)\n)?/gm)
	];
	const frame = frames.at(-1);
	if (!frame) return [];
	const where = frame[2] === '<module>' ? `line ${frame[1]}` : `line ${frame[1]}, in ${frame[2]}`;
	const source = frame[3]?.trim();
	return [{ label: 'Your code', value: source ? `${where}: ${source}` : where }];
}
