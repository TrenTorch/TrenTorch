import { cleanup, render, screen } from '@testing-library/svelte';
import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest';
import ModulesPage from './+page.svelte';

const auth = vi.hoisted(() => ({ session: { isLoading: false, user: null as object | null } }));

vi.mock('$app/state', () => ({ page: { url: new URL('http://localhost/modules') } }));
vi.mock('$app/paths', () => ({ resolve: (path: string) => path }));
vi.mock('$processes/auth/session.svelte', () => auth);
vi.mock('$processes/progress-tracking/solved.svelte', () => ({
	solved: { slugs: new Set<string>(), isSolved: () => false }
}));
vi.mock('$processes/progress-tracking/recent.svelte', () => ({ recent: { get: () => undefined } }));

const props = { data: { cudaIds: ['cuda-a', 'cuda-b'], cudaChapters: 3 }, params: {}, form: null };

describe('modules hub', () => {
	beforeEach(() => {
		auth.session.user = null;
	});
	afterEach(cleanup);

	it('lists the three live domains as links into their pages', () => {
		render(ModulesPage, props);
		expect(screen.getByRole('link', { name: /AI Systems/ })).toHaveAttribute(
			'href',
			'/modules/aisys'
		);
		expect(screen.getByRole('link', { name: /GPU Programming/ })).toHaveAttribute(
			'href',
			'/modules/gpu'
		);
		expect(screen.getByRole('link', { name: /Software Engineering/ })).toHaveAttribute(
			'href',
			'/modules/software'
		);
	});

	it('shows the planned domains as soon, without links', () => {
		render(ModulesPage, props);
		expect(screen.getByRole('heading', { name: 'Robotics' })).toBeInTheDocument();
		expect(screen.queryByRole('link', { name: /Robotics|System Design/ })).toBeNull();
		expect(screen.getAllByText('soon')).toHaveLength(2);
	});

	it('tells a guest that opening a domain needs sign-in', () => {
		render(ModulesPage, props);
		expect(screen.getAllByText('Sign in to open')).toHaveLength(3);
	});

	it('does not show the sign-in tag to a signed-in user', () => {
		auth.session.user = {};
		render(ModulesPage, props);
		expect(screen.queryByText('Sign in to open')).toBeNull();
		expect(screen.getAllByText('Open')).toHaveLength(3);
	});
});
