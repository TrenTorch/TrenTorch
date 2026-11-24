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

	describe('filtered accordion', () => {
		// Behaviour first fixed for the old /dsa page in #800, kept on the silos' steps and topics.
		const target = (() => {
			const step = dsaSteps.find((item) => item.topics.some((topic) => topic.questions.length > 0));
			const topic = step?.topics.find((item) => item.questions.length > 0);
			const question = topic?.questions[0];
			if (!step || !topic || !question) throw new Error('The sheet must have a question to test.');
			return { step, topic, question };
		})();
		const siloTitle = softwareSilos.find((silo) => silo.steps.includes(target.step.id))!.title;

		const buttonStartingWith = (label: string) =>
			screen.getByRole('button', { name: (name) => name.startsWith(label) });
		const stepButton = () => buttonStartingWith(target.step.title);
		const topicButton = () => buttonStartingWith(target.topic.title);
		const bodyFor = (button: HTMLElement) => {
			const id = button.getAttribute('aria-controls');
			if (!id) throw new Error('Accordion button must reference its controlled body.');
			return document.getElementById(id);
		};
		const searchFor = (query: string) =>
			fireEvent.input(screen.getByPlaceholderText('Search questions or tags...'), {
				target: { value: query }
			});

		it('expands matching steps and topics when a filter is applied', async () => {
			render(SoftwarePage);
			await searchFor(target.question.title);
			expect(stepButton()).toHaveAttribute('aria-expanded', 'true');
			expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
			expect(screen.getByText(target.question.title)).toBeInTheDocument();
		});

		it('lets users collapse and reopen steps while filtering', async () => {
			render(SoftwarePage);
			await searchFor(target.question.title);
			expect(bodyFor(stepButton())).not.toBeNull();
			await fireEvent.click(stepButton());
			expect(stepButton()).toHaveAttribute('aria-expanded', 'false');
			expect(bodyFor(stepButton())).toBeNull();
			await fireEvent.click(stepButton());
			expect(stepButton()).toHaveAttribute('aria-expanded', 'true');
			expect(bodyFor(stepButton())).not.toBeNull();
		});

		it('lets users collapse and reopen topics while filtering', async () => {
			render(SoftwarePage);
			await searchFor(target.question.title);
			expect(bodyFor(topicButton())).not.toBeNull();
			await fireEvent.click(topicButton());
			expect(topicButton()).toHaveAttribute('aria-expanded', 'false');
			expect(bodyFor(topicButton())).toBeNull();
			await fireEvent.click(topicButton());
			expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
		});

		it('lets users collapse a silo while filtering', async () => {
			render(SoftwarePage);
			await searchFor(target.question.title);
			const silo = buttonStartingWith(siloTitle);
			expect(silo).toHaveAttribute('aria-expanded', 'true');
			await fireEvent.click(silo);
			expect(silo).toHaveAttribute('aria-expanded', 'false');
		});

		it('resets filtered collapse choices when the search criteria change', async () => {
			render(SoftwarePage);
			await searchFor(target.question.title);
			await fireEvent.click(topicButton());
			await fireEvent.click(stepButton());
			await searchFor(target.question.title.toUpperCase());
			expect(stepButton()).toHaveAttribute('aria-expanded', 'true');
			expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
		});

		it('restores the normal accordion state when filters are cleared', async () => {
			render(SoftwarePage);
			await fireEvent.click(buttonStartingWith(siloTitle));
			await fireEvent.click(stepButton());
			await searchFor(target.question.title);
			await fireEvent.click(topicButton());
			expect(topicButton()).toHaveAttribute('aria-expanded', 'false');
			await searchFor('');
			// The silos start closed again once the filter clears; the step and topic state is kept.
			expect(buttonStartingWith(siloTitle)).toHaveAttribute('aria-expanded', 'false');
			await fireEvent.click(buttonStartingWith(siloTitle));
			expect(stepButton()).toHaveAttribute('aria-expanded', 'true');
			expect(topicButton()).toHaveAttribute('aria-expanded', 'false');
			await searchFor(target.question.title);
			expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
		});
	});
});
