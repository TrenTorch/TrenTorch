import { describe, it, expect, vi, beforeEach } from 'vitest';

const mockSession = vi.hoisted(() => ({ isLoading: false, user: null as object | null }));
vi.mock('./session.svelte', () => ({ session: mockSession }));

import { gateBehindSignIn } from './gate-behind-sign-in';
import { signInPrompt } from './sign-in-prompt.svelte';
import { takeAfterSignInDestination } from './after-sign-in-destination';

function fakeStorage() {
	const data = new Map<string, string>();
	return {
		getItem: (k: string) => data.get(k) ?? null,
		setItem: (k: string, v: string) => void data.set(k, v),
		removeItem: (k: string) => void data.delete(k)
	};
}

// A click on a link; `href` is what the browser reports for the anchor, which
// is always an absolute URL even when the page wrote a relative one.
function click(overrides: Partial<MouseEvent> = {}, href = 'https://trentorch.com/questions') {
	const event = {
		button: 0,
		metaKey: false,
		ctrlKey: false,
		shiftKey: false,
		altKey: false,
		defaultPrevented: false,
		currentTarget: { href },
		preventDefault: vi.fn(),
		...overrides
	};
	return event as unknown as MouseEvent & { preventDefault: ReturnType<typeof vi.fn> };
}

beforeEach(() => {
	vi.stubGlobal('sessionStorage', fakeStorage());
	mockSession.isLoading = false;
	mockSession.user = null;
	signInPrompt.close();
});

describe('gateBehindSignIn', () => {
	it('signed out: stops the navigation, opens the sign-in dialog, and remembers the destination', () => {
		const event = click();
		gateBehindSignIn(event);

		expect(event.preventDefault).toHaveBeenCalled();
		expect(signInPrompt.isOpen).toBe(true);
		expect(signInPrompt.reason).toBe('browse');
		expect(takeAfterSignInDestination()).toBe('/questions');
	});

	it('remembers only the path and query of the clicked link, never its origin', () => {
		gateBehindSignIn(click({}, 'https://trentorch.com/questions?page=3#top'));
		expect(takeAfterSignInDestination()).toBe('/questions?page=3');
	});

	it('signed in: lets the click navigate normally', () => {
		mockSession.user = { id: 'u1' };
		const event = click();
		gateBehindSignIn(event);

		expect(event.preventDefault).not.toHaveBeenCalled();
		expect(signInPrompt.isOpen).toBe(false);
		expect(takeAfterSignInDestination()).toBeNull();
	});

	it('session still loading: lets the click through instead of guessing', () => {
		mockSession.isLoading = true;
		const event = click({}, 'https://trentorch.com/potd');
		gateBehindSignIn(event);

		expect(event.preventDefault).not.toHaveBeenCalled();
		expect(signInPrompt.isOpen).toBe(false);
	});

	it.each([
		['middle click', { button: 1 }],
		['ctrl click', { ctrlKey: true }],
		['meta click', { metaKey: true }],
		['shift click', { shiftKey: true }]
	])('%s (opens elsewhere): not intercepted', (_name, overrides) => {
		const event = click(overrides);
		gateBehindSignIn(event);

		expect(event.preventDefault).not.toHaveBeenCalled();
		expect(signInPrompt.isOpen).toBe(false);
	});

	it('leaves a click another handler already cancelled alone', () => {
		gateBehindSignIn(click({ defaultPrevented: true }));
		expect(signInPrompt.isOpen).toBe(false);
	});

	it('does nothing for an element that is not a link', () => {
		const event = click({}, '');
		gateBehindSignIn(event);

		expect(event.preventDefault).not.toHaveBeenCalled();
		expect(signInPrompt.isOpen).toBe(false);
	});
});

describe('takeAfterSignInDestination', () => {
	it('returns a remembered path once, then nothing', () => {
		gateBehindSignIn(click({}, 'https://trentorch.com/potd'));
		expect(takeAfterSignInDestination()).toBe('/potd');
		expect(takeAfterSignInDestination()).toBeNull();
	});

	it.each(['//evil.example', 'https://evil.example/x', 'javascript:alert(1)', '/a\\b'])(
		'refuses %s so nobody can be sent off-site',
		(value) => {
			sessionStorage.setItem('trentorch-after-sign-in', value);
			expect(takeAfterSignInDestination()).toBeNull();
		}
	);

	it('returns null when storage is unavailable', () => {
		vi.stubGlobal('sessionStorage', {
			getItem: () => {
				throw new Error('blocked');
			}
		});
		expect(takeAfterSignInDestination()).toBeNull();
	});
});
