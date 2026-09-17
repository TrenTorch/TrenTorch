import { render, screen } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import DifficultyBadge from './DifficultyBadge.svelte';

// Smoke test for the jsdom/component-testing project itself (see
// .config/vite.config.ts's 'client' project) -- proves a real .svelte
// file mounts and renders, not just that the harness starts.
describe('DifficultyBadge', () => {
	it.each(['Easy', 'Medium', 'Hard'] as const)('renders the %s label', (difficulty) => {
		render(DifficultyBadge, { difficulty });
		expect(screen.getByText(difficulty)).toBeInTheDocument();
	});
});
