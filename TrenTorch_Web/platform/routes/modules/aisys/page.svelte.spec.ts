import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { afterEach, describe, it, expect, vi } from 'vitest';
import { aiSystemsParts } from '$data/domains';
import AiSystemsPage from './+page.svelte';

vi.mock('$app/state', () => ({ page: { url: new URL('http://localhost/modules/aisys') } }));
vi.mock('$app/paths', () => ({ resolve: (path: string) => path }));
vi.mock('$app/environment', () => ({ browser: true }));
vi.mock('$processes/progress-tracking/solved.svelte', () => ({
	solved: { slugs: new Set<string>(), isSolved: () => false }
}));
vi.mock('$processes/progress-tracking/recent.svelte', () => ({ recent: { get: () => undefined } }));

const props = { data: { potdSummaries: [] }, params: {}, form: null };

describe('AI Systems page', () => {
	afterEach(cleanup);

	it('lists four modules a page, collapsed, and never research papers', () => {
		render(AiSystemsPage, props);
		for (const part of aiSystemsParts.slice(0, 4)) {
			expect(screen.getByRole('button', { name: new RegExp(part.title) })).toHaveAttribute(
				'aria-expanded',
				'false'
			);
		}
		expect(screen.queryByRole('button', { name: new RegExp(aiSystemsParts[4].title) })).toBeNull();
		expect(screen.queryByRole('button', { name: /Research Papers/i })).toBeNull();
		expect(screen.getByRole('button', { name: 'Next page' })).toBeInTheDocument();
	});

	it('opens a module in place, without leaving the page', async () => {
		render(AiSystemsPage, props);
		const first = screen.getByRole('button', { name: new RegExp(aiSystemsParts[0].title) });
		await fireEvent.click(first);
		expect(first).toHaveAttribute('aria-expanded', 'true');
		expect(screen.getByRole('heading', { name: 'AI Systems' })).toBeInTheDocument();
	});
});
