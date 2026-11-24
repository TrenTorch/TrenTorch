import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { afterEach, describe, it, expect, vi } from 'vitest';
import GpuPage from './+page.svelte';
import type { CudaListEntry } from '$processes/cuda/cuda-course-index';

vi.mock('$app/state', () => ({ page: { url: new URL('http://localhost/modules/gpu') } }));
vi.mock('$app/paths', () => ({ resolve: (path: string) => path }));
vi.mock('$app/environment', () => ({ browser: true }));
vi.mock('$processes/progress-tracking/solved.svelte', () => ({
	solved: { slugs: new Set<string>(), isSolved: () => false }
}));
vi.mock('$processes/progress-tracking/attempted.svelte', () => ({
	attempted: { slugs: new Set<string>() }
}));
vi.mock('$processes/progress-tracking/recent.svelte', () => ({
	recent: { get: () => undefined, note: () => {} }
}));

const chapter = (part: string, n: number) => ({
	step: `chapter-${part}-${n}`,
	id: `${part}${n}`,
	title: `Chapter ${part}${n}`,
	part,
	estMinutes: 10
});
const props = {
	data: {
		problems: [],
		chapters: ['A', 'B', 'C', 'D', 'E'].flatMap((part) => [chapter(part, 1), chapter(part, 2)])
	},
	params: {},
	form: null
} as never;

describe('GPU Programming page', () => {
	afterEach(cleanup);

	it('lists four parts a page, collapsed, with paging', () => {
		render(GpuPage, props);
		expect(screen.getByRole('button', { name: /GPU Foundations/ })).toHaveAttribute(
			'aria-expanded',
			'false'
		);
		expect(screen.getByRole('button', { name: /The Programming Model/ })).toBeInTheDocument();
		expect(screen.queryByRole('button', { name: /Parallel Patterns/ })).toBeNull();
		expect(screen.getByRole('button', { name: 'Next page' })).toBeInTheDocument();
	});

	it('opens a part in place and lists its chapters', async () => {
		render(GpuPage, props);
		await fireEvent.click(screen.getByRole('button', { name: /GPU Foundations/ }));
		expect(screen.getByRole('link', { name: /Chapter A1/ })).toHaveAttribute(
			'href',
			'/modules/gpu/theory/[chapter]'
		);
	});
});

vi.stubGlobal(
	'ResizeObserver',
	class {
		observe() {}
		unobserve() {}
		disconnect() {}
	}
);

const filterProblems: CudaListEntry[] = [
	{
		id: 'cuda-vector-add',
		number: 'CU-001',
		title: 'Vector add',
		difficulty: 'Beginner',
		stage: 1,
		topics: ['map']
	},
	{
		id: 'cuda-fused-attention',
		number: 'CU-002',
		title: 'Fused attention',
		difficulty: 'Advanced',
		stage: 7,
		topics: ['shared-memory']
	}
];
const filterProps = {
	data: {
		problems: filterProblems,
		chapters: [
			{ step: 'a1', id: 'A1', title: 'What a GPU is', part: 'A', estMinutes: 10 },
			{ step: 'b1', id: 'B1', title: 'Threads and blocks', part: 'B', estMinutes: 12 }
		]
	},
	params: {},
	form: null
} as never;

const searchInput = () => screen.getByPlaceholderText('Search chapters, problems or topics...');
const pressFilter = async (name: string) => {
	await fireEvent.click(screen.getByRole('button', { name: /^Filters/ }));
	await fireEvent.click(screen.getByRole('button', { name }));
};

describe('GPU Programming page filters', () => {
	afterEach(cleanup);

	it('hides theory when a problem-only filter is active', async () => {
		render(GpuPage, filterProps);
		await pressFilter('Advanced');
		expect(screen.queryByRole('button', { name: /The Programming Model/ })).toBeNull();
		expect(screen.getByText('Fused attention')).toBeInTheDocument();
		expect(screen.queryByText('Vector add')).toBeNull();
	});

	it('keeps theory visible and narrowed for a text search', async () => {
		render(GpuPage, filterProps);
		await fireEvent.input(searchInput(), { target: { value: 'threads' } });
		expect(screen.getByText('Threads and blocks')).toBeInTheDocument();
		expect(screen.queryByRole('button', { name: /GPU Foundations/ })).toBeNull();
	});

	it('lets users collapse and reopen a stage while filtering', async () => {
		render(GpuPage, filterProps);
		await pressFilter('Advanced');
		const stage = () => screen.getByRole('button', { name: /Advanced, debugging and multi-GPU/ });
		expect(stage()).toHaveAttribute('aria-expanded', 'true');
		await fireEvent.click(stage());
		expect(stage()).toHaveAttribute('aria-expanded', 'false');
		expect(screen.queryByText('Fused attention')).toBeNull();
		await fireEvent.click(stage());
		expect(screen.getByText('Fused attention')).toBeInTheDocument();
	});

	it('lets users collapse and reopen a theory part while searching', async () => {
		render(GpuPage, filterProps);
		await fireEvent.input(searchInput(), { target: { value: 'threads' } });
		const part = () => screen.getByRole('button', { name: /The Programming Model/ });
		expect(part()).toHaveAttribute('aria-expanded', 'true');
		await fireEvent.click(part());
		expect(screen.queryByText('Threads and blocks')).toBeNull();
		await fireEvent.click(part());
		expect(screen.getByText('Threads and blocks')).toBeInTheDocument();
	});

	it('opens sections again when the search changes', async () => {
		render(GpuPage, filterProps);
		await fireEvent.input(searchInput(), { target: { value: 'threads' } });
		await fireEvent.click(screen.getByRole('button', { name: /The Programming Model/ }));
		expect(screen.queryByText('Threads and blocks')).toBeNull();
		await fireEvent.input(searchInput(), { target: { value: 'thread' } });
		expect(screen.getByText('Threads and blocks')).toBeInTheDocument();
	});

	it('goes back to the normal collapsed state when filters are cleared', async () => {
		render(GpuPage, filterProps);
		await fireEvent.input(searchInput(), { target: { value: 'threads' } });
		await fireEvent.input(searchInput(), { target: { value: '' } });
		expect(screen.getByRole('button', { name: /The Programming Model/ })).toHaveAttribute(
			'aria-expanded',
			'false'
		);
	});
});
