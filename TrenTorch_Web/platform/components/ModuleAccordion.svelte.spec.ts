import { cleanup, fireEvent, render, screen } from '@testing-library/svelte';
import { createRawSnippet } from 'svelte';
import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest';
import { Brain } from '@lucide/svelte';
import ModuleAccordion from './ModuleAccordion.svelte';

vi.mock('$app/paths', () => ({ resolve: (path: string) => path }));

const many = Array.from({ length: 9 }, (_, i) => ({
	id: `m${i}`,
	title: `Module ${i}`,
	icon: Brain,
	count: 3,
	solved: 0
}));
const items = [
	{ id: 'a', title: 'Alpha', icon: Brain, count: 4, solved: 0 },
	{ id: 'b', title: 'Beta', icon: Brain, count: 2, solved: 1 }
];
const children = createRawSnippet((item: () => { title: string }) => ({
	render: () => `<p>inside ${item().title}</p>`
}));

describe('ModuleAccordion', () => {
	beforeEach(() => {
		// jsdom has no layout, so no scrollIntoView.
		Element.prototype.scrollIntoView = vi.fn();
	});
	afterEach(cleanup);

	it('mounts nothing inside a module until it is opened', async () => {
		render(ModuleAccordion, { items, children });
		expect(screen.queryByText('inside Alpha')).toBeNull();
		await fireEvent.click(screen.getByRole('button', { name: /Alpha/ }));
		expect(screen.getByText('inside Alpha')).toBeInTheDocument();
		expect(screen.queryByText('inside Beta')).toBeNull();
	});

	it('closes an open module again', async () => {
		render(ModuleAccordion, { items, children });
		const button = screen.getByRole('button', { name: /Alpha/ });
		await fireEvent.click(button);
		await fireEvent.click(button);
		expect(screen.queryByText('inside Alpha')).toBeNull();
		expect(button).toHaveAttribute('aria-expanded', 'false');
	});

	it('opens the linked module from the start', () => {
		render(ModuleAccordion, { items, children, initialOpen: 'b' });
		expect(screen.getByText('inside Beta')).toBeInTheDocument();
		expect(screen.queryByText('inside Alpha')).toBeNull();
	});

	it('keeps every module open while filtering', () => {
		render(ModuleAccordion, { items, children, forceOpen: true });
		expect(screen.getByText('inside Alpha')).toBeInTheDocument();
		expect(screen.getByText('inside Beta')).toBeInTheDocument();
	});

	it('lets a module be closed while filtering, and reopens it when the filter changes', async () => {
		const { rerender } = render(ModuleAccordion, { items, children, forceOpen: true });
		await fireEvent.click(screen.getByRole('button', { name: /Alpha/ }));
		expect(screen.queryByText('inside Alpha')).toBeNull();
		expect(screen.getByText('inside Beta')).toBeInTheDocument();
		await rerender({ items: [items[0]], children, forceOpen: true });
		expect(screen.getByText('inside Alpha')).toBeInTheDocument();
	});

	it('keeps manual openings separate from filtering', async () => {
		const { rerender } = render(ModuleAccordion, { items, children, forceOpen: true });
		await fireEvent.click(screen.getByRole('button', { name: /Alpha/ }));
		await rerender({ items, children, forceOpen: false });
		expect(screen.queryByText('inside Alpha')).toBeNull();
		expect(screen.queryByText('inside Beta')).toBeNull();
	});

	it('shows how many questions are done', () => {
		render(ModuleAccordion, { items, children });
		expect(screen.getByText(/2 questions · 1 done/)).toBeInTheDocument();
		expect(screen.getByText(/4 questions/)).toBeInTheDocument();
	});

	it('shows four modules per page and pages through the rest', async () => {
		render(ModuleAccordion, { items: many, children });
		expect(screen.getAllByRole('button', { name: /Module \d/ })).toHaveLength(4);
		await fireEvent.click(screen.getByRole('button', { name: /next/i }));
		expect(screen.getByRole('button', { name: /Module 4/ })).toBeInTheDocument();
		expect(screen.queryByRole('button', { name: /Module 0/ })).toBeNull();
	});
});
