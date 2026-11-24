import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { afterEach, describe, expect, it, vi } from 'vitest';
import DsaPage from './+page.svelte';
import { dsaSteps } from '$data/dsa-sheet';

vi.mock('$app/state', () => ({
	page: { url: new URL('http://localhost/dsa') }
}));

vi.mock('$app/paths', () => ({
	resolve: (path: string) => path
}));

vi.mock('$processes/progress-tracking/attempted.svelte', () => ({
	attempted: { slugs: new Set<string>() }
}));

vi.mock('$processes/progress-tracking/recent.svelte', () => ({
	recent: { get: () => undefined }
}));

vi.mock('$processes/progress-tracking/solved.svelte', () => ({
	solved: { slugs: new Set<string>() }
}));

const target = (() => {
	const step = dsaSteps.find((item) => item.topics.some((topic) => topic.questions.length > 0));
	const topic = step?.topics.find((item) => item.questions.length > 0);
	const question = topic?.questions[0];
	if (!step || !topic || !question) throw new Error('The DSA sheet must have a question to test.');
	return { step, topic, question };
})();

const buttonStartingWith = (label: string) =>
	screen.getByRole('button', { name: (name) => name.startsWith(label) });
const stepButton = () => buttonStartingWith(target.step.title);
const topicButton = () => buttonStartingWith(target.topic.title);
const searchInput = () => screen.getByPlaceholderText('Search questions or tags...');
const bodyFor = (button: HTMLElement) => {
	const id = button.getAttribute('aria-controls');
	if (!id) throw new Error('Accordion button must reference its controlled body.');
	return document.getElementById(id);
};
const searchFor = (query: string) => fireEvent.input(searchInput(), { target: { value: query } });

describe('DSA page filtered accordion', () => {
	afterEach(cleanup);

	it('automatically expands matching steps and topics when a filter is applied', async () => {
		render(DsaPage);
		await searchFor(target.question.title);

		expect(stepButton()).toHaveAttribute('aria-expanded', 'true');
		expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
		expect(screen.getByText(target.question.title)).toBeInTheDocument();
	});

	it('lets users collapse and reopen steps while filtering', async () => {
		render(DsaPage);
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
		render(DsaPage);
		await searchFor(target.question.title);

		expect(bodyFor(topicButton())).not.toBeNull();
		await fireEvent.click(topicButton());
		expect(topicButton()).toHaveAttribute('aria-expanded', 'false');
		expect(bodyFor(topicButton())).toBeNull();

		await fireEvent.click(topicButton());
		expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
		expect(bodyFor(topicButton())).not.toBeNull();
	});

	it('resets filtered collapse choices when the search criteria change', async () => {
		render(DsaPage);
		await searchFor(target.question.title);
		await fireEvent.click(topicButton());
		await fireEvent.click(stepButton());

		await searchFor(target.question.title.toUpperCase());

		expect(stepButton()).toHaveAttribute('aria-expanded', 'true');
		expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
	});

	it('restores normal accordion state when filters are cleared', async () => {
		render(DsaPage);
		await fireEvent.click(stepButton());
		await searchFor(target.question.title);
		expect(topicButton()).toHaveAttribute('aria-expanded', 'true');

		await fireEvent.click(topicButton());
		expect(topicButton()).toHaveAttribute('aria-expanded', 'false');
		await searchFor('');

		expect(stepButton()).toHaveAttribute('aria-expanded', 'true');
		expect(topicButton()).toHaveAttribute('aria-expanded', 'false');

		await searchFor(target.question.title);
		expect(topicButton()).toHaveAttribute('aria-expanded', 'true');
	});
});
