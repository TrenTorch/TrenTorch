import { cleanup, render, screen } from '@testing-library/svelte';
import { afterEach, describe, it, expect } from 'vitest';
import PartTree from './PartTree.svelte';
import type { Part, Section, Track } from '$data/questions';

const track = (name: string, slug: string): Track => ({
	name,
	questions: [{ slug, title: `Question ${slug}`, difficulty: 'Easy', topics: ['t'] }]
});
const section = (name: string, ...tracks: Track[]): Section => ({
	name,
	tracks,
	questions: tracks.flatMap((t) => t.questions)
});
const part = (title: string, ...sections: Section[]): Part => ({
	id: 'part-x',
	title,
	sections,
	tracks: sections.flatMap((s) => s.tracks)
});

describe('PartTree', () => {
	afterEach(cleanup);

	it('shows a section folder when it is named differently from its root', () => {
		render(PartTree, {
			part: part(
				'Reinforcement Learning',
				section('Tabular Methods', track('Bandits', 'a'), track('Q-Learning', 'b')),
				section('Post-Training', track('RLHF', 'c'), track('DPO', 'd'))
			),
			forceOpen: true
		});
		expect(screen.getByText('Tabular Methods')).toBeInTheDocument();
		expect(screen.getByText('Post-Training')).toBeInTheDocument();
	});

	it('shows the sub-sections directly when a section is named like its root', () => {
		render(PartTree, {
			part: part(
				'Reinforcement Learning',
				section('Post-Training', track('RLHF', 'c'), track('DPO', 'd')),
				section('Reinforcement Learning', track('Bandits', 'a'), track('Q-Learning', 'b'))
			),
			forceOpen: true
		});
		// No folder for the same-named section, but its sub-sections are there.
		expect(screen.queryByText('Reinforcement Learning')).not.toBeInTheDocument();
		expect(screen.getByText('Bandits')).toBeInTheDocument();
		expect(screen.getByText('Q-Learning')).toBeInTheDocument();
		// The other section still gets its folder.
		expect(screen.getByText('Post-Training')).toBeInTheDocument();
	});

	it('lists the same-named section first, even when it comes last in the folder order', () => {
		render(PartTree, {
			part: part(
				'Reinforcement Learning',
				section('Post-Training', track('RLHF', 'c'), track('DPO', 'd')),
				section('Reinforcement Learning', track('Bandits', 'a'), track('Q-Learning', 'b'))
			),
			forceOpen: true
		});
		const before = (first: string, second: string) =>
			screen.getByText(first).compareDocumentPosition(screen.getByText(second)) &
			Node.DOCUMENT_POSITION_FOLLOWING;
		expect(before('Bandits', 'Post-Training')).toBeTruthy();
		expect(before('Q-Learning', 'Post-Training')).toBeTruthy();
	});
});
