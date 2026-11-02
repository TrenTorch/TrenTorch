import { cleanup, fireEvent, render, screen, within } from '@testing-library/svelte';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import Harness from './FilterBar.harness.svelte';

// jsdom has neither of these; FilterBar uses them to fade a scrolling chip list and to keep the popover on screen.
class NoopObserver {
	observe() {}
	disconnect() {}
}

// What the harness bound, read back from the page.
const bound = () => JSON.parse(screen.getByTestId('bound').textContent ?? '{}');
const trigger = () => screen.getByRole('button', { name: /^Filters/ });
const dialog = () => screen.getByRole('dialog', { name: 'Filters' });
const openPopover = async () => {
	await fireEvent.click(trigger());
	return within(dialog());
};

describe('FilterBar', () => {
	beforeEach(() => {
		vi.stubGlobal('ResizeObserver', NoopObserver);
		window.scrollBy = vi.fn();
	});
	afterEach(() => {
		cleanup();
		vi.unstubAllGlobals();
	});

	describe('the bar', () => {
		it('shows the search box, the Filters button and the result count', () => {
			const { container } = render(Harness);
			expect(screen.getByPlaceholderText('Search problems...')).toBeInTheDocument();
			expect(trigger()).toHaveAttribute('aria-expanded', 'false');
			expect(container.querySelector('.result-line')).toHaveTextContent('349 problems');
		});

		it('says "problem" for one result, and uses the noun it is given', () => {
			const one = render(Harness, { resultCount: 1 });
			expect(one.container.querySelector('.result-line')).toHaveTextContent('1 problem');
			expect(one.container.querySelector('.result-line')).not.toHaveTextContent('problems');
			cleanup();
			const lean = render(Harness, { mode: 'lean', resultCount: 454 });
			expect(screen.getByPlaceholderText('Search questions or tags...')).toBeInTheDocument();
			expect(lean.container.querySelector('.result-line')).toHaveTextContent('454 questions');
		});

		it('writes what is typed into the bound query', async () => {
			render(Harness);
			await fireEvent.input(screen.getByPlaceholderText('Search problems...'), {
				target: { value: 'softmax' }
			});
			expect(bound().query).toBe('softmax');
		});

		it('hints at the "/" shortcut, and hides the hint once there is text', async () => {
			const { container } = render(Harness);
			expect(container.querySelector('.search-key')).toBeInTheDocument();
			await fireEvent.input(screen.getByPlaceholderText('Search problems...'), {
				target: { value: 'x' }
			});
			expect(container.querySelector('.search-key')).not.toBeInTheDocument();
		});

		it('focuses the search box when "/" is pressed, but not while typing elsewhere', async () => {
			render(Harness);
			const search = screen.getByPlaceholderText('Search problems...');
			await fireEvent.keyDown(document.body, { key: '/' });
			expect(search).toHaveFocus();

			const popover = await openPopover();
			const topicSearch = popover.getByLabelText('Find a topic');
			topicSearch.focus();
			await fireEvent.keyDown(topicSearch, { key: '/' });
			expect(topicSearch).toHaveFocus();
		});
	});

	describe('the popover', () => {
		it('opens from the button and closes from it', async () => {
			render(Harness);
			expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
			await openPopover();
			expect(trigger()).toHaveAttribute('aria-expanded', 'true');
			await fireEvent.click(trigger());
			expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
		});

		it('closes on Escape and puts focus back on the button', async () => {
			render(Harness);
			await openPopover();
			await fireEvent.keyDown(document.body, { key: 'Escape' });
			expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
			expect(trigger()).toHaveFocus();
		});

		it('closes when the pointer goes down outside it, but not inside it', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.pointerDown(popover.getByText('Module'));
			expect(screen.getByRole('dialog')).toBeInTheDocument();
			await fireEvent.pointerDown(document.body);
			expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
		});

		it('closes from its own close button and from "Show N problems"', async () => {
			render(Harness);
			let popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Close filters' }));
			expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

			popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Show 349 problems' }));
			expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
		});

		it('puts the live result count on its button', async () => {
			render(Harness, { resultCount: 1 });
			const popover = await openPopover();
			expect(popover.getByRole('button', { name: 'Show 1 problem' })).toBeInTheDocument();
		});
	});

	describe('choosing filters', () => {
		it('sets a module, a difficulty, a status, a topic and a company, one chip each', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Deep Learning' }));
			await fireEvent.click(popover.getByRole('button', { name: 'Advanced' }));
			await fireEvent.click(popover.getByRole('button', { name: /Solved/ }));
			await fireEvent.click(popover.getByRole('button', { name: /Attention mechanism/ }));
			await fireEvent.click(popover.getByRole('button', { name: /Adobe/ }));
			expect(bound()).toMatchObject({
				moduleId: 'dl',
				difficulty: 'Advanced',
				status: 'solved',
				topic: 'attention',
				company: 'Adobe'
			});
			expect(popover.getByRole('button', { name: 'Advanced' })).toHaveAttribute(
				'aria-pressed',
				'true'
			);
		});

		it('picking a chip again clears it, and a status clears back to "all"', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Beginner' }));
			await fireEvent.click(popover.getByRole('button', { name: /Unsolved/ }));
			await fireEvent.click(popover.getByRole('button', { name: 'Beginner' }));
			await fireEvent.click(popover.getByRole('button', { name: /Unsolved/ }));
			expect(bound()).toMatchObject({ difficulty: '', status: 'all' });
		});

		it('replaces a choice in the same group instead of adding to it', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Beginner' }));
			await fireEvent.click(popover.getByRole('button', { name: 'Advanced' }));
			expect(bound().difficulty).toBe('Advanced');
			expect(popover.getByRole('button', { name: 'Beginner' })).toHaveAttribute(
				'aria-pressed',
				'false'
			);
		});

		it('turns Past Problem of the Day on and off with its switch', async () => {
			render(Harness);
			const popover = await openPopover();
			const toggle = popover.getByRole('switch');
			expect(toggle).toHaveAttribute('aria-checked', 'false');
			await fireEvent.click(toggle);
			expect(bound().pastPotd).toBe(true);
			expect(toggle).toHaveAttribute('aria-checked', 'true');
			await fireEvent.click(toggle);
			expect(bound().pastPotd).toBe(false);
		});
	});

	describe('long lists', () => {
		it('narrows topics and companies as you type, and says when nothing matches', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.input(popover.getByLabelText('Find a topic'), { target: { value: 'att' } });
			expect(popover.getByRole('button', { name: /Attention mechanism/ })).toBeInTheDocument();
			expect(popover.queryByRole('button', { name: /A\/B Testing/ })).not.toBeInTheDocument();

			await fireEvent.input(popover.getByLabelText('Find a topic'), { target: { value: 'zzz' } });
			expect(popover.getByText('No topic matches "zzz".')).toBeInTheDocument();

			await fireEvent.input(popover.getByLabelText('Find a company'), { target: { value: 'ado' } });
			expect(popover.getByRole('button', { name: /Adobe/ })).toBeInTheDocument();
			expect(popover.queryByRole('button', { name: /AWS/ })).not.toBeInTheDocument();
		});

		it('shows how many problems each topic and company has', async () => {
			render(Harness);
			const popover = await openPopover();
			expect(popover.getByRole('button', { name: 'Attention mechanism 5' })).toBeInTheDocument();
			expect(popover.getByRole('button', { name: 'Adobe 4' })).toBeInTheDocument();
		});
	});

	describe('what is applied', () => {
		it('shows each active filter as a chip, with a count on the button', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Deep Learning' }));
			await fireEvent.click(popover.getByRole('button', { name: 'Advanced' }));
			expect(
				screen.getByRole('button', { name: 'Remove Module filter: Deep Learning' })
			).toBeVisible();
			expect(
				screen.getByRole('button', { name: 'Remove Difficulty filter: Advanced' })
			).toBeVisible();
			expect(trigger()).toHaveAccessibleName(/2 active/);
		});

		it('shows no chips and no count when nothing is chosen', () => {
			const { container } = render(Harness);
			expect(container.querySelector('.applied')).not.toBeInTheDocument();
			expect(container.querySelector('.trigger-count')).not.toBeInTheDocument();
		});

		it('removes just that filter when its chip is pressed', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Deep Learning' }));
			await fireEvent.click(popover.getByRole('button', { name: 'Advanced' }));
			await fireEvent.click(
				screen.getByRole('button', { name: 'Remove Module filter: Deep Learning' })
			);
			expect(bound()).toMatchObject({ moduleId: '', difficulty: 'Advanced' });
		});

		it('clears every filter with "Clear all", and the search text stays', async () => {
			render(Harness);
			await fireEvent.input(screen.getByPlaceholderText('Search problems...'), {
				target: { value: 'norm' }
			});
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Advanced' }));
			await fireEvent.click(popover.getByRole('switch'));
			await fireEvent.click(screen.getByRole('button', { name: 'Clear all' }));
			expect(bound()).toEqual({
				query: 'norm',
				moduleId: '',
				topic: '',
				company: '',
				difficulty: '',
				status: 'all',
				pastPotd: false
			});
		});

		it('resets from the popover header too', async () => {
			render(Harness);
			let popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Beginner' }));
			popover = within(dialog());
			await fireEvent.click(popover.getByRole('button', { name: /reset/ }));
			expect(bound().difficulty).toBe('');
		});

		it('lists the Past POTD switch as an applied filter', async () => {
			render(Harness);
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('switch'));
			expect(screen.getByRole('button', { name: 'Remove Only filter: Past POTD' })).toBeVisible();
		});
	});

	describe('as the DSA sheet uses it (difficulty and status only)', () => {
		it('has no module, topic or company section and no switch', async () => {
			render(Harness, { mode: 'lean' });
			const popover = await openPopover();
			expect(popover.getByText('Difficulty')).toBeInTheDocument();
			expect(popover.getByText('Status')).toBeInTheDocument();
			expect(popover.queryByText('Module')).not.toBeInTheDocument();
			expect(popover.queryByText(/^Topic/)).not.toBeInTheDocument();
			expect(popover.queryByText(/^Company/)).not.toBeInTheDocument();
			expect(popover.queryByRole('switch')).not.toBeInTheDocument();
		});

		it('still filters, and counts questions', async () => {
			render(Harness, { mode: 'lean', resultCount: 110 });
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Advanced' }));
			expect(bound().difficulty).toBe('Advanced');
			expect(popover.getByRole('button', { name: 'Show 110 questions' })).toBeInTheDocument();
		});

		it('does not add a Past POTD chip when "Clear all" is used', async () => {
			render(Harness, { mode: 'lean' });
			const popover = await openPopover();
			await fireEvent.click(popover.getByRole('button', { name: 'Advanced' }));
			await fireEvent.click(screen.getByRole('button', { name: 'Clear all' }));
			expect(bound()).toMatchObject({ difficulty: '', status: 'all' });
			expect(bound().pastPotd).toBe(false);
		});
	});

	describe('as the Modules and Problem of the Day pages use it (a topic and a status, and a total)', () => {
		it('shows no count line while nothing is filtered, because the page already says how many', () => {
			const { container } = render(Harness, { mode: 'topics', resultCount: 1397, total: 1397 });
			expect(container.querySelector('.result-line')).toBeNull();
		});

		it('says "12 of 1397 questions" once the search or a filter narrows it', async () => {
			const { container } = render(Harness, { mode: 'topics', resultCount: 12, total: 1397 });
			await fireEvent.input(screen.getByPlaceholderText('Search problems...'), {
				target: { value: 'soft' }
			});
			expect(container.querySelector('.result-line')).toHaveTextContent('12 of 1397 questions');
			await fireEvent.input(screen.getByPlaceholderText('Search problems...'), {
				target: { value: '' }
			});
			expect(container.querySelector('.result-line')).toBeNull();
			const panel = await openPopover();
			await fireEvent.click(panel.getByRole('button', { name: /Attention/ }));
			expect(container.querySelector('.result-line')).toHaveTextContent('12 of 1397 questions');
		});

		it('leaves out the Difficulty section when there are no difficulties, and keeps Status and Topic', async () => {
			render(Harness, { mode: 'topics' });
			const panel = await openPopover();
			expect(panel.queryByText('Difficulty')).toBeNull();
			expect(panel.getByText('Status')).toBeInTheDocument();
			expect(panel.getByRole('button', { name: /Solved/ })).toBeInTheDocument();
			expect(panel.getByRole('button', { name: /Attention/ })).toBeInTheDocument();
		});

		it('still shows the count line always when no total is given, as the Problemset used to', () => {
			const { container } = render(Harness, { mode: 'lean', resultCount: 454 });
			expect(container.querySelector('.result-line')).toHaveTextContent('454 questions');
		});
	});
});
