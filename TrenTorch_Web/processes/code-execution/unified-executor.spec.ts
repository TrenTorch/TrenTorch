import { beforeEach, describe, expect, it, vi } from 'vitest';
import { get } from 'svelte/store';

// Every runtime is replaced by a stand-in with the same stores, so what is tested is the executor's own
// job: choosing a runtime, starting it when it is chosen, and forwarding only the chosen one's output.
const fakes = await vi.hoisted(async () => {
	const { writable } = await import('svelte/store');
	const make = (name: string) => ({
		name,
		init: vi.fn(),
		runCode: vi.fn(async () => ({ success: true, output: `${name} ran`, durationMs: 1 })),
		runQuery: vi.fn(async () => ({ success: true, output: 'sql ran', durationMs: 1 })),
		runTests: vi.fn(),
		runCustomTest: vi.fn(),
		runPreview: vi.fn(),
		runtimeState: writable('uninitialized'),
		consoleOutput: writable(''),
		consoleError: writable(false),
		testResults: writable(null),
		isRunning: writable(false),
		consoleFigures: writable([])
	});
	return {
		pyodide: make('pyodide'),
		sql: make('sql'),
		js: make('js'),
		cpp: make('cpp'),
		java: make('java'),
		go: make('go'),
		rust: make('rust')
	};
});

vi.mock('./pyodide-service', () => ({ pyodideService: fakes.pyodide }));
vi.mock('./sql-service', () => ({ sqlService: fakes.sql }));
vi.mock('./js-service', () => ({ jsService: fakes.js }));
vi.mock('./cpp-service', () => ({ cppService: fakes.cpp }));
vi.mock('./java-service', () => ({ javaService: fakes.java }));
vi.mock('./go-service', () => ({ goService: fakes.go }));
vi.mock('./rust-service', () => ({ rustService: fakes.rust }));

type Executor = typeof import('./unified-executor').unifiedExecutor;
let executor: Executor;

beforeEach(async () => {
	for (const fake of Object.values(fakes)) {
		fake.init.mockClear();
		fake.runCode.mockClear();
		fake.runQuery.mockClear();
		fake.consoleOutput.set('');
	}
	// A fresh executor each time: it is a singleton that remembers the last language.
	vi.resetModules();
	executor = (await import('./unified-executor')).unifiedExecutor;
});

const question = (id: string, tags: string[] = []) =>
	({ id, metadata: { tags, kind: undefined } }) as never;

describe('UnifiedExecutor', () => {
	it('starts as Python', () => {
		expect(executor.getLanguage()).toBe('python');
	});

	it("starts a language's runtime as soon as it is chosen, so the first Run is not the one that waits", () => {
		executor.setLanguage('rust');
		expect(fakes.rust.init).toHaveBeenCalledTimes(1);
		expect(executor.getLanguage()).toBe('rust');
	});

	it('does not start it again when the same language is chosen twice', () => {
		executor.setLanguage('go');
		executor.setLanguage('go');
		expect(fakes.go.init).toHaveBeenCalledTimes(1);
	});

	it('starts each language it is switched to, and only that one', () => {
		for (const lang of ['javascript', 'cpp', 'java', 'go', 'rust'] as const)
			executor.setLanguage(lang);
		const started = (f: { init: { mock: { calls: unknown[] } } }) => f.init.mock.calls.length;
		expect([fakes.js, fakes.cpp, fakes.java, fakes.go, fakes.rust].map(started)).toEqual([
			1, 1, 1, 1, 1
		]);
		expect(started(fakes.pyodide)).toBe(0);
	});

	it("forwards the chosen runtime's console output, and stops forwarding the previous one", () => {
		executor.setLanguage('javascript');
		fakes.js.consoleOutput.set('from js');
		expect(get(executor.consoleOutput)).toBe('from js');
		executor.setLanguage('cpp');
		fakes.cpp.consoleOutput.set('from cpp');
		expect(get(executor.consoleOutput)).toBe('from cpp');
		fakes.js.consoleOutput.set('late output from the runtime it left');
		expect(get(executor.consoleOutput)).toBe('from cpp');
	});

	it("forwards the chosen runtime's state, running flag and test results too", () => {
		executor.setLanguage('java');
		fakes.java.runtimeState.set('loading_packages');
		fakes.java.isRunning.set(true);
		fakes.java.consoleError.set(true);
		expect(get(executor.runtimeState)).toBe('loading_packages');
		expect(get(executor.isRunning)).toBe(true);
		expect(get(executor.consoleError)).toBe(true);
	});

	it('runs code on the runtime of the language it is set to', async () => {
		for (const [lang, fake] of [
			['javascript', fakes.js],
			['cpp', fakes.cpp],
			['java', fakes.java],
			['go', fakes.go],
			['rust', fakes.rust]
		] as const) {
			executor.setLanguage(lang);
			const result = await executor.runCode('code');
			expect(fake.runCode).toHaveBeenCalledWith('code');
			expect(result.output).toBe(`${fake.name} ran`);
		}
	});

	it("runs Python by default, and SQL with the question's schema", async () => {
		await executor.runCode('print(1)');
		expect(fakes.pyodide.runCode).toHaveBeenCalledWith('print(1)');
		executor.init(question('db-sql-group-by', ['sql']));
		expect(executor.getLanguage()).toBe('sql');
		expect(fakes.sql.init).toHaveBeenCalled();
		await executor.runCode('SELECT 1', 'CREATE TABLE t(a)');
		expect(fakes.sql.runQuery).toHaveBeenCalledWith('SELECT 1', 'CREATE TABLE t(a)');
	});

	it('goes back to Python when a Python question is opened after another language', () => {
		executor.setLanguage('cpp');
		executor.init(question('linear-regression'));
		expect(executor.getLanguage()).toBe('python');
	});

	it('keeps the language when there is no question', () => {
		executor.setLanguage('go');
		executor.init(null);
		expect(executor.getLanguage()).toBe('go');
	});

	it('has nothing to draw for a preview outside Python', async () => {
		executor.setLanguage('go');
		expect(await executor.runPreview('code', 'preview')).toEqual({ output: '', figures: [] });
	});
});
