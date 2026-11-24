import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { afterEach, describe, it, expect, vi } from 'vitest';
import { dsaSteps } from '$data/dsa-sheet';
import { softwareSilos } from '$data/software-silos';
import SoftwarePage from './+page.svelte';

vi.mock('$app/state', () => ({ page: { url: new URL('http://localhost/modules/software') } }));
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

describe('Software Engineering page', () => {
	afterEach(cleanup);

	it('puts every step of the sheet in exactly one silo', () => {
		const placed = softwareSilos.flatMap((silo) => silo.steps).sort();
		expect(placed).toEqual(dsaSteps.map((step) => step.id).sort());
	});

	it('lists the silos collapsed', () => {
		render(SoftwarePage);
		for (const silo of softwareSilos) {
			expect(screen.getByRole('button', { name: new RegExp(`^${silo.title}`) })).toHaveAttribute(
				'aria-expanded',
				'false'
			);
		}
	});

	it('opens a silo in place and shows its steps', async () => {
		render(SoftwarePage);
		const first = screen.getByRole('button', { name: new RegExp(`^${softwareSilos[0].title}`) });
		await fireEvent.click(first);
		expect(first).toHaveAttribute('aria-expanded', 'true');
		const step = dsaSteps.find((s) => s.id === softwareSilos[0].steps[0])!;
		expect(screen.getByRole('button', { name: new RegExp(step.title) })).toBeInTheDocument();
	});
});
