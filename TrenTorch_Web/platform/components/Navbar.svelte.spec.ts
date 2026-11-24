import { cleanup, render, screen, within } from '@testing-library/svelte';
import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest';
import Navbar from './Navbar.svelte';

vi.mock('$app/state', () => ({ page: { url: new URL('http://localhost/') } }));
vi.mock('$app/paths', () => ({ resolve: (path: string) => path }));

describe('Navbar', () => {
	beforeEach(() => {
		vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false }));
		render(Navbar);
	});
	afterEach(() => {
		cleanup();
		vi.unstubAllGlobals();
	});

	const menu = (name: string) => {
		const button = screen.getByRole('button', { name });
		return within(button.parentElement as HTMLElement);
	};

	it('lists Problem of the day and Problemset under Practice', () => {
		const practice = menu('Practice');
		expect(practice.getByRole('menuitem', { name: /Problem of the day/ })).toHaveAttribute(
			'href',
			'/potd'
		);
		expect(practice.getByRole('menuitem', { name: /Problemset/ })).toHaveAttribute(
			'href',
			'/problemset'
		);
	});

	it('lists Roadmap, Papers and Blogs under Learn, in that order', () => {
		const learn = menu('Learn');
		const items = screen
			.getByRole('button', { name: 'Learn' })
			.parentElement!.querySelectorAll('li');
		const labels = [...items].map((item) => item.textContent?.trim().split(/\s+/)[0]);
		expect(labels).toEqual(['Roadmap', 'Papers', 'Blogs']);
		expect(learn.getByRole('menuitem', { name: /Papers/ })).toHaveAttribute('href', '/papers');
	});

	it('marks the pages that do not exist yet as soon', () => {
		const learn = menu('Learn');
		expect(learn.getAllByText('soon')).toHaveLength(2);
		expect(learn.queryByRole('menuitem', { name: /Roadmap|Blogs/ })).toBeNull();
	});

	it('no longer links Research paper from the top level', () => {
		expect(screen.queryByRole('link', { name: 'Research paper' })).toBeNull();
	});
});
