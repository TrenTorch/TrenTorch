import { cleanup, render, screen } from '@testing-library/svelte';
import { afterEach, describe, expect, it } from 'vitest';
import StatTile from './StatTile.svelte';

describe('StatTile', () => {
	afterEach(cleanup);

	it('shows the value and the label', () => {
		render(StatTile, { label: 'Questions', value: 454 });
		expect(screen.getByText('454')).toBeInTheDocument();
		expect(screen.getByText('Questions')).toBeInTheDocument();
	});

	it('shows just the count while nothing is solved', () => {
		render(StatTile, { label: 'Questions', value: 454, progress: { done: 0, total: 454 } });
		expect(screen.queryByRole('progressbar')).toBeNull();
		expect(screen.queryByText(/solved/)).toBeNull();
	});

	it('shows a bar and how many are solved once any are', () => {
		render(StatTile, { label: 'Questions', value: 454, progress: { done: 45, total: 454 } });
		const bar = screen.getByRole('progressbar', { name: 'Questions solved' });
		expect(bar).toHaveAttribute('aria-valuenow', '45');
		expect(bar).toHaveAttribute('aria-valuemax', '454');
		expect(bar.firstElementChild).toHaveStyle({ width: `${(45 / 454) * 100}%` });
		expect(screen.getByText('45 solved')).toBeInTheDocument();
	});

	it('fills the bar when everything is solved', () => {
		render(StatTile, { label: 'Questions', value: 10, progress: { done: 10, total: 10 } });
		expect(screen.getByRole('progressbar').firstElementChild).toHaveStyle({ width: '100%' });
	});

	it('says what the bar counts, for tiles that count something other than solved', () => {
		render(StatTile, {
			label: 'Progressions',
			value: 21,
			progress: { done: 2, total: 21 },
			progressLabel: 'complete'
		});
		expect(screen.getByRole('progressbar', { name: 'Progressions complete' })).toBeInTheDocument();
		expect(screen.getByText('2 complete')).toBeInTheDocument();
		expect(screen.queryByText(/solved/)).toBeNull();
	});
});
