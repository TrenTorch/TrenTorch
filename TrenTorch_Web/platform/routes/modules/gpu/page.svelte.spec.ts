import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { afterEach, describe, it, expect, vi } from 'vitest';
import GpuPage from './+page.svelte';

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
		expect(screen.getByRole('button', { name: /Memory Performance/ })).toBeInTheDocument();
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
