// Every CUDA problem must be self-consistent: its reference solution passes every case of its own harness
// (hidden ones included) on the simulator, and its starter code does NOT pass them all. This runs the same
// worker file the browser loads (platform/static/gpubox/worker.js) inside a Node vm.
import { describe, it, expect } from 'vitest';
import { createWorkerVm } from './worker-vm.mjs';
import { listCudaProblems } from './read-problems';
import { cudaListEntries, cudaNeighbours, isCudaId } from './cuda-course-index';
import { cudaToQuestionContent } from './to-question-content';
import { metricsKey } from './metrics-key.mjs';
import { performanceSection } from './read-problems';
import { detectLanguage } from '../code-execution/detect-language';
import { guideTabsFor } from '../ide-content/guide-tabs';

const problems = listCudaProblems();
const vm = createWorkerVm();

describe('CUDA problem bank', () => {
	it('has every problem from the handbook with unique ids and slugs', () => {
		expect(problems.length).toBeGreaterThanOrEqual(49);
		expect(new Set(problems.map((p) => p.id)).size).toBe(problems.length);
		expect(new Set(problems.map((p) => p.slug)).size).toBe(problems.length);
		expect(new Set(problems.map((p) => p.title)).size).toBe(problems.length);
	});

	it('turns each problem into an IDE question of kind cuda', () => {
		for (const p of problems) {
			const q = cudaToQuestionContent(p);
			expect(q.id).toBe(`cuda-${p.slug}`);
			expect(q.metadata.kind).toBe('cuda');
			expect(detectLanguage(q)).toBe('cuda');
			expect(guideTabsFor({ id: q.id, kind: q.metadata.kind }, [], null)).toEqual([
				'description',
				'solution',
				'discussion'
			]);
			expect(q.starterCode.trim().length).toBeGreaterThan(0);
			expect(q.testHarnessCode).toMatch(/cases|programs/);
		}
	});

	it('lists the course in order and walks prev/next inside it', () => {
		const ids = cudaListEntries().map((e) => e.id);
		expect(ids[0]).toBe('cuda-vector-addition');
		expect(isCudaId(ids[3])).toBe(true);
		expect(isCudaId('sheet-count-pairs')).toBe(false);
		expect(cudaNeighbours(ids[0])).toEqual({ prevId: null, nextId: ids[1] });
		expect(cudaNeighbours(ids[ids.length - 1]).nextId).toBeNull();
	});

	for (const p of problems) {
		it(
			`${p.id} ${p.slug}: reference passes all cases, starter does not`,
			{ timeout: 120_000 },
			() => {
				const solution = vm.call({ action: 'test', source: p.solution, harness: p.harness });
				expect(solution.ok, solution.error).toBe(true);
				const failed = solution.results.filter((r: { passed: boolean }) => !r.passed);
				expect(failed, JSON.stringify(failed)).toEqual([]);
				expect(solution.results.length).toBeGreaterThan(0);

				const starter = vm.call({ action: 'test', source: p.starter, harness: p.harness });
				const passed = starter.ok
					? starter.results.filter((r: { passed: boolean }) => r.passed).length
					: 0;
				const total = starter.ok ? starter.results.length : 1;
				expect(passed, 'the starter code must not already pass every case').toBeLessThan(total);
			}
		);
	}

	it('has fresh metrics for every problem and quotes them in the Solution tab', () => {
		for (const p of problems) {
			expect(p.metrics, `${p.id} needs "npm run cuda:metrics"`).not.toBeNull();
			expect(p.metrics?.key, `${p.id}: metrics.json is stale, run "npm run cuda:metrics"`).toBe(
				metricsKey(p.solution, p.harness)
			);
			const explanation = cudaToQuestionContent(p).explanationMarkdown;
			expect(explanation).toMatch(
				p.mode === 'program' ? /Cluster report/ : /Memory-bound or compute-bound/
			);
		}
		const relu = performanceSection(problems.find((p) => p.slug === 'relu')!.metrics);
		expect(relu).toContain('memory-bound');
		const tiled = performanceSection(
			problems.find((p) => p.slug === 'tiled-matrix-multiplication')!.metrics
		);
		expect(tiled).toContain('ridge point');
	});

	it('writes statements with LaTeX and a plain-text kernel signature (no code box)', () => {
		for (const p of problems) {
			expect(p.statement, p.id).toContain('class="cuda-signature"');
			expect(p.statement, p.id).not.toMatch(/### Kernel signature[\s\S]*?```cuda/);
		}
		expect(problems.find((p) => p.slug === 'leaky-relu')!.statement).toContain('\\begin{cases}');
	});

	it('does not flag any reference or starter as a syntax error', () => {
		for (const p of problems) {
			for (const source of [p.solution, p.starter]) {
				const r = vm.call({ action: 'check', source });
				expect(r.ok, `${p.id}: ${r.error}`).toBe(true);
			}
		}
	});

	describe('compile errors name the line', () => {
		const relu = problems.find((p) => p.slug === 'leaky-relu')!;
		const fail = (source: string) => {
			const r = vm.call({ action: 'test', source, harness: relu.harness });
			expect(r.ok).toBe(false);
			return r.error as string;
		};
		it('a missing closing brace', () => {
			expect(fail(relu.solution.replace(/\}\s*$/, ''))).toMatch(
				/Compile error \(line 1\).*never closed/s
			);
		});
		it('a missing closing parenthesis', () => {
			expect(fail(relu.solution.replace('if (i < N)', 'if (i < N'))).toMatch(
				/Compile error \(line 3\).*'\(' opened here/s
			);
		});
		it('an extra closing brace', () => {
			expect(fail(relu.solution + '\n}')).toMatch(/Compile error \(line \d+\).*Unexpected '\}'/s);
		});
		it('a missing semicolon', () => {
			expect(fail(relu.solution.replace('float x = X[i];', 'float x = X[i]'))).toMatch(
				/Compile error \(line 4\).*does not end with ';'/s
			);
		});
		it('an unclosed comment', () => {
			expect(fail(relu.solution.replace('int i', '/* oops\nint i'))).toMatch(
				/never closed with '\*\/'/
			);
		});
		it('an undeclared variable names the line where it first appears', () => {
			const r = vm.call({
				action: 'test',
				source: relu.solution.replace('alpha * x', 'alpa * x'),
				harness: relu.harness
			});
			expect(r.results[0].error).toMatch(/'alpa' is used but never declared.*line 5/);
		});
	});

	it('compiles once per source (compile cache)', () => {
		const p = problems[0];
		vm.call({ action: 'test', source: p.solution + '\n// cache probe', harness: p.harness });
		const again = vm.call({
			action: 'test',
			source: p.solution + '\n// cache probe',
			harness: p.harness
		});
		expect(again.cached).toBe(true);
	});

	it('reports a missing kernel with a helpful message', () => {
		const p = problems[0];
		const r = vm.call({
			action: 'test',
			source: '__global__ void other(float* x) { }',
			harness: p.harness
		});
		expect(r.results.every((c: { passed: boolean }) => !c.passed)).toBe(true);
		expect(r.results[0].error).toContain('was not found');
	});
});
